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

# dependencies.py
# Created by Disa Mhembere on 2016-10-25.
# Email: disa@jhu.edu

# File used to do the following:
#   - Parse a file with code and produce a code hierarchy in json format
#       ignoring code managed by packages.
#   - Parse the dependencies file and create a configuration file for the CI

import argparse

class DependParser(object):
    def __init__(self):
        pass

    def generic_read(self, fn):
        raise NotImplementedError("generic_read")

    def py_read(self, fn):
        raise NotImplementedError("py_read")

    def r_read(self, fn):
        raise NotImplementedError("cpp_read")

    def julia_read(self, fn):
        raise NotImplementedError("java_read")

def main():
  parser = argparse.ArgumentParser(description="")
  parser.add_argument("ARG", action="", help="")
  parser.add_argument("-O", "--OPT", action="", help="")
  result = parser.parse_args()

if __name__ == "__main__":
  main()
