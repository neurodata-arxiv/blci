# Actions

BLCI has three fundamental actions which can trigger computation and a change of
state: `script`, `trigger` and `verify` actions.

## Script

This is enabled by the use of the `script` setting in the configuration file. This operation is passed directly to Travis CI's `script` [setting](https://docs.travis-ci.com/user/customizing-the-build/) setting. BLCI uses this to  allow users to force changes in data dependencies. If data dependencies change this may cause `trigger`s to be created.

Note that BLCI creates and fully manages a `.travis.yml` file that is added to the repo when the first `add` is done. BLCI alters and adds to the `script` setting then passes it to `.travis.yml`.

**NOTE: Do not directly alter the `.travis.yml` file that BLCI creates** --
this action results in undefined behavior. *TODO: Reject such actions*

##  Verifiers

*TODO: This functionality is not yet supported*
This is enabled by the `verify` setting in the `blci.yml` configuration. The `verify` setting allows you to check that data being passed for use with a
pipeline is valid and true to the intended use. This allows users to define
one or more tests for new users to the pipeline.

## Triggers

Triggers are not created or defined by users, but are reactions to changes in code and data. Triggers may cause a few different actions to be taken by BLCI:
* A push to the users Github repo (which may in turn trigger another action)
* A Travis CI build
* *TODO: Other actions may be performed*

