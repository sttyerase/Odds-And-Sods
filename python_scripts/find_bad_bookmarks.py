#! /usr/bin/python
## PYTHON PROGRAM TO LOOP A FILE OF BOOKMARKS EXPORTED FROM CHROME AND
## REPORT ERRORS
## TO RUN IN DEBUG MODE SET ENVIRONMENT VARIABLE DEBUG=true
## e.g., at the prompt enter:
##    DEBUG=true find_bad_bookmarks.py <bookmarks filename>

from urllib2 import Request, urlopen, URLError, HTTPError
import fileinput, os, ssl
from pip._vendor.urllib3.exceptions import SSLError

### OPEN THE FILE AND READ EACH LINE
count = 0
## DETERMINE DEBUG MODE AND OTHER ENV SETTINGS
try:
    DEBUG=os.environ['DEBUG']
except AttributeError:
    DEBUG = 'false'
except KeyError:
    DEBUG = 'false'
if(DEBUG == 'true'): print 'DEBUG: ', DEBUG
## BEGIN PROCESSING
## READ EACH LINE AND PARSE FOR WEB URL USING HREF=
for line in fileinput.input():
    count += 1
    if(line.find('HREF=') > 0):
        try:
            strstart  =  line.index('HREF=')
            urlstart  =  line.index('"',strstart + 1)
            urlend    =  line.index('"',urlstart + 1)
            urlstr    =  line[urlstart+1:urlend]
        except ValueError as ve:
            print 'ValueError: ', ve
            continue
        user_agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1)'
        ## FORCE GET METHOD.  ADD USER-AGENT HEADER TO REQUEST
        req       = Request(urlstr)
        req.add_header('User-Agent',user_agent)
        if(DEBUG == 'true'): print '####: ', urlstr,' METH: ', req.get_method(),' $$$$: ',req.has_data()
        ### VALIDATE EACH URL
        try:
            response = urlopen(req, timeout = 10)
        except HTTPError as e:
            print count, ' : ' ,urlstr
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code, ' : ', e.reason
        except URLError as e:
            print count, ' : ' ,urlstr
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        except ssl.SSLError as ssle:
            print count, ' : ' ,urlstr
            print 'SSL Error: ', ssle
    if(DEBUG == 'true'): print count
print 'Operation Complete.'
