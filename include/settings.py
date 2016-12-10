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
BL_DEFAULT_DEPS_FN = "blci.deps"
BL_DEFAULT_CONFIG_FN = "blci.yml"
BASE_CI_CONFIG_FN = ".travis.yml"

BL_READ_DEFAULTS = {
        "python": [".py", ".ipynb"],
        "julia": [".j", ".jl"],
        "cpp": [".cpp", ".c", ".h", ".hpp"],
        "c": [".c", ".h"],
        "r": [".r"],
        "java": [".java"],
        "mat": [".m"],
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
BL_ROOT = "blci_root" # Root with respect to users project

# Define some defaults
BL_DEFAULT_NTHREAD = "nthread"
BL_DEFAULT_VERSION = ""
BL_DEFAULT_CODE_LOCATION = "code"
BL_DEFAULT_DATA_LOCATION = "data"
BL_DEFAULT_IGNORE = [".*"]
BL_DEFAULT_PATH = []

# These are all the settings/parameters blci supports
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
        BL_ROOT,
        }

# These are the default parameters blci uses
BL_DEFAULTS = {
        BL_NTHREAD: BL_DEFAULT_NTHREAD,
        BL_VERSION : BL_DEFAULT_VERSION,
        BL_IGNORE : BL_DEFAULT_IGNORE,
        BL_CODE_LOCATION : BL_DEFAULT_CODE_LOCATION,
        BL_DATA_LOCATION : BL_DEFAULT_DATA_LOCATION,
        BL_PATH : BL_DEFAULT_PATH
        }

BL_REQUIRED = set.symmetric_difference(BL_SETTINGS,
    set((BL_DEFAULTS.keys())))
