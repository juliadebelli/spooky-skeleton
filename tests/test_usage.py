from nose2.tools.decorators import with_teardown
import os, subprocess, shutil
import skeleton

def teardown():
  shutil.rmtree("test", ignore_errors="True")

def test_prints_usage_message():
  """Check calling with no arguments.

  If skeleton is called without any arguments, 
  it should print an usage string and exit."""

  skeleton_process = subprocess.Popen(["python3","skeleton.py"],
                                      stderr = subprocess.PIPE,
                                      stdout = subprocess.PIPE)

  output, errors = skeleton_process.communicate()
  return_code = skeleton_process.returncode

  assert(not errors)
  assert(return_code == 0)
  assert(output.decode("utf-8") == skeleton.usage_message + "\n")

def test_create_existing_dir():
  """Check calling with an argument when project dir exists.
  
  If the requested directory exists,
  skeleton should exit with an error message."""

  try:
    os.mkdir("test")
  except FileExistsError:
    pass

  skeleton_process = subprocess.Popen(["python3","skeleton.py", "test"],
                                      stderr = subprocess.PIPE,
                                      stdout = subprocess.PIPE)

  output, errors = skeleton_process.communicate()
  return_code = skeleton_process.returncode

  shutil.rmtree("test", ignore_errors="True")

  assert(not output)
  assert(errors.decode("utf-8")
         == skeleton.make_dir_exists_message("test") + "\n")
  assert(return_code == 1)

@with_teardown(teardown)
def test_create_new_dir():
  """Check calling with an argument when project dir does not exist.

  If the requested directory does not exist, 
  skeleton should create it and exit with no error."""

  shutil.rmtree("test", ignore_errors="True")

  skeleton_process = subprocess.Popen(["python3","skeleton.py", "test"],
                                      stderr = subprocess.PIPE,
                                      stdout = subprocess.PIPE)

  output, errors = skeleton_process.communicate()
  return_code = skeleton_process.returncode

  abspath = os.path.abspath("test")

  assert(not errors)
  assert(return_code == 0)
  assert(os.path.exists(abspath))
