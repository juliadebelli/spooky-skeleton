import os, sys

usage_message = """
Usage:
  
  python skeleton.py <name>

  * Creates a directory named <name> and a default 
    directory structure for a Python project under it.
"""


dir_exists_message = """
Error:

  Directory {name} already exists.
  If you wish to use directory {name}, delete the existing directory.
"""

project_config = """config = {{
  "description": "",
  "author": "",
  "url": "",
  "download_url": ""
  "author_email": ""
  "version": 0.1.0,
  "install_requires": ["nose2"],
  "packages": ["{project_name}"],
  "scripts": [],
  "name": "{project_name}"
}}

setup(**config)
"""

tests = """from nose2.tools import *
import {project_name}

def test_basic:
  assert(2+2 == 4)
"""

requirements = "nose2\n"

makefile = "default: ;\n"

project_sigil = "$PROJECT"

def make_project_config(name):
  return project_config.format(project_name=name)

def make_test(name):
  return tests.format(project_name=name)

dir_structure = {
  "$PROJECT": {"dir": {
    "__init__.py": {"file": None}
  }},
  "tests": {"dir": {
    "__init__.py": {"file": None},
    "test_$PROJECT.py": {"file": make_test}
  }},
  "bin": {"dir": None},
  "docs": {"dir": None},
  "requirements.txt": {"file": requirements},
  "setup.py": {"file": make_project_config},
  "Makefile": {"file": makefile}
}

def replace_project_sigil(string, project_name):
  return string.replace(project_sigil, project_name)

def make_empty_file(name):
  open(name, 'w').close()

def make_file_with_contents(name, string):
  with open(name, 'w') as the_file:
    the_file.write(string)

def create_subdirs(project_name):
  def recurse_contents(contents):
    if contents != None:
      for key, value in contents.items():
        name = replace_project_sigil(key, project_name)
    
        if "dir" in value:
          os.mkdir(name)
          if value["dir"] != None:
            os.chdir(name)
            recurse_contents(value["dir"])
            os.chdir("..")
        
        elif "file" in value:
          if value["file"] is None:
            make_empty_file(name)
          elif callable(value["file"]):
            make_file_with_contents(name, value["file"](project_name))
          else:
            make_file_with_contents(name, value["file"])

  recurse_contents(dir_structure)
      

def create_dir_structure(name):
  absolute_path = os.path.abspath(name)
  
  if os.path.exists(absolute_path):
    error = make_dir_exists_message(name)
    error_message(error)
    sys.exit(1)

  else:
    os.mkdir(name)
    os.chdir(os.path.abspath(name))
    create_subdirs(name)
    os.chdir("..")

    
def error_message(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

  
def make_dir_exists_message(dirname):
  return dir_exists_message.format(name=dirname)


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print(usage_message)    
  else:
    create_dir_structure(sys.argv[1])
