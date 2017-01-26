#skeleton.py

Skeleton is a scaffolding generator I made to save time on my Python projects.
It is customized to my own preferences, but you can easily change the directory
structure it generates by editing the `dir_structure` variable in the script.

The DSL this variable uses is explained below.

##Usage

`skeleton.py <project_name>` 

This will create a directory named `project_name`, and within it, the directory
structure specified by the `dir_structure` variable.

##Directory structure DSL

The `dir_structure` variable uses a simple DSL based on Python dicts.

`dir_structure` must be a dictionary with string keys. Each key's value
must be of the form `{"dir": VALUE}` or `{"file": VALUE}`.

###Keys

Keys must be plain strings. However, if a key contains the substring `$PROJECT`,
this substring will be replaced by the project's name. This is so that,
for instance, directory names can be created based on the project's name.

###Directory values

Values of the form `{"dir": VALUE}` will result in a directory being created.
In this case, VALUE may be None or a dict with the same format as the 
top-level dict, i.e.: with keys of the form `{"dir": VALUE}` or `{"file": VALUE}`.

If VALUE is None, an empty directory will be created.

If VALUE is a dict, files and/or directories will be created within the 
new directory following the same rules as for the top-level directory.

###File values

Values of the form `{"file": VALUE}` will result in a file being created.
In this case, VALUE may be None, a string, or a function taking a single string
argument and returning a string.

If VALUE is None, an empty file will be created.

If VALUE is a string, a file will be created with the specificied string as
its content.

If VALUE is a function, it will be called with the project's name as its 
argument, and the file's contents will be set to its return value. This 
is done such that, for instance, the setup.py script can be automatically 
generated.

##License

Copyright (c) 2017 Pedro Castilho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
