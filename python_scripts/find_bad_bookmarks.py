#! /usr/bin/python
## PYTHON PROGRAM TO LOOP A FILE OF BOOKMARKS EXPORTED FROM CHROME AND
## REPORT ERRORS
## TO RUN IN DEBUG MODE SET ENVIRONMENT VARIABLE DEBUG=true
## e.g., at the prompt enter:
##    DEBUG=true find_bad_bookmarks.py <bookmarks filename>
## Default values:
## DEBUG = FALSE
## REQTIMEOUT = 10

from urllib2 import Request, urlopen, URLError, HTTPError
import fileinput, os, ssl, socket, httplib
from pip._vendor.urllib3.exceptions import SSLError
from httplib import InvalidURL

## SET WORKING ENVIRONMENT
DEBUG ='false'
REQTIMEOUT = 10
count = 0
errcount = 0
## DETERMINE DEBUG MODE AND OTHER ENV VARIABLES PASSED
try:
    DEBUG=os.environ['DEBUG']
    REQTIMEOUT=os.environ['REQTIMEOUT']
except AttributeError:
    DEBUG = 'false'
except KeyError:
    DEBUG = 'false'
if(DEBUG == 'true'): print 'DEBUG: ', DEBUG
## BEGIN PROCESSING
## READ EACH LINE AND PARSE FOR WEB URL BETWEEN QUOTE MARKS STARTING WITH HREF=
for line in fileinput.input():
    count += 1
    if(line.find('HREF=') > 0):
        try:
            strstart  =  line.index('HREF=')
            urlstart  =  line.index('"',strstart + 1)
            urlend    =  line.index('"',urlstart + 1)
            urlstr    =  line[urlstart+1:urlend]
            ## TEST ONLY HTTP or HTTPS URLS
            scheme    =  urlstr[0:urlstr.index(":")]
            if(scheme !='http' and scheme != 'https'):
                print 'CANNOT TEST URI SCHEME: ', scheme
                continue
        except ValueError as ve:
            print 'ValueError: ', ve
            continue
        user_agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1)'
        ## FORCE GET METHOD.  ADD USER-AGENT HEADER TO REQUEST
        req       = Request(urlstr)
        req.add_header('User-Agent',user_agent)
        if(DEBUG == 'true'): print '####: ', urlstr,' METH: ', req.get_method(),' HAS_DATA: ',req.has_data(),' SCHEME: ', scheme
        ### VALIDATE EACH URL
        try:
            response = urlopen(req, timeout = REQTIMEOUT)
        except HTTPError as e:
            print count, ' : ' ,urlstr
            print 'Error code: ', e.code, ' : ', e.reason
            errcount+=1
        except URLError as e:
            print count, ' : ' ,urlstr
            print 'Reason: ', e.reason
            errcount+=1
        except ssl.SSLError as ssle:
            print count, ' : ' ,urlstr
            print 'SSL Error: ', ssle
            errcount+=1
        except ssl.CertificateError as ce:
            print 'SSL Cert Error: ', ce  
            errcount+=1
        except socket.error as se:
            print 'Socket error: ', se
            errcount+=1
        except InvalidURL as iu:
            print 'Badly formed URL: ', iu
            errcount+=1
    if(DEBUG == 'true'): print count
print 'Operation Complete. Errors counted: ', errcount
