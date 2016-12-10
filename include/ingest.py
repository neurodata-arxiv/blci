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

import sys
from settings import *
import exceptions
from git import Repo

DEFAULT_INGEST_MESSAGE = "Initial project {} ingest"

def morph_base_CI(blci_conf, base_ci_conf):
    """
    Given a user defined project blci configuration file and the CI
    configuration file in the root of blci, create a new a config that encodes
    the following:
    - User defined tests
    - Triggers for code and data dependencies for any code or data change that
    will occur from an `update` action

    **Positional Arguments:**

    blci_conf:
        - User defined blci configuration file
        - Base CI configuration file defined by blci
    """
    return {} # FIXME

def ingest(projecthome):
    """
    Add a new project as a blci repo

    **Positional Arguments:**

        projecthome:
            - The root directory of where the blci project is.
    """

    conf = config(os.path.join(projecthome, BL_DEFAULT_CONFIG_FN),
            silent_fail=False)
    if is_git_branch(conf.get(BL_NAME)):
        raise exceptions.ParameterException("Repo {} is already tracked "
                "by blci in branch {}".format(projecthome, conf.get(BL_NAME)))

    repo = Repo(projecthome)
    Git = repo.git(work_tree=projecthome)

    Git.branch(conf.get(BL_NAME)) # Create new branch with repo name
    Git.checkout(conf.get(BL_NAME)) # Hop into that branch

    # Now from the new branch
    base_conf_fn = os.path.join(conf.get(BL_ROOT), BASE_CI_CONFIG_FN)
    base_conf = morph_base_CI(conf, base_conf_fn)

    write_yml(base_conf, base_conf_fn, verbose=True)

    # Add the config file
    Git.add(".") # Add all
    Git.commit("a", "m", DEFAULT_INGEST_MESSAGE.format(conf.get(BL_NAME)))
    Git.push("origin", "{}".format(conf.get(BL_NAME)))
