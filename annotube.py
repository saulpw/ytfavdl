#!/usr/bin/python2.5

import cgi
import cgitb; cgitb.enable()

import sys
import urllib
import re
import xml 
import xml.dom.minidom

# FindT has to go to the 'v/' url, which redirects to an .swf query with one of
# the query parms being 't' (a secret necessary to download the raw .flv),
# and extract it from the redirected-to url.

def FindT(id):
    webpage = urllib.urlopen("http://www.youtube.com/watch?v=" + id).read()
    mobj = re.search(r', "t": "([^"]+)"', webpage)
    return mobj.group(1)

# annotateQuery runs a query with the youtube api and finds T for each of the
#  returned <entry>s and inserts it as an attribute on <entry t="a0s9f...">.
#  then returns the xml as a string

def annotateQuery(q):
    url = "http://gdata.youtube.com/feeds/api/" + q
    x = xml.dom.minidom.parseString(urllib.urlopen(url).read())
    for n in x.getElementsByTagName('entry'):
        id = n.getElementsByTagName("id")[0]
        strid = None
        for c in id.childNodes:
            if c.nodeType == xml.dom.Node.TEXT_NODE:
                strid = c.nodeValue.split("/")[-1]
                break
        t = FindT(strid)
        n.setAttribute("t", t)

    return x.toxml()


def getYoutubeDownloadURL(id, t=None):
    if not t:
        t = FindT(swfurl) 
    if t:
        return "http://www.youtube.com/get_video?video_id=%s&t=%s" % (id, t) 


if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        r = annotateQuery("users/%s/favorites?max-results=10" % username)
        print r
    else:
        form = cgi.FieldStorage()
        r = annotateQuery(form["q"].value)

        print "Content-type: text/xml"
        print 
        try:
            result = str(r)
        except UnicodeEncodeError:
            result = str(r.encode('iso8859', 'replace'))

        print result
    
