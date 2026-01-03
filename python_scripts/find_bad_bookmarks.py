#! /usr/bin/env python3
## PYTHON PROGRAM TO LOOP A FILE OF BOOKMARKS EXPORTED FROM CHROME OR FIREFOX AND
## REPORT ERRORS
## TO RUN IN DEBUG MODE SET ENVIRONMENT VARIABLE VERBOSE=true
## e.g., at the prompt enter:
##    VERBOSE=true find_bad_bookmarks.py <bookmarks file name>
## Default values:
## VERBOSE = false
## REQTIMEOUT = 5
import argparse
import sys
import certifi
import urllib3
import os

## SET WORKING ENVIRONMENT
VERBOSE ='false'
REQTIMEOUT = 5
count = 0
errcount = 0
skiplist = ['accounts.google.com']
## PARSE COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description='find_bad_bookmarks.py <bookmarks file name>')
parser.add_argument('filename',default='bookmarks.html')
args = parser.parse_args()
fname=args.filename
fobject = ''
http = urllib3.PoolManager(
    cert_reqs='REQUIRED',
    ca_certs=certifi.where()
)
## DETERMINE VERBOSE MODE AND OTHER ENV VARIABLES PASSED
try:
    VERBOSE=os.getenv("VERBOSE")
    REQTIMEOUT=os.getenv("REQTIMEOUT")
    fobject = open(fname)
except OSError :
    print ('UNABLE TO OPEN FILE ', fname)
    sys.exit(2)
except AttributeError:
    print('ATTRIBUTE ERROR. EXITING NOW.')
    sys.exit(3)
except KeyError:
    print('KEY MAPPING ERROR. EXITING NOW')
    sys.exit(4)
if VERBOSE == 'true': print ('VERBOSE: ', VERBOSE)
## BEGIN PROCESSING
## READ EACH LINE AND PARSE FOR WEB URL BETWEEN QUOTE MARKS STARTING WITH HREF=
for line in fobject:
    count += 1
    if line.find('HREF=') > 0:
        try:
            strstart  =  line.index('HREF=')
            urlstart  =  line.index('"',strstart + 1)
            urlend    =  line.index('"',urlstart + 1)
            urlstr    =  line[urlstart+1:urlend]
            ## TEST ONLY HTTP or HTTPS URLS
            scheme    =  urlstr[0:urlstr.index(":")]
            if scheme != 'http' and scheme != 'https':
                print ('CANNOT TEST URI SCHEME: ', scheme)
                continue
        except ValueError as ve:
            print ('ValueError: ', ve)
            continue
        ### VALIDATE EACH URL
        try:
            response = http.request('GET',urlstr)
            if VERBOSE == 'true': print ('####: ', urlstr,' STATUS: ',response.status ,' SCHEME: ', scheme)
            if response.status != 200 :
                errcount+=1
                if response.status == 403:
                    if VERBOSE == 'true': print ('UNAUTHORIZED REQUEST',urlstr)
                else:
                    print ('INVALID: ' + urlstr + ' :: STATUS: ' , response.status)
        except urllib3.exceptions.SSLError as ssle:
            print(f"SSL Verification Error: {ssle}")
        except Exception as re:
            print(f"RESPONSE ERROR: {re}")
    if VERBOSE == 'true': print ('COUNT: ', count)
print ('Operation Complete. Errors counted: ', errcount)
