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

# format.py
# Created by Disa Mhembere on 2016-11-28.
# Email: disa@jhu.edu

import os
from bl_exceptions import FormatException

def check_project_format(_dir, dep_outfn, codedir, datadir):
    if os.path.isfile(dep_outfn):
        raise FormatException("Dependency file {} already exists. Either update"
                " project or delete project first".format(dep_outfn))
    if not os.path.isdir(codedir):
        raise FormatException("Incorrect code directory format. Expected a dir "
                "'{}'".format(codedir))
    if not os.path.isdir(datadir):
        raise FormatException("Incorrect data directory format. Expected a dir "
                "'{}'".format(datadir))
    print "Correct format!"
