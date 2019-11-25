#! /usr/bin/python
## PYTHON PROGRAM TO LOOP A FILE OF BOOKMARKS EXPORTED FROM CHROME AND
## REPORT ERRORS
## TO RUN IN DEBUG MODE SET ENVIRONMENT VARIABLE DEBUG=true

from urllib2 import Request, urlopen, URLError, HTTPError
import fileinput, os

### OPEN THE FILE AND READ EACH LINE
count = 0
DEBUG=os.environ['DEBUG']
if(DEBUG == 'true'): print 'DEBUG: ', DEBUG
for line in fileinput.input():
    count += 1
    if(line.find('HREF=') > 0):
        strstart  =  line.find('HREF=')
        strend    =  line.find('>',strstart + 1)
        subline   = line[strstart:strend+1]
        urlstart  = subline.find('"')
        urlend    = subline.find('"',urlstart+1)
        urlstr    = subline[urlstart+1:urlend]
        user_agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1)'
        headers = {'User-Agent' : user_agent}
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
    if(DEBUG == 'true'): print count
print 'Operation Complete.'
