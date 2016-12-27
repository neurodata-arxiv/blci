# BLCI User Interface

The way to interact with BLCI is through the `./bl` driver script within the
BLCI root directory. Pass no argument to see help and options.

<!--## Configuration file-->

<!--BLCI requires a configuration file named `blci.yml` to operate.-->
<!--When a repo is initiated via the `./bl -i` flag, `blci.yml` is-->
<!--updated to contain [defaults](defaults.html) and **stub**-->
<!--[settings](include.html#include.settings.BL_REQUIRED)-->
<!--that are minimally required in order for BLCI to be a *valid* BLCI repo.-->

<!--Let's start by creating an incomplete config file in `$PROJECT_HOME`-->
<!--(the root directory for your project):-->

<!--```-->
<!--name: my-repo-->
<!--language: python-->
<!--read:-->
	<!--- .py-->
<!--script:-->
	<!--- python -c "print 'Hello BLCI'"-->
<!--```-->

## Initialize the repo

Once you have a `blci.yml` configuration file in the root directory of your
repo/project (i.e., `$PROJECT_HOME`) with at least the required configuration
settings (`name`, `language`, `read`, `script`), You can initialize the repo as
follows:

```
./bl -i $PROJECT_HOME
```
BLCI initialization performs two actions:

1. Builds and saves the code dependency graph file `blci.deps`
2. Fleshes out a minimal `blci.yml` configuration file to a point to where
a repo is a valid BLCI repo leaving only the `data_deps` setting to be
completed by the user.

**NOTE:** The default action is to append and overwrite the minimal
configuration file a user creates. The filename of the original
configuration file will change to `blci.yml.old`. To change the *overrwrite*
behavior use the `-n [--nooverwrite]` flag.
## Add the repo

To add a repo execute:
```
./bl -a $PROJECT_HOME
```

A BLCI action:

1. Create a remote Github repo and track it using Travis CI **if none exists.**
2. Build the Travis metadata.
3. Add, commit, push and Travis build your repo.

## TODO: Undo

```
./bl -u $PROJECT_HOME
```

Undo the previous `./bl -a` (add) action and restore the repo to it's previous state.

## Build

Force a build of your BLCI repo without making changes to your code or using `./bl -a`. Execute:

```
./bl -b $PROJECT_HOME
```

Force a build action without changing any code within the repo.

## Clean

To clean up all BLCI metadata and configuration files use the clean operation.
**This action deletes files so use with care.**

```
./bl -i $PROJECT_HOME
```
