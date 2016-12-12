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

# console.py
# Created by Disa Mhembere on 2016-10-25.
# Email: disa@jhu.edu

import argparse
from include.ingest import ingest
from include.init import init
from include.exceptions import ParameterException

def main():
    parser = argparse.ArgumentParser(description="The BLCI CLI. Pass "
            "-h for help")
    parser.add_argument("projecthome", action="store", help="The root "
            "folder of the project")
    parser.add_argument("-i", "--init", action="store_true", help="Intiate "
            "a project with dependency and BLCI configuration file.")
    parser.add_argument("-I", "--ingest", action="store_true", help="Ingest "
            "(non-existing) module")
    parser.add_argument("-u", "--update", action="store_true", help="Update "
            "existing module")
    parser.add_argument("-o", "--overwrite", action="store_true", help=
            "Overwrite the config when performing actions? This will not remove"
            " old settings, but instead append & merge.")
    parser.add_argument("-b", "--bare", action="store_true", help="Scrap all "
            "configs and start afresh?")
    args = parser.parse_args()

    if args.init:
        init(args.projecthome, args.overwrite, args.bare)
    elif args.ingest:
        ingest(args.projecthome)
    else:
        raise NotImplementedError("Other methods incomplete!")

if __name__ == "__main__":
    main()