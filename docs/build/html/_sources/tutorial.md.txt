# Tutorial

We assume a machine with a reasonably up to date operating system.
**NOTE:** You may need to run the commands listed
here with higher user privilege such as root i.e., prefix commands with `sudo`.

## Install Dependencies
At the OS-level we require
[Python 2.7](https://www.python.org/downloads/release/python-2712/),
[Git](https://desktop.github.com/), and [Pip](https://pip.pypa.io/en/stable/)
to function.

If your system does not have any of these see the
[installation page](install.html).

## Install BLCI

Assuming all dependencies are installed simply clone BLCI from gitub and run the
installation script as follows:

```bash
git clone https://github.com/neurodata/blci.git
cd blci/
./install
```

If this fails, look to the full [installation guide](install.html) for detailed
installation instructions.

## BLCI Use

For more comprehensive documentation on the BLCI interface and commands,
please refer to the [interface page](interface.html).

### Example repo/project

The following is a project with code and data that we use as a running example
throughout this tutorial. To follow along **we advise you to [download
it](https://github.com/neurodata/blci/blob/master/docs/assets/myrepo.zip?raw=true).**

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

**NOTE:** All paths are relative to `$PROJECT_HOME`, the root directory for
your project.

#### Example `code` dir  details of importance

1. The script `code/a.py` *reads* `data/data.txt` and *writes*
`data/databy2.txt`
2. The script `code/analysis/c.py` *reads*

### Create a `blci.yml` config file

At a minimum the configuration file needs to contain the `language` setting and
BLCI will flesh it out as much possible, then users must complete it as
necessary.

All configuration settings are documented on the
[configuration page](config.html).

```
language: python
```

### Initialize (`init`) the repo

Execute:

```
./bl myrepo -i
```

BLCI initialization will result in a fleshed out, *but often incomplete*
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

**NOTE:** The order of the settings does not matter, but the spacing
matters when it comes to settings with lists as values.

BLCI also builds a code-to-code dependency metadata file that is saved as
`blci.deps`. This **should not** be edited by users. This file notes any
code-to-code dependencies within the repo. These are obtained from
`import`/`include` statements.

### Complete the configuration file

We must now specify all the data-to-code dependencies for the data files.
First, we need to add the `data` and `otherdata` directories as data locations.

```
data_loc:
- data
- otherdata
```

Next, we need to indicate the following data dependencies:

1. `data/data.txt` is read by `code/a.py` and `code/analysis/c.py`
2. `otherdata/data.txt` is written by `code/analysis/c.py`
3. `data/databy2.txt` is written by `code/a.py`.

Here is how we would achieve this:

```
data_dep:
    read:
        data/data.txt:
            - code/a.py
            - code/analysis/c.py
    write:
        data/databy2.txt:
            - code/a.py
        otherdata/data.txt:
            - code/analysis/c.py
```

## Modify `script` actions to justify `data_dep` settings

Now we add the `script` action that actually performs computation and supports
the `data_dep` settings. The following is what a `script` value might look like
for this example:

```
script:
    - python code/analysis/c.py data/data.txt 2.5 otherdata/data.txt
    - cd code && python a.py
```

Read over the
[`script`](https://docs.travis-ci.com/user/customizing-the-build#Customizing-the-Build-Step)
setting in Travis for details on what actions it triggers. Note that we use it
not as a testing action, but instead an action to *perform computation*.

### Add (`add`) the repo

Finally we need to add the repo as a BLCI repo. This action will:

1. Create a remote repo in Github for you with the name you specify (or it was
given by default) as the `name` argument. The repo will also have a branch with
the same name as your remote repo.
2. Create and track the remote repo with Travis-CI.

To perform this action execute:

```
./bl myrepo -a
```

Proceed to check [https://travis-ci.org/](https://travis-ci.org/) to ensure your
repo is created correctly and builds.

### Update BLCI repo
**TODO**: update instructions
