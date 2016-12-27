# Tutorial

We describe how to get up and running for a machine with a reasonably up to
date operating system. **NOTE:** You may need to run the commands listed
here with higher user privilege such as root i.e., prefix commands with `sudo`.

### Install Dependencies
At the OS-level we require
[Python 2.7](https://www.python.org/downloads/release/python-2712/),
[Git](https://desktop.github.com/), and [Pip](https://pip.pypa.io/en/stable/)
to function.

If your system does not have any of these see the
[installation page](install.html).

## BLCI Use

For more comprehensive documentation on the BLCI interface and commands,
please refer to the [interface page](interface.html).

### Example repo/project

The following is a repository of code and data that we use as a running example
throughout this tutorial.

```
myrepo/
	code/
		a.py
        analysis/
            c.py
	data/
		data.txt
		databy2.txt
	otherdata/
		data.txt
```

### Create a `blci.yml` config file

The minimum a configuration file needs to contain is the `language` setting and
BLCI will flesh it out as much possible, before the user must complete it.
**NOTE:** All paths are relative to `$PROJECT_HOME`, the root directory for
your project:

All configuration settings are documented on the
[configuration page](config.html).

```
language: python
```

### Initialize (`init`) the repo

BLCI initialize will result in a fleshed out, *but often incomplete*
`blci.yml` file. In our case what we receive is:

```
language: python
version: 2.7
name: myrepo
description: A BrainLab Continuous Integration repo
code_loc:
- code
credentials: .credentials
data_dep:
  read: {}
  write: {}
data_loc:
- data
ignore: [.*, .pyc, .d, .o, .javac, .rbin, .mat]
nthread: 1
read:
  - .py
  - .ipynb
path: []
```

**NOTE:** The order of the settings does not matter.

BLCI also builds a code-to-code dependency metadata file that is saved as
`blci.deps`. This **should not** be edited by users.

### Complete the configuration file

We need to add the `myrepo/otherdata` directory as a data directory and
specify all the data-to-code dependencies for the data files in
`myrepo/data` and `myrepo/`. We add the following lines to the config file and

### Make pipeline/repo a valid BLCI repo

**TODO**: add instructions
```
TODO
```

### Push BLCI repo
**TODO**: push instructions

### Update BLCI repo
**TODO**: update instructions

