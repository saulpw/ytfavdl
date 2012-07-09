#!/usr/bin/python2.5

import cgi
import cgitb; cgitb.enable()

import sys
import urllib
import subprocess

form = cgi.FieldStorage()
url = "http://www.youtube.com/get_video?video_id=%s&t=%s" % (form["video_id"].value, form["t"].value)
f = urllib.urlopen(url)
print "Content-type: audio/mpeg"
print
cmd = "ffmpeg -vn -i - -f mp3 -acodec copy -"
subprocess.Popen(cmd.split(" "),
                 stdin = f.fileno(),
                 stdout = sys.stdout)

