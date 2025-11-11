#!/usr/bin/env python3
import argparse
import sys

from dropbox import DropboxOAuth2FlowNoRedirect

'''
USE THIS SCRIPT TO OBTAIN THE REFRESH TOKEN FOR YOUR APP USING THE
APP KEY AND THE SECRET KEY FROM THE DEVELOPERS APP CONSOLE.
'''

APP_KEY = ''
APP_SECRET = ''
verbose = False

## OBTAIN KEY AND SECRET FROM COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description='dropbox_connect_test.py --appkey appkey --appsecret appsecret --reftoken refresh_token')
parser.add_argument('--verbose', help='turn on detailed output messages', action='store_true')
parser.add_argument('--appkey', nargs='?', help='App Key provided by Dropbox')
parser.add_argument('--appsecret', nargs='?', help='App Secret provided by Dropbox')

## PARSE COMMAND LINE ARGUMENTS AND VERIFY
args = parser.parse_args()

if not args.appkey:
    print('--appkey is mandatory')
    sys.exit(3)
else:
    APP_KEY = args.appkey
if not args.appsecret:
    print('--appsecret is mandatory')
    sys.exit(4)
else:
    APP_SECRET = args.appsecret
if args.verbose:
    verbose = True

if verbose:
    print('APPKEY: ' +  APP_KEY, ' APPSECRET: ' + APP_SECRET)

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type="offline")

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
    print('REFRESH TOKEN           : ' + oauth_result.refresh_token)
    print('USER ID                 : ' + oauth_result.user_id)
    print('TEMPORARY ACCESS TOKEN  : ' + oauth_result.access_token)
    print('ACCESS TOKEN EXPIRES    : ' + oauth_result.expires_at.strftime('%Y-%m-%d-%H:%M'))
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)
