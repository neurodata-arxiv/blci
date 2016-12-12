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
from bl_exceptions import FileNotFoundException

def ls_r(path, fileext):
    matches = []
    for ext in fileext:
        for root, dirnames, fns in os.walk(path):
            for fn in fnmatch.filter(fns, "*"+ext):
                matches.append(os.path.join(root, fn))
    return matches

def get_ext(path):
    return os.path.splitext(path)[1]

def localize(base, path):
    """ Returns a localized path with respect to a base path """
    base_len = len(os.path.abspath(base))
    absolute_path = os.path.abspath(path)
    return absolute_path[base_len+1:]

def is_git_branch(branchname, _dir="./"):
    from git import Repo
    repo = Repo(_dir)
    for branch in repo.refs:
        if branchname == branch.name:
            return True
    return False

def write_yml(yamldict, fn, verbose=False):
    with open(fn, "wb") as f:
        yaml.dump(yamldict, f, default_flow_style=False)

    if verbose:
        print "Write yml {} ..".format(f)

def read_yml(fn):
    if not os.path.exists(fn):
        raise FileNotFoundException("{fn}".format(fn))

    with open(fn, "rb") as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as _err:
            sys.stderr.write("Config load ERROR:" + _err + "\n")
            exit(911)
