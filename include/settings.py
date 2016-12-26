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

# settings.py
# Created by Disa Mhembere on 2016-12-09.
# Email: disa@jhu.edu

# Constants
""" Default file names we expect to exsit """
BL_DEFAULT_DEPS_FN = "blci.deps"
BL_DEFAULT_CONFIG_FN = "blci.yml"
BASE_CI_CONFIG_FN = ".travis.yml"
GIT_IGNORE_FN = ".gitignore"

""" File types read by default by language """
BL_READ_DEFAULTS = {
        "python": [".py", ".ipynb"],
        "julia": [".j", ".jl"],
        "cpp": [".cpp", ".c", ".h", ".hpp"],
        "c": [".c", ".h"],
        "r": [".r"],
        "java": [".java"],
        "mat": [".m"]
        }

# Define settings constants
BL_NAME = "name"
BL_LANGUAGE = "language"
BL_VERSION = "version"
BL_IGNORE = "ignore"
BL_NTHREAD = "nthread"
BL_READ = "read"
BL_WRITE = "write"
BL_CODE_LOCATION = "code_loc"
BL_DATA_LOCATION = "data_loc"
BL_DATA_DEP = "data_dep"
BL_SCRIPT = "script"
BL_PATH = "path"
BL_INSTALL = "install"
BL_CREDS = "credentials" # Same for github and travis
BL_DESCRIPTION = "description"

""" Language version defaults """
BL_DEFAULT_LANG_VERSION = {
        "python": 2.7,
        "julia": 0.4,
        "cpp": "c++11",
        "c": "c11",
        "r": 3,
        "java": 7,
        "mat" : 7
        }

""" Language version defaults """
BL_DEFAULT_READ = {
        "python": [".py", ".pyx"],
        "julia": [".j"],
        "cpp": [".c", ".cpp", ".cxx", ".h", "hpp"],
        "c": [".c", ".h"],
        "r": [".r"],
        "java": [".java"],
        "mat" : [".m"]
        }

""" Configuration default values """
BL_DEFAULT_NTHREAD = 1
BL_DEFAULT_VERSION = ""
BL_DEFAULT_CODE_LOCATION = ["code"]
BL_DEFAULT_DATA_LOCATION = ["data"]
BL_DEFAULT_IGNORE = [".*", ".pyc", ".d", ".o", ".javac", ".rbin", ".mat"]
BL_DEFAULT_DATA_DEP = {"read": {}, "write": {}}
BL_DEFAULT_DESCRIPTION = "A BrainLab Continuous Integration repo"
BL_DEFAULT_CREDS = ".credentials"

""" These are all the settings/parameters blci supports """
BL_SETTINGS = {
        BL_NAME,
        BL_LANGUAGE,
        BL_VERSION,
        BL_IGNORE,
        BL_NTHREAD,
        BL_READ,
        BL_CODE_LOCATION,
        BL_DATA_LOCATION,
        BL_DATA_DEP,
        BL_SCRIPT,
        BL_PATH,
        BL_INSTALL,
        BL_DESCRIPTION,
        BL_CREDS
        }

""" These are the default parameters blci uses """
BL_DEFAULTS = {
        BL_NTHREAD: BL_DEFAULT_NTHREAD,
        BL_VERSION : BL_DEFAULT_VERSION,
        BL_IGNORE : BL_DEFAULT_IGNORE,
        BL_CODE_LOCATION : BL_DEFAULT_CODE_LOCATION,
        BL_DATA_LOCATION : BL_DEFAULT_DATA_LOCATION,
        BL_PATH : [],
        BL_DATA_DEP : BL_DEFAULT_DATA_DEP,
        BL_INSTALL : "",
        BL_DESCRIPTION : BL_DEFAULT_DESCRIPTION,
        BL_CREDS : BL_DEFAULT_CREDS,
        BL_SCRIPT : "",
        BL_NAME : ""
        }

BL_REQUIRED = set.symmetric_difference(BL_SETTINGS,
    set((BL_DEFAULTS.keys())))

""" Separates Base CI (Travis) configurations from BLCI specific ones """
BL_SPECIFIC_CONFS = {
        BL_NAME,
        BL_IGNORE,
        BL_NTHREAD,
        BL_READ,
        BL_CODE_LOCATION,
        BL_DATA_LOCATION,
        BL_DATA_DEP,
        BL_PATH,
        BL_CREDS
        }
