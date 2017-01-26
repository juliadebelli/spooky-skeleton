from nose2.tools.decorators import with_teardown
import os, shutil
import skeleton

def setup():
  pass

def teardown():
  shutil.rmtree("test", ignore_errors=True)

def test_has_valid_dir_structure():
  """Check if the specified dir structure is valid"""
  def recurse_contents(contents):
    if contents is None:
      return None
    
    else:
      for key, value in contents.items():
        assert(isinstance(key, str))
        
        if value is None:
          return None
        elif "dir" in value:
          recurse_contents(value["dir"])
        elif "file" in value:
          assert(value["file"] is None or isinstance(value["file"], str) or callable(value["file"]))
          if callable(value["file"]):
            generator = value["file"]
            assert(isinstance(generator("test"), str))
        else:
          raise Exception("""
          Every entry in the directory structure must be
          either a directory or a file.
          """)

  recurse_contents(skeleton.dir_structure)

@with_teardown(teardown)
def test_creates_toplevel_dir_structure():
  """Check if the proper top-level directory structure is created."""

  shutil.rmtree("test", ignore_errors = True)
  
  skeleton.create_dir_structure("test")
  os.chdir("test")

  for key, value in skeleton.dir_structure.items():
    name = skeleton.replace_project_sigil(key, "test")
    absolute_path = os.path.abspath(name)
    
    if "dir" in value:
      assert(os.path.isdir(absolute_path))
    elif "file" in value:
      assert(os.path.isfile(absolute_path))
    else:
      raise Exception("""
      Every entry in the directory structure must be
      either a directory or a file.
      """)

  os.chdir("..")

@with_teardown(teardown)
def test_creates_subdirs():
  """Check if the proper directory structure is created."""
  
  def check_file(name, contents):
    if contents is None:
      return None
    else:
      with open(name, "r") as the_file:
        data = the_file.read()
        if not callable(contents):
          assert(data == contents)
        else:
          assert(data == contents("test"))

  def recurse_contents(contents):
    if contents is None:
      assert(not os.listdir(os.path.curdir))
    else:
      for key, value in contents.items():
        name = skeleton.replace_project_sigil(key, "test")
        absolute_path = os.path.abspath(name)
        
        if value is None:
          return None
        
        elif "dir" in value:
          assert(os.path.isdir(absolute_path))
          os.chdir(name)
          recurse_contents(value["dir"])
          os.chdir("..")
        
        elif "file" in value:
          assert(os.path.isfile(absolute_path))
          check_file(name, value["file"])

  shutil.rmtree("test", ignore_errors = True)
  
  skeleton.create_dir_structure("test")
  os.chdir("test")
  recurse_contents(skeleton.dir_structure)
  os.chdir("..")
