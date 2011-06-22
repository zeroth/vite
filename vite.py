import sys
import imp
import os

settings = imp.load_source('settings', './settings.py')

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print "You require Jinja2 to use Vite"
    sys.exit(0)

for dirName in settings.DATA_DIR:
    if not os.path.exists("./" + dirName) :
        print "Directory '" + dirName + "' is not present! please create a direcoty and try again."
        sys.exit(0)

