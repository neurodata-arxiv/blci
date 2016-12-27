# Authentication

BLCI requires you to already have authentication credentials to:

1. [Github](https://github.com)
2. [Travis CI](https://travis-ci.org/)
3. SSH keys setup for Github (*TODO: Won't be necessary in the future*)
4. A Github OAuth token

## SSH Keys
You must have setup SSH keys to allow password-less authentication to your Github
repos already. If you do not, follow the steps outlined 
[here](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)
and copy and add your `id_rsa.pub` public key to your Github account at
[https://github.com/settings/keys](https://github.com/settings/keys).

Lastly, In order to allow BLCI to create an autonomously managed Github and Travis CI
repos you will need an **authentication token**.

## OAuth authentication token

Follow the steps outlined
[here](https://help.github.com/articles/creating-an-access-token-for-command-line-use/).
Copy and paste the token into a file in the root of your project. The default name that BLCI
expects is `.credentials`, but you can set the
[`credentials`](file:///Users/disa/Research/blci/docs/build/html/config.html#credentials)
setting in the `blci.yml` configuration to adapt the default behavior.
Your token file will never be tracked by Git or BLCI.
**It must remain local and untracked!**

## Permission level required for OAuth token
Your token must select the following scopes:

- repo
- read:org
- admin:repo_hook
- user:email
- delete_repo

## No usable auth token?

If you do not have one you will need to create an authentication token with
sufficient permission. Create a new token at [Github](https://github.com/settings/tokens/new).
