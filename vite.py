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

#############################Site################################
class Site:
    pages = [] 

#############################Page################################
class Page:
    author = "Unknown"
    title = "Untitle"
    date = "0/0/0"
    content = ""
    layout = ""
    url= ""
    
#################################################################
def get_path(dir_name, source = os.getcwd()):
    _current_path = source
    _path = ""
    if(os.path.exists(os.path.join(_current_path, dir_name))):
        _path = os.path.join(_current_path, dir_name)
    return _path

def file_dir_exists(name):
    return os.path.exists(get_path(name))

def create_dir(source, new_dir_name):
    if not file_dir_exists(os.path.join(source, new_dir_name)):
        os.mkdir(os.path.join(source, new_dir_name))
    return  get_path(new_dir_name, source)
   
#Global objects
templates = ""
dirs = ()
site = Site()

def basic_check():
    #checking for available folders
    for dirName in settings.DATA_DIR:
        if not file_dir_exists( dirName) :
            print "Directory '" + dirName + "' is not present! please create a direcoty and try again."
            sys.exit(0)
    #data directories are available
    global dirs
    dirs = settings.DATA_DIR

    #checking for templates directory
    if settings.TEMPLATE_DIR == "":
        settings.TEMPLATE_DIR = "templates"

    if not file_dir_exists(settings.TEMPLATE_DIR) :
        print "Template directory is not present! please create a direcoty and try again."
        sys.exit(0)
    
    #Template directory is available
    global templates
    templates = settings.TEMPLATE_DIR

def process_dir(dir_name):
    #check / create site dir
    if not file_dir_exists("site"):
        os.mkdir(os.path.join(os.getcwd(), "site"))
    _source_dir = get_path(dir_name)
    _dest_dir = create_dir(get_path("site"), dir_name)
    _files = os.listdir(_source_dir)
    for f in _files:
        page, content =  process_file(get_path(f, _source_dir), _dest_dir)
        #save page
        _dest_file_name = page.title.strip().lower().replace(" ", "_").strip()
        _dest_file_path = _dest_dir+"/"+_dest_file_name+".html"
        _dest_file = open(_dest_file_path, 'w')
        _dest_file.write(content)
        _dest_file.close()
        global site
        page.url = _dest_file_path
        site.pages.append(page)
    create_index()

def create_index():
    jinja_env = Environment(loader=FileSystemLoader(os.getcwd()))
    template = jinja_env.get_template("index.html")
    global site
    final_data = template.render(site=site)
    s = get_path("site")
    _dest_file = s + "/" + "index.html" 
    f = open(_dest_file, 'w')
    f.write(final_data)
    f.close()

def process_file(file_name, dest_dir):
    mf = open(file_name, 'r')
    if not mf:
        print file_name + " cann't be open";
        sys.exit(0)

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
    #print hDict
    page = Page()
    page.author = hDict["author"]
    page.title = hDict["title"]
    page.date = hDict["date"]
    page.layout = hDict["layout"]
        
    #get content
    mark = markdown.Markdown()
    page.content = mark.convert(text)
    jinja_env = Environment(loader=FileSystemLoader(get_path(templates)))
    template = jinja_env.get_template(page.layout.strip())
    final_data = template.render(page=page)
    return page, final_data
    
def init():
    print "Basic Checking...."
    basic_check()
    print "Done."
    for dir_name in dirs:
        if file_dir_exists(dir_name):
            process_dir(dir_name)

if __name__ == '__main__':
    init()


