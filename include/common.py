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

# common.py
# Created by Disa Mhembere on 2016-11-25.
# Email: disa@jhu.edu

import os
import fnmatch

def err(err):
    return "\x1B[31mERROR: {}\x1B[0m".format(err)

def check_dir_format(_dir):
    raise FormatException("Incorrect directory format for dir "
            "'{}'".format(_dir))
    return true

def ls_r(path, fileext):
    matches = []
    for ext in fileext:
        for root, dirnames, fns in os.walk(path):
            for fn in fnmatch.filter(fns, "*"+ext):
                matches.append(os.path.join(root, fn))
    return matches

def get_ext(path):
    return os.path.splitext(path)[1]
