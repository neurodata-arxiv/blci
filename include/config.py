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
    def __init__(self, fn, projecthome, on_anomaly="IGNORE",
            add_defaults=True):
        """
        The blci configuration reader, writer and init project stub creator

        **Positional Arguments:**

        fn:
            - The config filename that you are reading or intend to write

        projecthome:
            - The relative/absolute path to the root of your project

        **Optional Arguments:**

        on_anomaly:
            - Default action on anomaly: ["IGNORE", "WARN", "ERROR"]
        add_defaults:
            - Populate your specified config with blci defaults
        """
        # Give defaults if building a new config
        self.fn = fn
        self.projecthome = os.path.abspath(projecthome)
        self._conf = {}

        if os.path.exists(self.fn):
            self.read_config(self.fn, on_anomaly)
        else:
            raise FileNotFoundException("Cannot find configuration file "
                    "{}".format(self.fn))

        if add_defaults:
            self.add_defaults()

    def add_defaults(self):
        """
        Add default values for any settings that we provide defaults for.
        """

        for conf in BL_DEFAULTS:
            if not self.has_setting(conf) or not self.get(conf):
                if conf == BL_VERSION: # Version default
                    self._conf[conf] = \
                        BL_DEFAULT_LANG_VERSION[self.get(BL_LANGUAGE)]
                elif conf == BL_READ: # Read default
                    self._conf[conf] = BL_DEFAULT_READ[self.get(BL_LANGUAGE)]
                else:
                    self._conf[conf] = BL_DEFAULTS[conf] # All other defaults

        if not self.has_setting(BL_READ):
            if self.get(BL_LANGUAGE) not in BL_READ_DEFAULTS.keys():
                raise UnsupportedFileException("{}".format(
                    self.get(BL_LANGUAGE)))

            self._conf[BL_READ] = BL_READ_DEFAULTS[self.get(BL_LANGUAGE)]

        if not self.get(BL_NAME): # Default is an empty string
            self._conf[BL_NAME] = os.path.basename(self.projecthome)

    def read_config(self, fn, on_anomaly="ERROR"):
        """
        Given a configuration file that is in `YAML format <http://yaml.org/>`_

        **Positional Arguments:**

        fn:
            - The config filename that you are reading or intend to write

        **Optional Arguments:**

        on_anomaly:
            - Action to perform when we encounter an anomaly
        """

        with open(fn, "rb") as f:
            try:
                self._conf = yaml.load(f)
            except yaml.YAMLError as err:
                raise FileNotFoundException("Config load ERROR:" + str(err))
        self.__check_valid__(on_anomaly)

    def bashRE_2_pyRE(self, regex):
        """
        TODO: Very rudimentary way to change bash shell regexs to python.

        **Positional Arguments:**

        regex:
            - The bash regular expression
        """
        return regex.replace(".", "\.").replace("*", "+")

    def isignored(self, path):
        """
        Determine if a provided path is meant to be ignored by blci.

        **Positional Arguments:**

        path:
            - The path or regex describing the path.
        """

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
        """
        Add a path stub to the `data_dep` `read` and `write` sections.

        **Positional Arguments:**

        path:
            - The path to a data file that will be written by blci.
        """

        path = localize(self.projecthome, path)
        self.__check_and_stub_dat_dep__()

        for ioattr in self.get(BL_DATA_DEP):
            if path not in self.get(BL_DATA_DEP)[ioattr].keys():
                # Add it to read or write
                print "Adding '{}' to {}: {} ...".format(path,
                        BL_DATA_DEP, ioattr)
                self._conf[BL_DATA_DEP][ioattr][path] = []

    def add_data_loc_path(self, path):
        """
        Add a path to the `data_loc` section of the blci config file.

        **Positional Arguments:**

        path:
            - The path to a data file that will be written by blci.
        """

        if not self.has_setting(BL_DATA_LOCATION):
            self._conf[BL_DATA_LOCATION] = []

        if path not in map(os.path.relpath, self.get(BL_DATA_LOCATION)):
            self._conf[BL_DATA_LOCATION].append(path)

    def unique_fn(self, path):
        """
        Generate a unique path given a proposed path. It simply adds a count to
        the proposed path until it is a non-existent path.

        **Positional Arguments:**

        path:
            - The proposed path to be written.

        **Retuns:**

        A `str` for the path of unique file.
        """

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
        """
        Write the config file to disk.

        **Optional Arguments:**

        overwrite:
            - Overwrite the existing config file if it does exist.
        """

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

    def build_data_dep_stub(self, overwrite=True):
        """
        Build a stub of a config or add data dependencies to an existing
        config given one or more directories containing data.

        **Positional Arguments:**

        overwrite:
            - Overwrite the existing data dependency file, if it does exist.
        """

        if not self:
            print "Incomplete configuration file '{}' ==>\n{}".format(
                    self.fn, self)

        for path in self.get(BL_DATA_LOCATION):
            if not os.path.exists(os.path.join(self.projecthome, path)):
                raise FileNotFoundException("'data_loc' Directory "
                        "'{}' does not exist!".format(path))

        self.__check_and_stub_dat_dep__()

        for path in self.get(BL_DATA_LOCATION):
            self.add_data_loc_path(path)

        for _dir in self.get(BL_DATA_LOCATION):
            for _file in glob(os.path.join(_dir,"*")):
                if not self.isignored(_file):
                    self.track_datafile(_file)

    def __check_valid__(self, on_anomaly):
        """
        Determine whether the current config object is one that:
            0. Uses a supported language and version
            1. Has all the required settings keys for BLCI
            2. Has file paths that actually exist

        **Positional Arguments:**

        on_anomaly:
            - The degree to which the alert the user ["ERROR", "WARN", "IGNORE"]
        """

        # 0. Is a supported laguage and version
        if self.get(BL_LANGUAGE) not in BL_DEFAULT_READ.keys():
            if on_anomaly == "ERROR":
                msg = "Unsupported language: '{}'".format(self.get(BL_LANGUAGE))
                raise ParameterException(msg)
            elif on_anomaly == "WARN":
                warn(msg)
            else:
                return False

        if self.get(BL_LANGUAGE) not in BL_DEFAULT_READ.keys():
            if on_anomaly == "ERROR":
                msg = "Unsupported language version: "
                "'{}'".format(self.get(BL_VERSION))
                raise ParameterException(msg)
            elif on_anomaly == "WARN":
                warn(msg)
            else:
                return False

        # 1. Has reqd settings
        for setting in BL_REQUIRED:
            if not self.has_setting(setting):
                msg = "Required setting '{}' missing from file '{}'".format(
                        setting, self.fn)
                if on_anomaly == "ERROR":
                    raise ParameterException(msg)
                elif on_anomaly == "WARN":
                    warn(msg)
                else:
                    return False

        # 2. Finally, check paths exist
        path_settings = [BL_CODE_LOCATION, BL_DATA_LOCATION, BL_PATH]

        for setting in path_settings:
            if self.has_setting(setting): # If not it will get a default val
                for path in self.get(setting):
                    if not os.path.exists(os.path.join(self.projecthome, path)):
                        msg = "File '{}' missing".format(path)
                        if on_anomaly == "ERROR":
                            raise FileNotFoundException(msg)
                        elif on_anomaly == "WARN":
                            warn(msg)
                        else:
                            return False

        # 3b) Check data dependencies
        if self.has_setting(BL_DATA_DEP): # If not it will get a default val
            for k,v in self.get(BL_DATA_DEP).iteritems():
                for path in self.get(BL_DATA_DEP)[k]: # read or write
                    if not os.path.exists(os.path.join(self.projecthome, path)):
                        msg = "File '{}' missing".format(path)
                        if on_anomaly == "ERROR":
                            raise FileNotFoundException(msg)
                        elif on_anomaly == "WARN":
                            warn(msg)
                        else:
                            return False

        return True

    def isvalid(self):
        """
        Is the configuration file a valid one?

        **Returns:**

        A bool for validity of the configuration file based on the
        on_anomaly=IGNORE argument to :func:`~include.add.__check_valid__`
        """

        return self.__check_valid__(on_anomaly="IGNORE")

    def getall(self):
        return self._conf

    def get(self, setting):
        """
        Get a setting.

        **Positional Arguments:**

        setting:
            - The name of setting you seek

        **Returns:**
            - The value of the setting.
        """
        return self._conf[setting]

    def has_setting(self, setting):
        """
        Does the configuration file have the setting?

        **Positional Arguments:**

        setting:
            - The name of setting you seek.

        **Returns:**
            - A `bool` indicating if the setting is set or not.
        """
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
