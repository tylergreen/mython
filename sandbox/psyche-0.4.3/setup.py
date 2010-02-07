#!/usr/bin/env python2.2

from distutils.core import setup
import glob, os.path, sys


def get_command():
    """Returns the command for setup, ignoring all options"""
    for opt in sys.argv[1:]:
        if not opt.startswith("-"):
            return opt
    return None


def get_doc_root():
    if os.name not in ['nt', 'dos', 'ce']:
        return os.path.join("share", "doc", "psyche")
    else:
        return os.path.join("doc", "psyche")

def get_project_docs():
    """Returns a list of all Project docs"""
    return ["AUTHORS", "ChangeLog", "COPYING", "INSTALL", "NEWS",
            "README", "TODO", os.path.join("doc", "manual.pdf")]

def get_manuals():
    """Returns a list of all manual files"""
    # manual
    docs = glob.glob(os.path.join("doc", "manual", "*.html"))
    docs.append(os.path.join("doc", "manual", "manual.css"))

    if get_command() == "sdist":
        docs.append(os.path.join("doc", "manual.tex"))
        docs.append(os.path.join("doc", ".latex2html-init"))
        
    return docs


def get_packages():
    """Returns a list of all packages"""
    packages=['psyche',   # psyche
              'psyche.Plex'] # plex

    # for sdist, we want to include the tests
    if get_command() == "sdist":
        packages.append('psychetest')

    return packages

def get_scripts():
    """Returns a list of all scripts"""
    scripts=[]
    
    if get_command() == "sdist" or os.name not in ['nt', 'ce', 'dos']:
        scripts.append(os.path.join("scripts", "psyche"))

    if get_command() == "sdist" or os.name in ['nt', 'ce', 'dos']:
        scripts.append(os.path.join("scripts", "psyche.bat"))
    
    # source also gets the test script and the Makefile
    if get_command() == "sdist":
        scripts.append(os.path.join("scripts", "test.py"))
        scripts.append("Makefile")

    return scripts



# the actual setup
setup(
    # program name
    name = "psyche",
    version = "0.4.3",

    # meta information
    description = "Scheme Interpreter written in Python",
    author = "Yigal Duppen",
    author_email = "yduppen@xs4all.nl",
    url = "http://www.xs4all.nl/~yduppen/psyche",
    license = "GPL", 
    long_description = """Psyche is a Scheme interpreter written in Python

It is almost R5RS compliant and makes it possible to embed most
Scheme scripts within Python. Psyche can easily be extended with
Python functions.
""",
    platforms = ['all'],

    # source structure
    packages = get_packages(),
    package_dir = {'': 'src'},
    scripts = get_scripts(),

    data_files = [(os.path.join(get_doc_root(), "manual"), get_manuals()),
                  (get_doc_root(), get_project_docs())],

    )





