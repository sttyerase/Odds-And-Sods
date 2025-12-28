#! /usr/bin/env python3
## PYTHON PROGRAM TO LOOP A FILE OF BOOKMARKS EXPORTED FROM CHROME AND
## REPORT ERRORS
## TO RUN IN DEBUG MODE SET ENVIRONMENT VARIABLE DEBUG=true
## e.g., at the prompt enter:
##    DEBUG=true find_bad_bookmarks.py <bookmarks filename>
## Default values:
## DEBUG = FALSE
## REQTIMEOUT = 10

import urllib3
import fileinput, os, ssl, socket

## SET WORKING ENVIRONMENT
DEBUG ='false'
REQTIMEOUT = 10
count = 0
errcount = 0
http = urllib3.PoolManager
## DETERMINE DEBUG MODE AND OTHER ENV VARIABLES PASSED
try:
    DEBUG=os.environ['DEBUG']
    REQTIMEOUT=os.environ['REQTIMEOUT']
except AttributeError:
    DEBUG = 'false'
except KeyError:
    DEBUG = 'false'
if DEBUG == 'true': print ('DEBUG: ', DEBUG)
## BEGIN PROCESSING
## READ EACH LINE AND PARSE FOR WEB URL BETWEEN QUOTE MARKS STARTING WITH HREF=
for line in fileinput.input():
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
        user_agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1)'
        ## FORCE GET METHOD.  ADD USER-AGENT HEADER TO REQUEST
        if DEBUG == 'true': print ('####: ', urlstr, ' METH: ', 'GET', ' HAS_DATA: ', 'UNKNOWN', ' SCHEME: ', scheme)
        ### VALIDATE EACH URL
        try:
            response = http.request('GET',urlstr)
        except urllib3.exceptions.HTTPError as he:
            print (count, ' : ' ,urlstr)
            print ('ERROR: ', he)
            errcount+=1
        except urllib3.exceptions.RequestError as re:
            print (count, ' : ' ,urlstr)
            print ('ERROR: ',re)
            errcount+=1
        except ssl.CertificateError as ce:
            print ('SSL Cert Error: ', ce)
            errcount+=1
        except ssl.SSLError as ssle:
            print (count, ' : ' ,urlstr)
            print ('SSL Error: ', ssle)
            errcount+=1
        except socket.error as se:
            print ('Socket error: ', se)
            errcount+=1
    if DEBUG == 'true': print ('COUNT: ', count)
print ('Operation Complete. Errors counted: ', errcount)
