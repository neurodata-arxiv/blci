# Default settings

We document default values for the configuration file here. Note that all
filenames below are relative to `$PROJECT_HOME` i.e., the root of your
project.

## Filenames

The following files named are fully managed by BLCI and **should not be changed
manually**:

- BLCI's main configuration file: *blci.yml*
- For data dependencies: *blci.deps*
- The underlying continuous integration configuration file: *.travis.yml*
- Git's ignore file: *.gitignore*

Only the credentials filename is configurable. This file contains one
line that has your Github API token by default it is *.credentials*. This
can be altered using the `credentials` setting in the configuration file.

## `version` setting

Every language progresses so it is important we track the version of the language
to correctly parse code. We use the following as defaults for languages:

* python: 2.7,
* julia: 0.4,
* cpp: "c++11",
* c: "c11",
* r: 3,
* java: 7,
* mat: 7

## `read` setting

We maintain the following `read` settings defaults by file type:

- python: [ ".py", ".ipynb"]
- julia: [".j", ".jl"]
- cpp: [".cpp", ".c", ".h", ".hpp"]
- c: [".c", ".h"]
- r: [".r"]
- java: [".java"]
- mat: [".m"]

## Miscellaneous configuration settings (blci.yml)

The following are default configurations setting you receive if not specified.

* `nthread`: 1
* `code_loc`: ["code"]
* `data_loc`: ["data"]
* `ignore`: [".*", ".pyc", ".d", ".o", ".javac", ".rbin", ".mat"]
* `description`: "A BrainLab Continuous Integration repo"
* `credentials`: ".credentials"

The following settings can be left undefined but will receive no-op values by default:

* `path`, `data_dep`, `install`, `version`