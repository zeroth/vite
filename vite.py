import sys
import imp
import os
from jinja2 import Environment, FileSystemLoader
import markdown

settings = imp.load_source('settings', './settings.py')

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print "You require Jinja2 to use Vite"
    sys.exit(0)

#checking for available folders
for dirName in settings.DATA_DIR:
    if not os.path.exists("./" + dirName) :
        print "Directory '" + dirName + "' is not present! please create a direcoty and try again."
        sys.exit(0)

#checking for templates directory
if settings.TEMPLATE_DIR == "":
    settings.TEMPLATE_DIR = "templates"
    
if not os.path.exists("./" + settings.TEMPLATE_DIR):
    print "Template directory is not present! please create a direcoty and try again."
    sys.exit(0)

#### just to test Markdown 1st

def processFile(fileName):
    mf = open(fileName, 'r')
    if not mf:
        print fileName + " cann't be open";
    data = mf.read()
    header, _s_,  text = data.partition("%%")
    ## parse header
    hList = header.split("\n")
    hDict = {}
    for item in hList:
        if(item == ""):
            continue
        key, value = item.split(":")
        hDict[key] = value
    print hDict
    mark = markdown.Markdown()
    print mark.convert(text)
    
for f in os.listdir("./posts"):
    processFile("./posts/"+f)

