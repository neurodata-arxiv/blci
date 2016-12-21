# Authentication

BLCI requires you to already have authentication credentials to:

1. [Github](https://github.com)
2. [Travis CI](https://travis-ci.org/)

In order to allow BLCI to create an autonomously managed Github and Travis CI
repos you will need an **authentication token**.

## Authentication token

Have your Github email and password handy for this. Follow the steps outlined
[here](https://help.github.com/articles/creating-an-access-token-for-command-line-use/).
Copy and paste the token into a file in the root of your project. The default name that BLCI
expects is `.credentials`, but you can set the `credentials` setting in the `blci.yml`
configuration to adapt the default behavior.

## Permission level required for token

Your token must select the following scopes:

- repo
- read:org
- admin:repo_hook
- user:email
- delete_repo

## No usable auth token?

If you do not have one you will need to create an authentication token with
sufficient permission. Create a new token at
[github](https://github.com/settings/tokens/new).
