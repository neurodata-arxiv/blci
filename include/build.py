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

# build.py
# Created by Disa Mhembere on 2016-12-21.
# Email: disa@jhu.edu

from github import Github
from git import Repo
from settings import *
from subprocess import check_output
from common import read_token
from os.path import join

def trigger_build(conf, projecthome):
    """
    Hack to trigger a build.
    TODO: Remove the push to repo

    **Positional Arguments:**

    conf:
        - A BLCI configuration :class:`~include.config.config` object

    projecthome:
        - root directory of the project
    """
    # Make a change
    git_ignore_fn = join(projecthome, GIT_IGNORE_FN)

    lines = []
    with open(git_ignore_fn, "rb") as f:
        lines.extend(f.readlines())

    if not lines[-1].strip(): # Already ends in newline
        with open(git_ignore_fn, "wb") as f:
            f.writelines(lines[:-1]) # Get rid of newline
    else:
        with open(git_ignore_fn, "ab") as f:
            f.seek(f.tell())
            f.write("\n")

    # Trigger a build
    repo = Repo(projecthome)
    Git = repo.git(work_tree=projecthome)
    Git.checkout(conf.get(BL_NAME)) # Ensure correct branch
    Git.commit("-am", "BLCI: Trigger build")
    Git.push("origin", conf.get(BL_NAME))

    # FIXME
    # Attempt to use Travis-CI restful api. Issue with token?
    # https://docs.travis-ci.com/user/triggering-builds

    # body = '{"request": {"branch": "%s"}}' % conf.get(BL_NAME)
    # token = read_token(conf.get(BL_CREDS))
    # g = Github(token)
    # output = check_output(["curl", "-s", "-X", "POST",
        # "-H", '"Content-Type: application/json"',
	# "-H", '"Accept: application/json"',
	# "-H", '"Travis-API-Version: 3"',
	# "-H", '"Authorization: token {}"'.format(token),
	# "-d", '"%s"' % body,
	# "https://api.travis-ci.org/repo/{}%2F{}/requests".format(
            # g.get_user().login, conf.get(BL_NAME))
        # ])
