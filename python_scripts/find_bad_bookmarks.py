
## PYTHON PROGRAM TO LOOP A LIST OF BOOKMARKS AND
## REPORT ERRORS

from urllib2 import Request, urlopen, URLError, HTTPError
import fileinput
fname = './bookmarks.html'

### OPEN THE FILE AND READ EACH LINE
for line in fileinput.input():
    if(line.find('<A') > 0):
        strstart  =  line.find('<A')
        strend    =  line.find('>',strstart + 1)
        ## print ': ' + str(strstart) + ' : ' + str(strend)
        subline   = line[strstart:strend+1]
        urlstart  = subline.find('"')
        urlend    = subline.find('"',urlstart+1)
        urlstr    = subline[urlstart+1:urlend]
        req       = Request(urlstr)
        ### VALIDATE EACH URL
        try:
            response = urlopen(req)
        except HTTPError as e:
            print urlstr
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError as e:
            print urlstr
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason

