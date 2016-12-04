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

# test_dependencies.py
# Created by Disa Mhembere on 2016-11-28.
# Email: disa@jhu.edu

import argparse
import sys
import os
sys.path.append(os.path.abspath("../"))

from dependencies import DependParser

def test(path="./test-blci/code",
        outputfn="./test-blci/blci_deps.json", fileext=[".py"]):
    dp = DependParser(fileext)
    dp.readcode(path)
    dp.write_deps(outputfn)

    outdp = DependParser(fileext)
    outdp.read(outputfn)
    assert dp == outdp

def main():
    parser = argparse.ArgumentParser(description="Dependency builder outputs a "
            "dir structure with all (local) non-package deps")
    parser.add_argument("path", action="store", help="The file or a directory "
            "containing files for which we want to build a dep graph")
    parser.add_argument("fileext", action="store", help="The file "
            "type we should parse for deps (others ignored) when given a "
            "directory", nargs="+")
    parser.add_argument("-o", "--outputfn", action="store", help="The output "
            "filename for the dep file written to disk", default=
            os.path.abspath(os.path.join(sys.argv[1], "blci_deps.json")))
    #TODO: Use me
    parser.add_argument("-i", "--ignore", action="store", help="The paths/exps "
          "to ignore", nargs="*")

    args = parser.parse_args()
    test(args.path, args.outputfn, args.fileext)

if __name__ == "__main__":
    main()
