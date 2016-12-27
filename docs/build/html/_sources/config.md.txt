# The configuration file

We document the configuration file that is essential to the correct
functionality of BLCI. Note that there are several default values that
are specified and documented [here](defaults.html). All paths are relative
to the root directory of the project i.e., `$PROJECT_HOME`.

**NOTE:** Any configuration passed that is not BLCI specific is passed directly
to the Travis CI configuration file `.travis.yml`.

## Settings

We document all BLCI specific settings.

### `name`
The user defined repository name e.g., `my-repo`.

### `language`
The programming language your project utilizes e.g., `cpp`.

### `version`
The version of the programming language you are using e.g., `2.7`.

### `nthread`
The number of threads of execution to use locally for any actions
that are parallelizable.

### `ignore`
The file extensions, file names, or *TODO: regular expressions* that should
**not** be considered for code dependencies e.g., `.pyc`, `.d`.

### `read`
The file extensions, file names, or *TODO: regular expressions* that BLCI
**will** use for code dependencies.

### `data_dep`
- `data_dep:read`
This allows users to define what *read* data-to-code dependencies exist within
the repo. The key, a path to a data file is what is going to be **read** by the
value(s), paths to code files. This setting is a key-value pair with key being
a filename and value being the code that can possibly write the file e.g.,
`data/data.npy: [file1.py, file2.py]`.
- `data_dep:write`
This allows users to define what *write* data-to-code dependencies exist within
the repo. The key, a path to a data file is what is going to be **written** by
the value(s), paths to code files. This setting is a key-value pair with key
being a filename and value being the code that writes it.
e.g., `data/data.npy: [file1.py, file2.py]`.

### `code_loc`
The directory/directories containing **code** BLCI must track and utilize.
e.g `[code/serial, code/parallel]`.

### `data_loc`
The directory/directories containing **data** BLCI must track and utilize.
e.g `[code, code/serial, code/parallel]`.

### `path`
A location where BLCI should look for packages/libraries installed that are
non-conventional e.g. `[include/path]`.

### `install`
Passed directly to
[Travis](https://docs.travis-ci.com/user/customizing-the-build/#Skipping-the-Installation-Step).
Used to install packages/software and identical to the use within Travis-CI.

### `credentials`
The file that contains your Github OAuth token. The default is `.credentials`.

### `description`
A user defined description of your repo. This can be as verbose as you deem
necessary. e.g. `"A repo that enables Floki to be cunning"`.
