= Youtube to MP3 Converter

The webserver needs to have python2.5 and ffmpeg installed, and be configured
for Python CGI.  

Add this to the apache2 config:

    # allow Python CGI
    Options ExecCGI
    AddHandler cgi-script py

    # so the streams are easily savable with nice filenames
    AliasMatch ^/yt2mp3/(.*)\.mp3$ /var/www/htdocs/tube2mp3.py

Copy these files into the above directory with the right permissions:

* tube2mp3.py: (cgi/python) youtube flv->mp3 converter

  given query parms 'video_id' and the corresponding 't', grabs the raw FLV
  from youtube, converts it to mp3 using ffmpeg, and dumps it back out as
  audio/mpeg.  Minimal latency and no disk storage required (all done using
  python and pipes).

* annotube.py: (cgi/python) youtube query forwarder 

  sends a query 'q' (prepending 'http://gdata.youtube.com/feeds/api/') to
  youtube; for each <entry> in the result, goes back to youtube to get 't', and
  stores it as an attribute ('t' of course) on <entry> tag.  Unfortunately,
  this script incurs no small amount of latency, and provides no feedback.

* style.css: (css) gives it that distinctive look.

* index.html: (ajax) to send a query through annotube and create some links to .mp3s, that the AliasMatch rule above sends to tube2mp3.py to convert from flv gotten from youtube.

Share and enjoy!
