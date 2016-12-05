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

# config.py
# Created by Disa Mhembere on 2016-12-03.
# Email: disa@jhu.edu

# FIXME: Ensure all paths are relative the $PROJECT_HOME

import argparse
import sys
import yaml
import exceptions
from glob import glob
import re
import os

BL_SETTINGS = {
        "language",
        "version",
        "ignore",
        "nthread",
        "read",
        "code_loc",
        "data_loc",
        "data_dep",
        "script"
        }

BL_DEFAULTS = {
        "nthread": 1,
        "version": None,
        "ignore": "",
        "code_loc": "code",
        "data_loc": "data",
        }

BL_REQUIRED = set.symmetric_difference(BL_SETTINGS,
    set((BL_DEFAULTS.keys())))

class config():
    def __init__(self, fn=None, silent_fail=False):
        self.fn = fn

        if fn:
            self.read_config(fn, silent_fail)
        else:
            self._conf = {}
            self.valid = False

    def read_config(self, fn, silent_fail=False):
        with open(fn, "r") as f:
            try:
                self._conf = yaml.load(f)
            except yaml.YAMLError as err:
                sys.stderr.write("Config load ERROR:" + err + "\n")

        one_failed = False
        for setting in self._conf:
            if setting not in BL_SETTINGS:
                one_failed = True
                if not silent_fail:
                    raise exceptions.ParameterException(
                        "Unknown setting '{}' in file '{}'".format(setting, fn))

        if one_failed:
            self.valid = False
        else:
            self.valid = True

        if self.isvalid():
            for setting in BL_REQUIRED:
                if setting not in self._conf:
                    self.valid = False
                    break

    def isvalid_data(self):
        """ Does the config contain data_dep for the
                files stated in data_loc?
        """
        pass # FIXME: Stub

    def bashRE_2_pyRE(self, regex):
        """ FIXME: Very rudimentary """
        return regex.replace(".", "\.").replace("*", "+")

    def isignored(self, path):
        if not self.has_setting("ignore"):
            return False # No way to know so assume not to ignore

        # First attempt a direct match ...
        if os.path.exists(path):
            return True # if it exists then ignore it

        for item in self.get("ignore"):
            if re.match(self.bashRE_2_pyRE(item)):
                return True
        return False

    def isdatafile_tracked(self, path):
        if not self.has_setting("data_dep"): return False

        for ioattr in self.get("data_dep"):
            if path in ioattr:
                return True
        return False

    def track_datafile(self, path):
        if not self.has_setting("data_dep"):
            self._conf["data_dep"] = [{"read":[]}, {"write":[]}]

        # Add to read
        self._conf["data_dep"]["read"].append(path)

        # Add to write
        self._conf["data_dep"]["write"].append(path)

    def add_data_loc_path(self, path):
        if not has_setting("data_loc"):
            self._conf["data_loc"] = []

        if path not in self.get("data_loc"):
            self._conf["data_loc"].append(path)

    def unique_fn(self, path):
        # Create a unique fn using the path but don't overwrite if exists
        return "_stub" # TODO: Stub todo

    def write(self, overwrite=True):
        if not self.fn:
            self.fn = "blci.yml"

        if not overwrite:
            sp = os.path.splitext(self.fn)
            self.fn = self.unique_fn(sp[0]) + sp[1]

        with open(self.fn, "wb") as f:
            yaml.dump(self._conf, f)

    def build_data_dep_stub(self, data_loc=[], overwrite=True):
        """
        Build a stub of a config or add data dependencies to an existing
        config given one or more directories containing data
        """
        data_loc_not_found = False
        if not data_loc and not self.fn:
            data_loc_not_found = True

        elif self.fn:
            self.read_config(self.fn, silent_fail=True)
            if not self.has_setting("data_loc"):
                data_loc_not_found = True

        if data_loc_not_found:
            raise exceptions.ParameterException("Specify param "
                    "'data_loc' in config or pass 'data_loc' argument")

        if not self.has_setting("data_dep"):
            self._conf["data_dep"] = []

        if data_loc:
            for path in data_loc:
                self.add_data_loc_path(path)

        for _dir in data_loc:
            for _file in glob(os.path.join(_dir,"*")):
                if not self.isignored(_file) and not isdatafile_tracked(_file):
                    self.track_datafile(_file)

        self.write(overwrite)

    def isvalid(self):
        return self.valid

    def getall(self):
        return self._conf

    def get(self, setting):
        return self._conf[setting]

    def has_setting(self, setting):
        return self._conf.has_key(setting)

    def __getitem__(self, setting):
        return self._conf[setting]
