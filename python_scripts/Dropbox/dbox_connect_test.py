"""
USE THIS SCRIPT TO TEST THE CREDENTIALS FOR DROPBOX

THIS SCRIPT TESTS OFFLINE CONNECTION TO DROPBOX USING THE CREDENTIALS CREATED
BY THE DEVELOPERS APP CONSOLE: https://www.dropbox.com/developers/apps.
THE CREDENTIALS ARE PROVIDED TO THE SCRIPT AS COMMAND LINE PARAMETERS:
"""

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

## EVALUATE THE CONNECTION
try:
    # Example API call
    account_info = dbx.users_get_current_account()
    print("Successfully connected to Dropbox account: \n   " ,account_info.name," \n   ",account_info.email)

    # You can now proceed with your production API calls,
    # and the SDK will manage the short-lived access tokens for you.

except dropbox.exceptions.AuthError as err:
    print("Authentication failed. Check your app key, app secret, and refresh token.")
    print(err)
except Exception as err:
    print(f"An error occurred: {err}")
