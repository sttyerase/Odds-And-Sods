#! /usr/bin/env python3
"""
UPLOAD THE CONTENTS OF A LOCAL FOLDER TO A DROPBOX FOLDER
"""

from __future__ import print_function

import argparse
import contextlib
from datetime import datetime
import os
import six
import sys
import time
import unicodedata
import dropbox

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

APP_KEY = ''
APP_SECRET = ''
REFRESH_TOKEN = ''
START_MSG  = '============================== STARTING UPLOAD RUN ==================================='
FINISH_MSG = '============================== FINISHED UPLOAD RUN ==================================='
DRYRUN_MSG = '======================== DRY RUN NOT UPLOADING ANYTHING   ============================'
verbose = False
dry_run = False
parser = argparse.ArgumentParser(description='Send new local files to Dropbox folder')
parser.add_argument('folder', nargs='?', default='dropbox_load',
                    help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                    help='Local directory to upload')
parser.add_argument('--verbose','-v', help='turn on helpful output messages', action='store_true')
parser.add_argument('--dry_run', help='print messages but do not sync files', action='store_true')
parser.add_argument('--appkey', help='Your application key from Dropbox')
parser.add_argument('--appsecret', help='Your application secret from Dropbox')
parser.add_argument('--reftoken', help='Refresh token from Dropbox')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')
args = parser.parse_args()

## PARSE COMMAND LINE ARGUMENTS AND VERIFY VALUES
if not args.appkey:
    print('--appkey is mandatory')
    sys.exit(3)
else:
    APP_KEY = args.appkey
if not args.appsecret:
    print('--appkey is mandatory')
    sys.exit(4)
else:
    APP_SECRET = args.appsecret
if not args.reftoken:
    print('--reftoken is mandatory')
    sys.exit(5)
else:
    REFRESH_TOKEN = args.reftoken
if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
    print('At most one of --yes, --no, --default is allowed')
    sys.exit(6)
if args.verbose:
    verbose = True
if args.dry_run:  ## USE DRY_RUN FOR TESTING SCRIPT BEFORE DEPLOYMENT
    dry_run = True

folder = args.folder
rootdir = os.path.expanduser(args.rootdir)

# INITIALIZE THE DROPBOX OBJECT USING THE KEY, SECRET AND REFRESH TOKEN
# THE SDK HANDLES THE TOKEN REFRESH AUTOMATICALLY IN THE BACKGROUND
dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    oauth2_refresh_token=REFRESH_TOKEN
)

## DETERMINE THE TEAM SPACE ROOT FOLDER TO ACCESS THE TEAM SPACE FOLDER FT6_AnalyticsBD
root_namespace_id = dbx.users_get_current_account().root_info.root_namespace_id
dbx = dbx.with_path_root(dropbox.common.PathRoot.root(root_namespace_id))

def main():
    """ Main program. """
    """
    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    print(datetime.now(), START_MSG)
    if dry_run:
        print(datetime.now(),DRYRUN_MSG)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(6)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a directory on your filesystem')
        sys.exit(7)
    if verbose:
        print('VALUES: ', APP_KEY,' | ', APP_SECRET,' | ' ,REFRESH_TOKEN)

    ## ITERATE THROUGH DIRECTORIES AND FILES UNDER rootdir
    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        # FIRST DO ALL THE FILES.
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):  ## IF FILE NAME IS NOT INSTANCE OF STR
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    res = ''
                    if not dry_run:
                        res = download(dbx, folder, subfolder, name)
                    with open(fullname, 'rb') as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        if yesno('Refresh %s' % name, False, args):
                            if not dry_run:
                                upload(dbx, fullname, folder, subfolder, name, overwrite=True)
            elif yesno('Upload %s' % name, True, args):
                if not dry_run:
                    upload(dbx, fullname, folder, subfolder, name)

        # THEN CHOOSE WHICH SUBDIRECTORIES TO TRAVERSE.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            elif yesno('Descend into %s' % name, True, args):
                print('Keeping directory:', name)
                keep.append(name)
            else:
                print('OK, skipping directory:', name)
        dirs[:] = keep

    dbx.close()
    print(datetime.now(), FINISH_MSG)

def list_folder(ddbx, lfolder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (lfolder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = ddbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

def download(ddbx, dfolder, subfolder, name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (dfolder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = ddbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data

def upload(ddbx, fullname, ufolder, subfolder, name, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (ufolder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = ddbx.files_upload(data, path, mode,
                client_modified=datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res

def yesno(message, default, yargs):
    """Handy helper function to ask a yes/no question.

    Command line arguments --yes or --no force the answer;
    --default to force the default answer.

    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.

    Retry on unrecognized answer.

    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
    """
    if yargs.default:
        print(message + '? [auto]', 'Y' if default else 'N')
        return default
    if yargs.yes:
        print(message + '? [auto] YES')
        return True
    if yargs.no:
        print(message + '? [auto] NO')
        return False
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            print('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        print('Please answer YES or NO.')

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

if __name__ == '__main__':
    main()
