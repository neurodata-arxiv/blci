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

import argparse
import os
import json

from common import ls_r
from common import get_ext
from common import localize
from bl_exceptions import *
from os.path import dirname
from settings import *

# Inline comment
comment = {
        ".py": "#", ".ipynb":"#", ".r": "#", ".j": "#", ".jl": "#",
        ".c": "//", ".cpp": "//", ".java": "//",
        ".mat": "%"
    }

supported_fileexts = comment.keys()
supported_fileexts.append(".json") # read made deps

# NOTE: We use " " as a placeholder for languages with no multi-line comment
#   since all lines are stripped
ml_comment = {
        ".py": "'''", ".ipynb": '"""',
        ".j": "#=", ".jl": "=#",
        ".r": " ",
        ".c": "/*", ".cpp": "/*", ".java": "/*"
    }

# Closing multi-line comment
close_ml_comment = {
        ".py": '"""', ".ipynb": '"""',
        ".j": "=#", ".jl": "=#",
        ".r": " ",
        ".c": "*/", ".cpp": "*/", ".java": "*/"
    }

# How we figure out if the
module_keywords = {
        ".py": ["import", "from"], ".ipynb": ["import", "from"],
        ".j": ["using", "import", "importall"],
        ".r": ["source"],
        ".c": ["#include"], ".cpp": ["#include"],
        "java": ["import"],
        }

class DependParser(object):
    def __init__(self, fileext, projecthome):
        """
        Object used to do the following:
            - Parse a file with code and produce a code hierarchy in json format
               ignoring code managed by package managers.
           - Parse the dependencies file and create a configuration file
               for the CI.

        **Positional Arguments:**

        fileext:
            - The file extensions that we will inspect for deps.
        projecthome:
            - The root directory of where the blci project is.
        """

        assert isinstance(fileext, list), "Accepted file extensions must be a "
        "list"
        self.fileext = fileext
        self.projecthome = projecthome

        # key: is file, v: list(all files that depend on the file)
        self.__map__ = {}

    def readcode(self, code_loc):
        """
        Given a list of files in any supported languge, parse through each one.

        **Positional Arguments:**

        code_loc:
            - The dir in which the code resides
        """

        assert isinstance(code_loc, list), "Code locations must be a list"

        files = []
        for path in code_loc:
            files.extend(ls_r(path, self.fileext))

        for ext in self.fileext:
            if ext not in supported_fileexts:
                raise UnsupportedFileException(ext)

        # TODO: ||ize
        for fn in files:
            print "Reading {} ...".format(fn)
            self.read(fn)

    def __put_dep__(self, mod, importer):
        """
        Add a dependency to the dep file.

        **Positional Arguments:**

        mod:
            - is the file that is being imported/included
        importer:
            - the file that includes/imports `mod`
        """
        mod = localize(self.projecthome, mod)
        importer = localize(self.projecthome, importer)

        if self.__map__.has_key(mod):
            self.__map__[mod].append(importer)
        else:
            self.__map__[mod] = [importer]

    def __build_map__(self, fn, modlines):
        """
        Determine if import is local, if it is: add it to the depenedency
        struct. This method calls the appropriate method for the language based
        on the file extension.

        **Positional Arguments:**

        fn:
            - The file name to be added to the dependency struct
        modlines:
            - The lines containing "import" module statements
        """
        if get_ext(fn).startswith(".py"):
            self.__python_build_map__(fn, modlines)
        else:
            raise NotImplementedError("File type {} not yet "
                    "supported".format(get_ext(fn)))

    def __python_build_map__(self, fn, modlines):
        """
        Python has 3 patters for includes:
        1. import module[.nested-module]
        2. from module[.nested-module].script import function
        3. from module[.nested-module] import script

        **Positional Arguments:**

        fn:
            - The file name to be added to the dependency struct
        modlines:
            - The lines containing "import" module statements
        """

        base_dir = dirname(fn)
        files = ls_r(base_dir, self.fileext)

        for line in modlines:
            split_line = line.split()
            # 1. & 2.
            mod = os.path.join(base_dir, *split_line[1].split("."))+".py"
            if not (os.path.isfile(mod)) and line.startswith("from"):
                # 3.
                if len(split_line) != 4:
                    raise ParsingException("Cannot part 'from' "
                            "import: {} in {}. Please conform to PEP8 import "
                            "conventions".format(line, fn))

                mod = os.path.join(base_dir,
                        *(split_line[1]+"."+split_line[3]).split("."))+".py"
            if not (os.path.isfile(mod)): continue
            # else
            self.__put_dep__(mod, fn)

    def __json_build_map__(self, fn):
        """
        Build the dependency struct from a file in json format

        ** Positional Arguments **

        fn:
            - The file path on disk
        """

        with open(fn, "rb") as f:
            if len(self.__map__) == 0:
                self.__map__ = json.load(f)
            else:
                ondisk = json.load(f)
                for k, v in ondisk.iteritems():
                    if self.__map__.has_key(k): # Case we have the key
                        for deps in v: # v is a list
                            if deps not in self.__map__[k]:
                                self.__map__[k].append(deps)
                    else: # Case we don't have the key
                        self.__map__[k] = v

    def __r_build_map__(self):
        raise NotImplementedError("R read")

    def __julia_build_map__(self):
        raise NotImplementedError("julia read")

    def read_deps(self):
        # read the dependency graph from disk
        raise NotImplementedError("read_deps")


    def __check_local_mod__(self, fn, dep_encoding_lines):
        pass

    def read(self, fn):
        """
        Generic code reader to extract deps from a file. NOTE: The
            file extension is very important as it determines A LOT!

        ** Positional Arguments **

        fn:
            - The filename to be read
        """
        ext = get_ext(fn)
        if ext not in supported_fileexts:
            raise NotImplementedError("Cannot read file type "
                    "{} yet".format(ext))

        if ext == ".json":
            self.__json_build_map__(fn)
            return

        self.comm = comment[ext]
        self.ml_comm = ml_comment[ext]
        self.ml_cl_comm = close_ml_comment[ext]

        with open(fn, "rb") as f:
            dep_encoding_lines = []

            ml_comm_flag = False
            lineno = -1
            while True:
                lineno += 1
                line = f.readline().strip()
                if not line: break
                if line.startswith(self.comm):
                    continue
                elif not ml_comm_flag and line.startswith(self.ml_comm):
                    ml_comm_flag = True
                    continue
                elif line.startswith(self.ml_cl_comm) or \
                        line.endswith(self.ml_cl_comm):
                    if not ml_comm_flag: raise ParsingException("Multiline "
                        "comment closing block without opening block line {}: "
                            "{}".format(lineno, fn))
                    ml_comm_flag = False
                # look for import statements
                for kywd in module_keywords[ext]:
                    if line.startswith(kywd): dep_encoding_lines.append(line)

            if (dep_encoding_lines): # Ignore empty dep files
                self.__build_map__(fn, dep_encoding_lines)

    def write(self, outfn=""):
        """
        Write dependency struct to disk

        ** Positional Arguments **

        outfn:
            - The path/name of dep fileext
        """

        print "Writing dependency file '{}' ..".format(outfn)
        with open(outfn, "wb") as f:
            json.dump(self.__map__, f)

    def __repr__(self):
        return str(self.__map__)

    def __eq__(self, other):
        return self.__map__ == other.__map__

    def __ne__(self, other):
        return not self.__eq__(other)
