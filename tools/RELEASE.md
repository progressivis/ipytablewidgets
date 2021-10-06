# How to release a new version of ipytablewidgets

**NB:** Currently, this procedure was tested only on **Linux**.

**NB:** You can create a new release only if you have _maintainer_ privileges on:

* ipytablewidgets _PyPI_ project
* jupyter-tablewidgets _NPM_ package


Roughly, create a new release implies four main actions:

1. create a new tag/release on the repository
2. build the entire project(i.e. python+javascript)
3. publishing python code on the **PyPI** registry
4. publishing javascript code on the **NPM** registry

These actions are performed by the _create_release.py_ script, present in this directory.
Before using the script, you have to create (only the first time) and activate (always) an appropriate environment for it.

## Create an appropriate environment

If you already created an appropriate environment skip to the next item.

```bash
conda env create -f release_env.yml # -n  my_env_name
```
**NB:** The created environment is named _itw_release_ but you can change it by using the commented option 

## Activate the environment

```bash
conda activate itw_release
```

## The _create_release.py_ command

### Options explained

#### -r, --release-type [major|minor|patch|manual]

This option is mandatory. The first three values (major, minor, patch) have the same meaning as in [npm version](https://docs.npmjs.com/cli/v7/commands/npm-version) (actually _npm version_ is executed, then the new value of the _version_ key in _js/package.json_ is used for the following steps)

The _manual_ value keeps the current version in _package.json_ unchanged. If the corresponding repository tag already exists then no new tag is created and the user is asked if he wants to continue with packaging. This is useful if one want to recover a previous failure (e.g. when the publication on **PyPI** or **NPM** failed for some reason)

#### -\-skip-pypi BOOLEAN

The default value is **False**
When set to *True** the publication of the _ipytablewidgets_ python package on **PyPI** is not performed

#### -\-skip-npm-publish BOOLEAN

The default value is **False**
When set to *True** the publication of the _jupyter-tablewidgets_ javascript package on **NPM** is not performed

These two last options are also useful for failure recovery

### Before execution

The use needs to be logged in **NPM** registry and it is highly recomended to have a **PyPI** configured for [API token autentication](https://pypi.org/help/#apitoken)


### Normal use of _create_release.py_

In order to create a new release (major, minor or patch) the appropriate command is:

```bash
python create_release.py -r {major|minor|patch}
```

The command must be executed in the _tools_ directory.

**NB:** you have to be sure of your choice (among major, minor and patch) because it is not easy to _undo_ the result (e.g.  _undo_ a _major_ revision if you choose by mistake _major_ instead of _patch_) and this situation is not recoverable by this script.

### Failure recovery

If the git tag creation succeeds but, for some reason (e.g. authentication problem on registries) one (or both) publication failed, you can recover the release creation.

For example, if the git tag creation succeeds, the PyPI publication also succeeds but the NPM publication failed because you forgot to login on the registry, you can recover it this way (after eliminating the cause of the previous failure):

```bash
python create_release.py -r manual --skip-pypi=True
```

In this case, the script will discover that the tag corresponding to the _version_ key in _package.json_ already exists and ask you if you want to continue the packaging anyway. If your answer is **y** the tag creation and the PyPI publication are skipped and the **NPM** publication is runned again.
