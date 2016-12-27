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
from shutil import rmtree
import yaml
from git import Repo

from bl_exceptions import FileNotFoundException

def ls_r(path, fileext):
    """
    Works like a shells `ls -r` syscall, but searches with a given file
    extensions (`fileext`) in mind

    **Positional Arguments:**

    path:
        - The base path from where we traverse the directory structure
    fileext:
        - The file extensionS we care about when we traverse
    """

    matches = []
    for ext in fileext:
        for root, dirnames, fns in os.walk(path):
            for fn in fnmatch.filter(fns, "*"+ext):
                matches.append(os.path.join(root, fn))
    return matches

def get_ext(path):
    """
    Given a path return the file extension.

    **Positional Arguments:**

    path: The file whose path we assess
    """
    return os.path.splitext(path)[1]

def localize(base, path):
    """
    Returns a localized path with respect to a base path. For instance if we
    have base=/home/floki/ and path=/home/floki/ragnar/foo.txt, localize will
    return ragnar/foo.txt

    **Positional Arguments:**

    base:
        - The base path from which we wish to localize a file path
    path:
        - The path that we aim to localize
    """

    base_len = len(os.path.abspath(base))
    absolute_path = os.path.abspath(path)
    return absolute_path[base_len+1:]

def is_git_branch(branchname, _dir="./"):
    """
    Does the the branch specified exist in the repo

    **Positional Arguments:**

    branchname:
        - The git branch you wish to evaluate existence of

    **Optional Arguments:**

        _dir:
            - The dir that is a git repo
    """

    if not is_git_repo(_dir): return False

    repo = Repo(_dir)
    for branch in repo.refs:
        if branchname == branch.name:
            return True
    return False

def is_git_repo(path):
    """
    Rudimentary tests for if I have a git repo. Simply look for .git directory

    **Positional Arguments:**

    path:
        - The path that we are assessing
    """

    return os.path.exists(os.path.join(path, ".git")) and \
            os.path.isdir(os.path.join(path, ".git"))

def write_yml(yamldict, fn, verbose=False):
    """
    Write a YAML formatted file to disk.

    **Positional Arguments:**

    yamldict:
        - The python dictionary object we will write as YAML
    fn:
        - The file name we wish to use

    **Optional Arguments:**

    verbose:
        - Prints debug information if true
    """

    with open(fn, "wb") as f:
        yaml.dump(yamldict, f, default_flow_style=False)

    if verbose:
        print "Write yml {} ..".format(f)

def read_yml(fn):
    """
    Read a YAML formatted file in a python dictionary

    **Positional Arguments:**

    fn:
        - The file path on disk
    """

    if not os.path.exists(fn):
        raise FileNotFoundException("{fn}".format(fn))

    with open(fn, "rb") as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as _err:
            sys.stderr.write("Config load ERROR:" + _err + "\n")
            exit(911)

def read_token(credentials_fn):
    """
    Read a github token from a file that has it stored as plain text

    **Positional Arguments:**

    credentials_fn:
        - An existing path to a file containing credentials
    """

    if not credentials_fn:
        raise FileNotFoundException(credentials_fn)

    try:
        with open(credentials_fn, "rb") as f:
            token = f.readline().strip()
    except Exception, msg:
        raise ParameterException("Problem with credentials file " + msg)

    return token

def delete(path, verbose=False):
    """
    Delete a file, or directory

    **Positional Arguments:**

    path:
        - The path to the file system object to be deleted

    **Optional Arguments:**

    verbose:
        - Print debug messages when actions are taken
    """

    if (os.path.exists(path)):
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)

        if verbose:
            print "Deleted '{}' ...".format(path)
    else:
        if verbose:
            print "No such path '{}' ...".format(path)
