import argparse
import sys
import dropbox

## DEFINE GLOBAL VARIABLES
APP_KEY = ''
APP_SECRET = ''
REFRESH_TOKEN = ''
verbose = False

## OBTAIN KEY, SECRET, AND REFRESH TOKEN FROM COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description='dropbox_connect_test.py --appkey appkey --appsecret appsecret --reftoken refresh_token')
parser.add_argument('--verbose', help='turn on helpful output messages', action='store_true')
parser.add_argument('--appkey', nargs='?', help='App Key provided by Dropbox')
parser.add_argument('--appsecret', nargs='?', help='App Secret provided by Dropbox')
parser.add_argument('--reftoken', nargs='?', help='Reference Key provided by  Dropbox'
                                                  '(see https://www.dropbox.com/developers/apps)')

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
if not args.reftoken:
    print('--reftoken is mandatory')
    sys.exit(5)
else:
    REFRESH_TOKEN = args.reftoken
if args.verbose:
    verbose = True

if verbose:
    print('APPKEY: ' +  APP_KEY, ' APPSECRET: ' + APP_SECRET, ' REFRESH_TOKEN: ' + REFRESH_TOKEN)

# INITIALIZE THE DROPBOX OBJECT USING THE KEY, SECRET AND REFRESH TOKEN
# THE SDK HANDLES THE TOKEN REFRESH AUTOMATICALLY IN THE BACKGROUND
dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    oauth2_refresh_token=REFRESH_TOKEN
)

## INSERT API CALLS HERE
result = dbx.users_get_current_account()
print('ACCOUNT:\n', result)
root_namespace_id = dbx.users_get_current_account().root_info.root_namespace_id
print('ROOT_NAMESPACE:\n', root_namespace_id)
dbx = dbx.with_path_root(dropbox.common.PathRoot.root(root_namespace_id))
result = dbx.files_list_folder('')
print('LIST FOLDER:\n',result)
