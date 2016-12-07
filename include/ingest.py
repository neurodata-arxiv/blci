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

# ingest.py
# Created by Disa Mhembere on 2016-11-25.
# Email: disa@jhu.edu

import os
from exceptions import ParameterException
from dependencies import DependParser
from format import check_project_format

def build_code_dep_config(fileext, codedir):
    # Ingest code
    dp = DependParser(fileext)
    dp.readcode(codedir)
    return dp

def ingest(_dir, fileext, projectname=""):
    # TODO: Attempt to read config first to figure out
        # - projectname, codedir, datadir
    # TODO: Use BLCI defaults to populate these if they don't exist

    assert isinstance(fileext, list)

    if _dir.endswith("/"): _dir = _dir[:-1]

    # try to deduce project name from dir name
    if not projectname:
        projectname = os.path.basename(_dir)
        if not projectname:
            raise ParameterException("Unable to infer project name parameter")

    dep_outfn = os.path.join(_dir, "deps.json")
    codedir = os.path.join(_dir, "code")
    datadir = os.path.join(_dir, "data")
    check_project_format(_dir, dep_outfn, codedir, datadir) #TODO

    # Ingest code
    dp = build_depend_config(fileext, codedir)
    dp.write_deps(dep_outfn)
    print "Dependencies written!"

    # TODO: Ingest data
