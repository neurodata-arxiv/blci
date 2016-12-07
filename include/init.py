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

# init.py
# Created by Disa Mhembere on 2016-12-05.
# Email: disa@jhu.edu

from include.config import config
import os
from ingest import build_code_dep_config

def init(fileext, projecthome, code_dir=[],
        data_loc=[], overwrite=False, bare=False):
    """
    @param projecthome: the root dir of the project
    @param data_loc: the location(s) of where the data resides
    @param: bare means ignore the current config and write a new one
    """
    c = None
    if bare:
        c = config()
    else:
        c = config(os.path.join(projecthome, "blci.yml"))

    # Build code dependencies
    dp = build_code_dep_config(fileext)


    # Build data dependencies

    c.build_data_dep_stub(projecthome, data_loc, overwrite)
    c.write()
