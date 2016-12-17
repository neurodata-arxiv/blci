#!/usr/bin/env python

# Copyright 2016 neurodata (http://neurodata.io/)
# # Licensed under the Apache License, Version 2.0 (the "License");
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

# bl_exceptions.py
# Created by Disa Mhembere on 2016-10-25.
# Email: disa@jhu.edu

# Hold blci custom exceptions

def err(err):
    return "\x1B[31mERROR: {}\x1B[0m".format(err)

def __warn__(err):
    return "\x1B[33mWARNING: {}\x1B[0m".format(err)

class FormatException(Exception):
    def __init__(self, msg):
        super(FormatException, self).__init__(err(msg))

class UnknownFileException(Exception):
    def __init__(self, msg):
        super(UnknownFileException, self).__init__(err(msg))

class UnsupportedFileException(UnknownFileException):
    def __init__(self, _type):
        super(UnsupportedFileException, self).__init__\
            (err("Unsupported type '{}'".format(_type)))

class ParameterException(Exception):
    def __init__(self, msg):
        super(ParameterException, self).__init__(err(msg))

class ParsingException(Exception):
    def __init__(self, msg):
        super(ParsingException, self).__init__(err(msg))

class FileNotFoundException(IOError):
    def __init__(self, msg):
        super(FileNotFoundException, self).__init__(err(msg))

def warn(msg):
    print __warn__(msg)
