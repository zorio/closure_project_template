# -*- coding: utf-8 -*-

import os
import subprocess
import urllib
import zipfile


CLOSURE_DIR = "closure-project"

CLOSURE_COMPILER_URL = \
    "http://closure-compiler.googlecode.com/files/compiler-latest.zip"
CLOSURE_COMPILER_DIRNAME = "closure-compiler"
CLOSURE_COMPILER_FILENAME = CLOSURE_COMPILER_DIRNAME + ".zip"

CLOSURE_LIBRARY_DIRNAME = "closure-library"
CLOSURE_LIBRARY_COMMAND = \
    "svn checkout http://closure-library.googlecode.com/svn/trunk/ " +\
    CLOSURE_LIBRARY_DIRNAME

CLOSURE_TEMPLATES_URL = \
    "http://closure-templates.googlecode.com/files/closure-templates-for-javascript-latest.zip"
CLOSURE_TEMPLATES_DIRNAME = "closure-templates"
CLOSURE_TEMPLATES_FILENAME = CLOSURE_TEMPLATES_DIRNAME + ".zip"

CLOSURE_STYLESHEETS_URL = \
    "https://closure-stylesheets.googlecode.com/files/closure-stylesheets-20111230.jar"
CLOSURE_STYLESHEETS_DIRNAME = "closure-stylesheets"
CLOSURE_STYLESHEETS_FILENAME = CLOSURE_STYLESHEETS_DIRNAME + ".jar"


def update_all():
  make_closure_dir()
  get_closure_library()
  get_closure_compiler()
  get_closure_templates()
  get_closure_stylesheets()

def make_closure_dir():
  os.path.exists(CLOSURE_DIR) or os.mkdir(CLOSURE_DIR)
  os.chdir(CLOSURE_DIR)

def get_closure_library():
  print "Download Closure library"
  if os.path.exists(CLOSURE_LIBRARY_DIRNAME):
    os.chdir(CLOSURE_LIBRARY_DIRNAME)
    print "svn upate"
    subprocess.call("svn update", shell=True)
    os.chdir("..")
  else:
    print CLOSURE_LIBRARY_COMMAND
    subprocess.call(CLOSURE_LIBRARY_COMMAND, shell=True)  

def get_closure_compiler():
  print "Download Closure Compiler"
  urllib.urlretrieve(CLOSURE_COMPILER_URL, CLOSURE_COMPILER_FILENAME)
  zipfile.ZipFile(CLOSURE_COMPILER_FILENAME).extractall(CLOSURE_COMPILER_DIRNAME)

def get_closure_templates():
  print "Download Closure Template"
  urllib.urlretrieve(CLOSURE_TEMPLATES_URL, CLOSURE_TEMPLATES_FILENAME)
  zipfile.ZipFile(CLOSURE_TEMPLATES_FILENAME).extractall(CLOSURE_TEMPLATES_DIRNAME)

def get_closure_stylesheets():
  print "Download Closure Stylesheets"
  if not os.path.exists(CLOSURE_STYLESHEETS_DIRNAME):
    os.mkdir(CLOSURE_STYLESHEETS_DIRNAME)
  urllib.urlretrieve(CLOSURE_STYLESHEETS_URL,
      os.path.join(CLOSURE_STYLESHEETS_DIRNAME, CLOSURE_STYLESHEETS_FILENAME))

if __name__ == "__main__":
  update_all()
