import sys
import imp
import os
from jinja2 import Environment, FileSystemLoader
import markdown

#import settings.py
settings = imp.load_source('settings', './settings.py')

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print "You require Jinja2 to use Vite"
    sys.exit(0)


def get_path(dir_name):
    _current_path = os.getcwd()
    _path = ""
    if(os.path.exists(os.path.join(_current_path, dir_name))):
        _path = os.path.join(_current_path, dir_name)
    return _path

def file_dir_exists(name):
    return os.path.exists(get_path(name))

#Global objects
templates = ""
dirs = ()

def basic_check():
    #checking for available folders
    for dirName in settings.DATA_DIR:
        if not file_dir_exists( dirName) :
            print "Directory '" + dirName + "' is not present! please create a direcoty and try again."
            sys.exit(0)
    #data directories are available
    dirs = settings.DATA_DIR

    #checking for templates directory
    if settings.TEMPLATE_DIR == "":
        settings.TEMPLATE_DIR = "templates"

    if not file_dir_exists(settings.TEMPLATE_DIR) :
        print "Template directory is not present! please create a direcoty and try again."
        sys.exit(0)
    
    #Template directory is available
    templates = settings.TEMPLATE_DIR

def process_dir(dir_name):
    #check / create site dir

def init():
    basic_check()

    for dir_name in dirs:
        if file_dir_exists(dir_name):
            process_dir(dir_name)

def process_file(fileName):
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
    process_file("./posts/"+f)

