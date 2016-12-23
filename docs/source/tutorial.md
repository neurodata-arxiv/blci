# Tutorial

We define how to get up and running for a machine with a reasonably up to date
operating system. **NOTE:** You may need to run the commands listed here with
higher user privilege such as root i.e., prefix commands with `sudo`.

### Install Dependencies
At the OS-level we require [Python 2.7](https://www.python.org/downloads/release/python-2712/), [Git](https://desktop.github.com/), and [Pip](https://pip.pypa.io/en/stable/) to function.

If your system does not have any of these see the [installation page](install.html).

## BLCI Use

For more comprehensive documentation on the BLCI interface and commands, please refer to the [interface page](interface.html).

### Create a `blci.yml` config file

For a complete explanation of configuration parameters and the `blci.yml` configuration file refer to the [config file page](config.html).

Consider this simple example repository with the following hierarchy:

```
blci\
myrepo\
	code\
		a.py
	data\
		data.txt
		databy2.txt
	otherdata\
		data.txt
```

A minimal starting `blci.yml` configuration file is necessary as the `--init`
call will flesh it out to include defaults and stubs as necessary. **NOTE** that all paths are relative to `myrepo` which blci refers to as `$PROJECT_HOME`:

```
language: python
version: 2.7
name: foobars
blci_root: ../blci
read: *.py
script: python code/analysis/c.py data/data.txt 2.5 otherdata/data.txt python
```

**TODO**: make a minimal working config

### Make pipeline/repo a valid BLCI repo

**TODO**: add instructions
```
TODO
```

### Push BLCI repo
**TODO**: push instructions

### Update BLCI repo
**TODO**: update instructions




