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
from travispy import TravisPy

from settings import *
from bl_exceptions import ParameterException
from config import config
from common import is_git_repo, is_git_branch, read_token
from common import write_yml
from os.path import join
from build import trigger_build

def handle_gitignore(projecthome, bl_conf):
    """
    Build/update the .gitignore file and ensure that blci ignored files are
    not added to repo. Some files like the credentials file should never be
    tracked or added to the remote repo.

    **Positional Arguments:**

    bl_conf:
        - A BLCI configuration :class:`~include.config.config` object

    credentials_fn:
        - An existing path to a file containing credentials
    """

    credentials_fn = bl_conf.get(BL_CREDS)
    git_ignore_fn = join(projecthome, GIT_IGNORE_FN)

    if not os.path.exists(credentials_fn):
        raise FileNotFoundException("Cannot find file credentials file {}".
                format(join(projecthome, credentials_fn)))

    has_creds = False
    ignored = set()
    if os.path.exists(git_ignore_fn):
        with open(git_ignore_fn, "rb") as f:
            while (True):
                line = f.readline()
                if not line: break

                line = line.strip()
                ignored.add(line)
                # TODO: Account for bash regexs matching credentials_fn
                if (line == ".*" and credentials_fn.startswith(".")) \
                        or line.startswith(credentials_fn):
                    has_creds = True
                    break # No work to do

    with open(git_ignore_fn, "ab") as f:
        f.write(credentials_fn + "\n")
        for exp in bl_conf.get(BL_IGNORE):
            # TODO: Account for more advanced regexs
            bash_exp = "*"+exp if (exp.startswith(".") and exp != ".*") else exp
            if bash_exp not in ignored:
                f.write(bash_exp + "\n")

def create_remote_repo(bl_conf):
    """
    Uses user-defined configuration file to create a **public** github repo that
    is initialized using configurations supplied to the BLCI configuration file.

    **Positional Arguments:**

    bl_conf:
        - A BLCI configuration :class:`~include.config.config` object with a
            credentials entry that is a path for a file containing a string
            representing a `Github OAuth2 token
            <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`_.

    **Returns:**

    A `PyGithub Repository <http://pygithub.readthedocs.io/>`_ object.
    """

    g = Github(read_token(bl_conf.get(BL_CREDS)))
    user = g.get_user()

    return user.create_repo(bl_conf.get(BL_NAME), bl_conf.get(BL_DESCRIPTION),
           private=False, auto_init=True)

def travis_track(bl_conf):
    """
    Track a github repo using travis CI programmatically

    **Positional Arguments:**

    bl_conf:
        - A BLCI configuration :class:`~include.config.config` object
    """

    print "Tracking repo with Travis ..."
    travis = TravisPy.github_auth(read_token(bl_conf.get(BL_CREDS)))
    repo = travis.repo("{}/{}".format(
        travis.user().login, bl_conf.get(BL_NAME)))
    repo.enable() # Switch is now on

    print "Synchronizing Github and Travis ..."
    travis.user().sync()

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
        - A BLCI configuration :class:`~include.config.config` object
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
    conf = config(join(projecthome, BL_DEFAULT_CONFIG_FN),
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

    handle_gitignore(projecthome, conf)

    if new_repo:
        Git.add(projecthome)
        Git.add("-f", join(projecthome, GIT_IGNORE_FN))
        Git.commit("-m", "BLCI: Repo creating")

    # Don't have a branch already ..
    if not is_git_branch(conf.get(BL_NAME), projecthome):
        Git.branch(conf.get(BL_NAME)) # Create new branch with repo name

    # Update and ingest should be the same process
    Git.checkout(conf.get(BL_NAME)) # Hop into that branch

    # Now from the new branch
    # TODO: No need to rewrite everytime actually ..
    base_CI_conf = create_base_CI_conf(conf, Git)
    write_yml(base_CI_conf, join(projecthome, BASE_CI_CONFIG_FN), verbose=True)
    if new_repo:
        Git.add("-f", join(projecthome, BASE_CI_CONFIG_FN))

    if new_repo: # Make and add the remote
        remote_repo = create_remote_repo(conf)
        Git.remote("add", "origin", remote_repo.ssh_url) # Must have SSH

    Git.commit("-am", message) # Add all
    Git.push("origin", conf.get(BL_NAME))

    if new_repo:
        travis_track(conf)
        trigger_build(conf, projecthome)

    print "Add action successful ..."
