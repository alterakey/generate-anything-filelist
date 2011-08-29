import os
import re
import subprocess
import time

try:
    timeout = int(os.environ['INTERVAL'])
except (KeyError, ValueError):
    timeout = 3

try:
    root = os.environ['ROOT'].split(u':')
except KeyError:
    root = [u'.']

try:
    re_exclude = re.compile(os.environ['EXCLUDE'])
except KeyError:
    re_exclude = re.compile(ur'CVS|\.(svn|git|hg|dropbox\.cache|ccache|fseventsd|metadata)')

try:
    re_include = re.compile(os.environ['INCLUDE'])
except KeyError:
    re_include = re.compile(ur'.*')

try:
    output = os.environ['OUTPUT']
except KeyError:
    output = u'filelist'

while True:
    args = []
    args.append(u'find')
    args.extend(root)
    args.append(u'-type')
    args.append(u'f')
    finder = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
      with open(output, 'wb') as out:
          for l in finder.stdout:
              if re_include.search(l) and not re_exclude.search(l):
                  out.write(l)
    finally:
      finder.wait()
    time.sleep(timeout)
