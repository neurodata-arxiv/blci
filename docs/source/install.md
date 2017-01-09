# Installation

BLCI installation is simple. There are only a few dependencies:

Your system must have working version of:

- [Python 2.7](https://www.python.org/downloads/)
- [Git](https://desktop.github.com/)
- [Pip](https://pip.pypa.io/)

**NOTE:** You may need to run the commands listed here with
higher user privilege such as root i.e., prefix commands with `sudo`.

BrainLab-CI can be installed by cloning the Github repo as follows:

- Through HTTPS: `git clone https://github.com/neurodata/blci.git`
```bash
cd blci/
./install
```

Once installation is complete use the BLCI driver `./bl`

## Missing OS-level dependencies ??

If you are missing some of these, install them first for ultimate happiness.

#### Mac quick install (requires `Brew`)
If you do not have Brew, first install it:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

, next install the dependencies:

```bash
brew install git
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
pip install -U argparse pyyaml pytest gitpython
```

#### Ubuntu quick install

For most modern mainstream Linux environments it is sufficient to use the system provided package manager. For [Ubuntu](https://www.ubuntu.com/) this is `apt-get`, for [RedHat](https://www.redhat.com/) this is `yum`. We will use Ubuntu as our example:

```
apt-get install git
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
pip install -U argparse pyyaml pytest gitpython
```
