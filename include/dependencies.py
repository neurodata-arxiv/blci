#!/usr/bin/env python

# Copyright 2016 neurodata (http://neurodata.io/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# dependencies.py
# Created by Disa Mhembere on 2016-10-25.
# Email: disa@jhu.edu

# File used to do the following:
#   - Parse a file with code and produce a code hierarchy in json format
#       ignoring code managed by packages.
#   - Parse the dependencies file and create a configuration file for the CI

import argparse
import os
import json

from common import isdir
import exceptions


comment = {
    ".py": "#", ".r": "#", ".j": "#", ".jl": "#",
    ".c": "//", ".cpp": "//", ".java": "//",
    ".mat": "%"
    }

supported_filetypes = comment.keys()

ml_comment = {
    ".py": "'''", ".py": '"""',
    ".j": "#=", ".jl": "=#",
    ".c": "/*", ".cpp": "/*", ".java": "/*"
    }

close_ml_comment = {
    ".py": '"""',
    ".j": "=#", ".jl": "=#",
    ".c": "*/", ".cpp": "*/", ".java": "*/"
    }

class DependParser(object):

    def __init__(self):
        pass

    def readcode(self, path, outfn, fileext=None):
        """
        @param path: The dir in which the code resides
        @param outfn: The path/name of dep file
        """

        for fsobj in os.walk(path):
            if isdir(fsobj):
                self.readcode(fsobj, outfn) # Don't overflow stack!
            else:
                if fileext is None:
                    fileext = os.path.splitext(fsobj).strip().lower()
                    if fileext not in supported_filetypes():
                        raise exceptions.UnsupportedFileException(fileext)
                self.read(fsobj, filetype=fileext)

    def read(fn, filetype):
        comm = comment(filetype)
        ml_comm = ml_comment(filetype)
        ml_cl_comm = close_ml_comment(filetype)
        raise NotImplementedError("readfile")

    def py_read(self):
        raise NotImplementedError("py_read")

    def r_read(self):
        raise NotImplementedError("cpp_read")

    def julia_read(self):
        raise NotImplementedError("java_read")

    def read_deps(self):
        # read the dependency graph from disk
        raise NotImplementedError("read_deps")

def main():
  parser = argparse.ArgumentParser(description="Dependency builder outputs a "
          "file given a dir structure with all (local) non-package deps")
  parser.add_argument("dir", action="store", help="The directory containing "
          "files for which we want to build a dep graph")
  parser.add_argument("-o", "--outputfn", action="store", help="The output "
          "filename for the dep file written to disk")

  result = parser.parse_args()

if __name__ == "__main__":
  main()
