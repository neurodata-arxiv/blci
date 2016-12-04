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

BLCI_SETTINGS = {
        "language",
        "version",
        "ignore",
        "nthread",
        "read"
        }

class config():
    def __init__(self, fn=None, silent_fail=False):
        if fn:
            self.read_config(fn, silent_fail)
        else:
            self._conf = None
            self.valid = False

    def read_config(self, fn, silent_fail=False):
        with open(fn, "r") as f:
            try:
                self._conf = yaml.load(f)
            except yaml.YAMLError as err:
                sys.stderr.write("Config load ERROR:" + err + "\n")

        one_failed = False
        for setting in self._conf:
            if setting not in BLCI_SETTINGS:
                one_failed = True
                if not silent_fail:
                    raise exceptions.ParameterException(
                        "Unknown setting '{}' in file '{}'".format(setting, fn))

        if one_failed:
            self.valid = False
        else:
            self.valid = True

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
