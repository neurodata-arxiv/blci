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

import sys, os
from git import Repo
from github import Github

from settings import *
from bl_exceptions import ParameterException
from config import config
from common import is_git_repo
from common import is_git_branch

def create_git_repo(bl_conf):
    """
    Uses user-defined configuration file to create a **public** github repo that
    is initialized using configurations supplied to the BLCI configuration file.

    **Positional Arguments:**

    bl_conf:
        - A BLCI configuration (`config.config`) object

    **Returns:**

    A [PyGithub](http://pygithub.readthedocs.io/) `Repo` object
    """

    if not settings_fn:
        raise FileNotFoundException(settings_fn)

    creds = read_yml(credentials_fn)
    g = Github(creds["email"], creds["passwd"])
    user = g.get_user()

    return user.create_repo(bl_conf.get(BL_NAME), bl_conf.get(BL_DESCRIPTION),
           private=False, auto_init=True)

def travis_track(bl_conf):
    """
    Track a github repo using travis CI programmatically

    **Positional Arguments:**

    bl_conf:
        - A BLCI configuration (`config.config`) object
    """
    endpoint = "https://api.travis-ci.org"

    # TODO: For now we assume the user is using a repo in their own account and
    #   an exterior organization

def create_base_CI_conf(bl_conf, Git):
    """
    Given a user defined project blci configuration file and the CI
    configuration file in the root of blci, create a new a config that encodes
    the following:
    - User defined tests
    - Triggers for code and data dependencies for any code or data change that
    will occur from an `update` action

    **Positional Arguments:**

    bl_conf:
        - User defined blci configuration file
        - Base CI configuration file defined by blci
    Git:
        - Git repo object from Gitpython package
    """
    base_CI_conf = {}
    for setting, val in bl_conf.getall().iteritems():
        if setting not in BL_SPECIFIC_CONFS:
            base_CI_conf[setting] = val

    # Which branch to work with
    base_CI_conf["branches"] = { "only": bl_conf.get(BL_NAME) }

    diff = Git.diff()
    if diff: # Things have changed
        # TODO: Add webhooky things
        pass

    return base_CI_conf

def add(projecthome, message):
    """
    Add or update a blci repo

    **Positional Arguments:**

        projecthome:
            - The root directory of where the blci project is.
    """
    projecthome = os.path.abspath(projecthome)
    conf = config(os.path.join(projecthome, BL_DEFAULT_CONFIG_FN),
            silent_fail=False)

    new_repo = False # is this a new blci repo or not
    if not is_git_repo(projecthome):
        repo = Repo.init(projecthome, bare=False)
        new_repo = True
    else:
        repo = Repo(projecthome)

    Git = repo.git(work_tree=projecthome)
    if not Git.branch(): # We may have a repo with no commits ...
        new_repo = True

    if new_repo:
        Git.add(projecthome)
        Git.commit("-m", "BLCI: Repo creating")

    # Don't have a branch already ..
    if not is_git_branch(conf.get(BL_NAME), projecthome):
        Git.branch(conf.get(BL_NAME)) # Create new branch with repo name

    # Update and ingest should be the same process
    Git.checkout(conf.get(BL_NAME)) # Hop into that branch

    # Now from the new branch
    # TODO: No need to rewrite everytime actually ..
    base_CI_conf = create_base_CI_conf(conf, Git)
    write_yml(base_CI_conf, BASE_CI_CONFIG_FN, verbose=True)

    # Add the config file
    Git.add(projecthome) # Add all
    if not message:
        if new_repo:
            message = "BLCI: Initial commit"
        else:
            message = "BLCI: Generic commit message"

    Git.commit("-am", message)
    Git.push("origin", "{}".format(conf.get(BL_NAME)))

    if new_repo:
        Git.remote("add", "origin", origin_url)
        # TODO: Add code push to
