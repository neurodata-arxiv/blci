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

# clean.py
# Created by Disa Mhembere on 2016-12-26.
# Email: disa@jhu.edu

import os
from os.path import join
from settings import *
from common import delete

def cleanall(projecthome, verbose=False):
    """
    Delete all BLCI configurations and metadata files

    **Positional Arguments:**

    projecthome:
        - The path to the root of the project

    **Optional Arguments:**

    verbose:
        - Print messages when actions are taken
    """

    clean_bl_config(projecthome, verbose)
    clean_dependencies(projecthome, verbose)
    clean_base_ci_config(projecthome, verbose)
    clean_git(projecthome, verbose)

def clean_bl_config(projecthome, verbose=False):
    """
    Delete BLCI configuration file

    **Positional Arguments:**

    projecthome:
        - The path to the root of the project

    **Optional Arguments:**

    verbose:
        - Print messages when actions are taken
    """

    delete(join(projecthome, BL_DEFAULT_CONFIG_FN), verbose)

def clean_dependencies(projecthome, verbose=False):
    """
    Delete BLCI dependency metadata file

    **Positional Arguments:**

    projecthome:
        - The path to the root of the project
    """

    delete(join(projecthome, BL_DEFAULT_DEPS_FN), verbose)

def clean_base_ci_config(projecthome, verbose=False):
    """
    Delete Travis-CI configuration file

    **Positional Arguments:**

    projecthome:
        - The path to the root of the project

    **Optional Arguments:**

    verbose:
        - Print messages when actions are taken
    """

    delete(join(projecthome, BASE_CI_CONFIG_FN), verbose)

def clean_git(projecthome, verbose=False):
    """
    Delete Git ignore file

    **Positional Arguments:**

    projecthome:
        - The path to the root of the project

    **Optional Arguments:**

    verbose:
        - Print messages when actions are taken
    """
    delete(join(projecthome, ".git"))
    delete(join(projecthome, GIT_IGNORE_FN))
