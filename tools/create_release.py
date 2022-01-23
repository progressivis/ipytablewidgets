# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import subprocess
import click
import git
import time
import os
import json
import os.path as osp
from os.path import join as pjoin
import tempfile
import sys
import glob

here = osp.dirname(osp.abspath(__file__))
repo_root = osp.dirname(here)
home_dir = os.getenv("HOME")


def get_version():
    package_json = pjoin(repo_root, "js", "package.json")
    with open(package_json) as f:
        return json.load(f)["version"]


# see: https://www.devdungeon.com/content/working-git-repositories-python#toc-8
@click.command()
@click.option("--skip-pypi", default=False)
@click.option("--skip-npm-publish", default=False)
@click.option(
    "--release-type",
    "-r",
    required=True,
    type=click.Choice(["major", "minor", "patch", "manual"], case_sensitive=False),
)
def release_it(skip_pypi, skip_npm_publish, release_type):
    click.echo(release_type)
    if not skip_pypi:
        # TODO: check it better
        if not osp.exists(pjoin(home_dir, ".pypirc")):
            inp = input(
                "PyPI config file .pypirc does not exist in your homedir."
                "Continue anyway [y/n]?"
            )
    repo = git.Repo(repo_root)
    # import pdb;pdb.set_trace()
    assert repo.active_branch.name in ("main", "master")
    remotes = repo.remotes
    assert len(remotes) == 1
    remote = remotes[0]
    existing_tags = [to.name for to in repo.tags]
    if repo.is_dirty(untracked_files=False):
        inp = input("Changes detected. Continue anyway [y/n]?")
        if inp != "y":
            print("Exiting ...")
            return
    vers = get_version()
    if release_type != "manual":
        subprocess.check_call(
            ["npm", "version", release_type], cwd=pjoin(repo_root, "js")
        )
        time.sleep(1)
        vers = get_version()
        repo.index.add([pjoin(repo_root, "js", "package.json")])
        repo.index.commit(f"version bumped ({vers}) by npm version {release_type}")
    if vers in existing_tags:
        inp = input(
            f"Release {vers} already exists. Continue with packaging anyway [y/n]?"
        )
        if inp != "y":
            print("Exiting ...")
            return
    else:
        repo.create_tag(vers)
        print(repo.remotes.origin.push(vers))
    https_url = repo.remotes.origin.url.replace(":", "/", 1).replace(
        "git@", "https://"
    )  # TO DO: improve
    print(https_url)
    if skip_pypi and skip_npm_publish:
        return
    pack_name = (
        subprocess.check_output([sys.executable, "setup.py", "--name"], cwd=repo_root)
        .decode("utf8")
        .strip()
    )
    tmpdir = tempfile.mkdtemp(prefix=pack_name, dir="/tmp/")
    repo_dir = pjoin(tmpdir, pack_name)
    clone = git.Repo.clone_from(https_url, repo_dir)
    clone.git.checkout(vers)
    subprocess.check_call([sys.executable, "-m", "build"], cwd=repo_dir)
    if not skip_pypi:
        dist_dir = pjoin(repo_dir, "dist")
        dist_files = glob.glob(dist_dir + "/*")
        subprocess.check_call(
            ["twine", "upload", "--repository", "pypi"] + dist_files, cwd=repo_dir
        )
    if not skip_npm_publish:
        js_dir = pjoin(repo_dir, "js")
        subprocess.check_call(["npm", "publish"], cwd=js_dir)
    # TODO: delete tmpdir
    print("tmpdir:", tmpdir)


if __name__ == "__main__":
    release_it()
