# Overview

BrainLab-CI (BLCI) is a code and data management continuous integration
tool that; providing the ability to perform collaborative, community
experiments with data-quality controls and full provenance. BLCI
autonomously determines code dependencies and provides infrastructure
to link code to data items.


## Functionality
BLCI provides the ability to:

- Create a dependency-aware pipeline (or section of a pipeline) that tracks
code and data dependencies and performs autonomous updates when upstream
changes occur.
- Define custom **trigger** actions to read/write and update data when code changes. This is done via the `script` argument in the `blci.yml` configuration file. See [the actions page](actions.html) for information on triggers.
- Trigger actions are performed when your repo is *added* or *updated*.
- Define **verification** actions via the `verify` argument in the `blci.yml` configuration file. The actions can be used to ensure either:
	1. Code pushed to repo is valid for use with data.
	2. Data pushed to repo is valid for use with code.
- Visualize the effects of pushed code and data to the repo via dashboards (FIXME).

## Compatibility and Support

We support modern Linux and Mac operating systems and provide documentation
with these in mind. BLCI has can also run in Windows environments,
but we do not provide Windows specific documentation. We suggest Windows
users take advantage of virtualization environments such as
[VirtualBox](https://www.virtualbox.org/), [VMWare](http://www.vmware.com/) to obtain Linux environments.

## How to **not** use BLCI

BLCI is meant to be used a version control system. In fact it relies on [Git](https://git-scm.com/) for version control so using it as such redundant and gives you less control over your *commits*. If a user performs *git commits* without using the BLCI's `./bl` undefined behavior may occur.
