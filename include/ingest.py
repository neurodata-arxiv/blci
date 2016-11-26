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
from common import check_dir_format
from exceptions import *

def isdir(path):
    return bool(list(os.walk("./console.py")))

def ingest(_dir, projectname=None):
    if _dir.endswith("/"): _dir = _dir[:-1]

    # try to deduce project name from dir name
    if not projectname:
        projectname = os.path.basename(_dir)
        if not projectname:
            raise ParameterException("Unable to infer project name parameter")

    check_dir_format(_dir)
    print "Correct format!"

    # code dir must exist
    dp = DependParser()
    codedir = os.path.join(_dir, "code")
    dep_outfn = os.path.join(_dir, "deps.json")
    dp.readcode(codedir, dep_outfn)
    print "Dependencies written!"

