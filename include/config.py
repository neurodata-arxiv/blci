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

import argparse
import sys
import yaml
import exceptions
from glob import glob
import re
import os
import time
from common import localize
from settings import *

class config():
    def __init__(self, fn="", projecthome="", silent_fail=False,
            add_defaults=True):
        """
        The blci configuration reader, writer and init project stub creator

        @param fn: The config filename that you are reading or intend to write
        @param projecthome: The relative/absolute path to the root of your
            project
        @param silent_fail: If you specify an invalid/incomplete config file via
            the `fn` argument. Should blci throw an exception?
        """
        # Give defaults if building a new config
        self.fn = fn
        self.projecthome = projecthome

        if self.fn:
            self.read_config(self.fn, silent_fail)
        else:
            self._conf = BL_DEFAULTS
            self.valid = False

        if add_defaults:
            self.add_defaults()

    def add_defaults(self):
        for conf in BL_DEFAULTS:
            if not self.has_setting(conf) or not self.get(conf):
                self._conf[conf] = BL_DEFAULTS[conf]

        if not self.has_setting("read"):
            if self._conf["language"] not in BL_READ_DEFAULTS.keys():
                raise exceptions.UnsupportedFileException("{}".format(
                    self._conf["language"]))

            self._conf["read"] = BL_READ_DEFAULTS[self._conf["language"]]

    def read_config(self, fn, silent_fail=False):
        with open(fn, "rb") as f:
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
                    return

            # Now make sure they exist
            for loc in self.get("code_loc"):
                if not os.path.exists(os.path.join(self.projecthome, loc)):
                    self.valid = False
                    return
            for loc in self.get("data_loc"):
                if not os.path.exists(os.path.join(self.projecthome, loc)):
                    self.valid = False
                    return

    def isvalid_data(self):
        """
        Does the config contain data_dep for the
                files stated in data_loc?
        """
        pass # FIXME: Stub

    def bashRE_2_pyRE(self, regex):
        """ TODO: Very rudimentary """
        return regex.replace(".", "\.").replace("*", "+")

    def isignored(self, path):
        if not self.has_setting("ignore"):
            return False # No way to know so assume not to ignore

        # First attempt a direct match ...
        if path in self._conf["ignore"]:
            return True # if it exists then ignore it

        for item in self.get("ignore"):
            if re.match(self.bashRE_2_pyRE(item), path):
                return True
        return False

    def track_datafile(self, path):
        path = localize(self.projecthome, path)
        self.__check_and_stub_dat_dep__()

        for ioattr in self.get("data_dep"):
            if path not in self._conf["data_dep"][ioattr].keys():
                # Add it to read or write
                print "Adding '{}' to data_dep: {} ...".format(path, ioattr)
                self._conf["data_dep"][ioattr][path] = []

    def add_data_loc_path(self, path):
        if not self.has_setting("data_loc"):
            self._conf["data_loc"] = []

        if path not in map(os.path.relpath, self.get("data_loc")):
            self._conf["data_loc"].append(path)

    def unique_fn(self, path):
        # Create a unique fn using the path but don't overwrite if exists
        if os.path.isdir(path):
            raise exceptions.ParameterException("Path '{}' must be a file, not "
                    "a directory ...".format(path))
        count = 1
        while (os.path.exists(path)):
            sp = os.path.splitext(path)
            prospective_path = sp[0] +"_" + str(count) + sp[1]
            if os.path.exists(prospective_path):
                count += 1
            else:
                path = prospective_path

        return path

    def write(self, overwrite=True):
        if not self.fn:
            self.fn = BL_DEFAULT_CONFIG_FN

        if not overwrite:
            self.fn = self.unique_fn(self.fn)

        print "Writing config file {} ..".format(self.fn)
        with open(self.fn, "wb") as f:
            f.write("# Written by BLCI's automated script on "
                    "{}\n\n".format(time.strftime("%c")))
            yaml.dump(self._conf, f, default_flow_style=False)

    def __check_and_stub_dat_dep__(self):
        if not self.has_setting("data_dep"):
            self._conf["data_dep"] = {"read":{}, "write":{}}
            return

        if not self._conf["data_dep"].has_key("read"):
            self._conf["data_dep"]["read"] = {}
        if not self._conf["data_dep"].has_key("write"):
            self._conf["data_dep"]["write"] = {}

    def build_data_dep_stub(self, projecthome, data_loc=[], overwrite=True):
        """
        Build a stub of a config or add data dependencies to an existing
        config given one or more directories containing data
        """
        self.projecthome = projecthome
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

        self.__check_and_stub_dat_dep__()

        for path in data_loc:
            self.add_data_loc_path(path)

        for _dir in data_loc:
            for _file in glob(os.path.join(_dir,"*")):
                if not self.isignored(_file):
                    self.track_datafile(_file)

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

    def __repr__(self):
        s = "BLCI configuration object:\n"
        for k,v in self._conf.iteritems():
            s += "{}: {}\n".format(k, v)
        return s

    def __eq__(self, other):
        return self._conf == other._conf

    def __ne__(self, other):
        return not self.__eq__(other)
