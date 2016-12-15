# BLCI User Interface

The way to interact with BLCI is through the `./console.py` driver script within the BLCI root directory. Pass the `-h` to see all the arguments and options i.e., `./console.py -h`.

## The example repo

Let us start with our example pipeline we want to be BLCI repo. Consider the following directory hierarchy when we start:

```
test-blci\
	- code
		- __init__.py
		- a.py
	- data
		- data.txt
		- databy2.txt
	- otherdata
		- data.txt
```

## Initiate a repo

BLCI requires a configuration file named `blci.yml` to operate. When a repo is initiated via the `./console.py -i` flag, `blci.yml` is updated to contain the all the [required configuration](#TODO) **stubs** it needs in order to be a *valid* BLCI repo. 

Let's start by creating an incomplete config file:

```
TODO: file here
```

Now by passing the following would stub our `blci.yml` file with all reqquired configs.

```
TODO: init repo
```

## Complete the config
TODO

## Ingest the repo
TODO

## Push the repo
TODO

## Update the repo
TODO

## Push the repo
