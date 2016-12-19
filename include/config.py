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
from bl_exceptions import *
from glob import glob
import re
import os
import time
from common import localize
from settings import *

class config():
    def __init__(self, fn, projecthome="", silent_fail=False,
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
        self._conf = {}

        if os.path.exists(self.fn):
            self.read_config(self.fn, silent_fail)
        else:
            raise FileNotFoundException("Cannot find configuration file "
                    "{}".format(self.fn))

        if add_defaults:
            self.add_defaults()

    def add_defaults(self):
        for conf in BL_DEFAULTS:
            if not self.has_setting(conf) or not self.get(conf):
                if conf == BL_VERSION:
                    self._conf[conf] = \
                        BL_DEFAULT_LANG_VERSION[self.get(BL_LANGUAGE)]
                elif conf == BL_READ:
                    self._conf[conf] = BL_DEFAULT_READ[self.get(BL_LANGUAGE)]
                else:
                    self._conf[conf] = BL_DEFAULTS[conf]

        if not self.has_setting(BL_READ):
            if self.get(BL_LANGUAGE) not in BL_READ_DEFAULTS.keys():
                raise UnsupportedFileException("{}".format(
                    self.get(BL_LANGUAGE)))

            self._conf[BL_READ] = BL_READ_DEFAULTS[self.get(BL_LANGUAGE)]

    def read_config(self, fn, silent_fail=False):
        with open(fn, "rb") as f:
            try:
                self._conf = yaml.load(f)
            except yaml.YAMLError as err:
                raise FileNotFoundException(
                        "Config load ERROR:" + err)
        if silent_fail:
            self.__check_valid__(level="WARN")
        else:
            self.__check_valid__(level="ERROR")

    def bashRE_2_pyRE(self, regex):
        """ TODO: Very rudimentary """
        return regex.replace(".", "\.").replace("*", "+")

    def isignored(self, path):
        if not self.has_setting(BL_IGNORE):
            return False # No way to know so assume not to ignore

        # First attempt a direct match ...
        if path in self.get(BL_IGNORE):
            return True # if it exists then ignore it

        for item in self.get(BL_IGNORE):
            if re.match(self.bashRE_2_pyRE(item), path):
                return True
        return False

    def track_datafile(self, path):
        path = localize(self.projecthome, path)
        self.__check_and_stub_dat_dep__()

        for ioattr in self.get(BL_DATA_DEP):
            if path not in self.get(BL_DATA_DEP)[ioattr].keys():
                # Add it to read or write
                print "Adding '{}' to {}: {} ...".format(path,
                        BL_DATA_DEP, ioattr)
                self._conf[BL_DATA_DEP][ioattr][path] = []

    def add_data_loc_path(self, path):
        if not self.has_setting(BL_DATA_LOCATION):
            self._conf[BL_DATA_LOCATION] = []

        if path not in map(os.path.relpath, self.get(BL_DATA_LOCATION)):
            self._conf[BL_DATA_LOCATION].append(path)

    def unique_fn(self, path):
        # Create a unique fn using the path but don't overwrite if exists
        if os.path.isdir(path):
            raise ParameterException("Path '{}' must be a file, not "
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
        if not self.has_setting(BL_DATA_DEP):
            self._conf[BL_DATA_DEP] = {BL_READ:{}, BL_WRITE:{}}
            return

        if not self.get(BL_DATA_DEP).has_key(BL_READ):
            self._conf[BL_DATA_DEP][BL_READ] = {}
        if not self._conf[BL_DATA_DEP].has_key(BL_WRITE):
            self._conf[BL_DATA_DEP][BL_WRITE] = {}

    def build_data_dep_stub(self, projecthome, overwrite=True):
        """
        Build a stub of a config or add data dependencies to an existing
        config given one or more directories containing data
        """
        self.projecthome = projecthome

        if not self:
            print "Incomplete configuration file '{}' ==>\n{}".format(
                    self.fn, self)

        for path in self.get(BL_DATA_LOCATION):
            if not os.path.exists(os.path.join(projecthome, path)):
                raise FileNotFoundException("'data_loc' Directory "
                        "'{}' does not exist!".format(path))

        self.__check_and_stub_dat_dep__()

        for path in self.get(BL_DATA_LOCATION):
            self.add_data_loc_path(path)

        for _dir in self.get(BL_DATA_LOCATION):
            for _file in glob(os.path.join(_dir,"*")):
                if not self.isignored(_file):
                    self.track_datafile(_file)

    def __check_valid__(self, level):
        """
        Determine whether the current config object is one that:
            1. BLCI understands i.e., keys are valid
            2. Has all the required settings keys for BLCI
            3. Has file paths that actually exist
        """
        # 1. Make sure we understand all settings
        for setting in self._conf:
            if setting not in BL_SETTINGS:
                msg = "Unknown setting '{}' in file '{}'".format(
                        setting, self.fn)
                if level == "ERROR":
                    raise ParameterException(msg)
                elif level == "WARN":
                    warn(msg)
                else:
                    return False

        # 2. Has reqd settings
        for setting in BL_REQUIRED:
            if not self.has_setting(setting):
                msg = "Required setting '{}' missing from file '{}'".format(
                        setting, self.fn)
                if level == "ERROR":
                    raise ParameterException(msg)
                elif level == "WARN":
                    warn(msg)
                else:
                    return False

        # 3. Finally, check paths exist
        projecthome = os.path.dirname(self.fn)
        path_settings = [BL_CODE_LOCATION, BL_DATA_LOCATION, BL_PATH]

        for setting in path_settings:
            if self.has_setting(setting): # If not it will get a default val
                for path in self.get(setting):
                    if not os.path.exists(os.path.join(projecthome, path)):
                        msg = "File '{}' missing".format(path)
                        if level == "ERROR":
                            raise FileNotFoundException(msg)
                        elif level == "WARN":
                            warn(msg)
                        else:
                            return False

        # 3b) Check data dependencies
        if self.has_setting(BL_DATA_DEP): # If not it will get a default val
            for k,v in self.get(BL_DATA_DEP).iteritems():
                for path in self.get(BL_DATA_DEP)[k]: # read or write
                    if not os.path.exists(os.path.join(projecthome, path)):
                        msg = "File '{}' missing".format(path)
                        if level == "ERROR":
                            raise FileNotFoundException(msg)
                        elif level == "WARN":
                            warn(msg)
                        else:
                            return False

        return True

    def isvalid(self):
        """
        Return a bool for validity of the configuration file based on the
        level=IGNORE argument to __check_valid__
        """

        return self.__check_valid__(level="IGNORE")

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

    def __nonzero__(self):
        return self.isvalid()
