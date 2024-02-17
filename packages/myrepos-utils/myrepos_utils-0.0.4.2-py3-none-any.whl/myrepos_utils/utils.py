#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) Michel Lind
#
# SPDX-3.0-License-Identifier: GPL-2.0-or-later
#
# This program is free software.
# For more information on the license, see COPYING.md.
# For more information on free software, see
# <https://www.gnu.org/philosophy/free-sw.en.html>.

import configparser
import os
import pathlib
import subprocess

CONFIG = configparser.ConfigParser()
CONFIG_PATH = os.path.expanduser("~/.mrconfig")
CONFIG.read(CONFIG_PATH)


def get_config_repo_cmd(
    checkout_dir: str,
    checkout_cmd: str,
    config_path: str = CONFIG_PATH,
    extra_git_remotes: list[(str, str)] = None,
    git_configs: list[(str, str)] = None,
) -> list[str]:
    relpath = get_relpath(checkout_dir, config_path)
    checkout_full_cmd_list = [checkout_cmd]

    if extra_git_remotes or git_configs:
        repo_name = os.path.basename(relpath)
        checkout_full_cmd_list.append(f"cd {repo_name}")

    if git_configs:
        for key, value in git_configs:
            checkout_full_cmd_list.append(f"git config {key} {value}")

    if extra_git_remotes:
        for remote_name, remote_url in extra_git_remotes:
            checkout_full_cmd_list.append(f"git remote add {remote_name} {remote_url}")
        # intentionally do this later in case git fetch fails
        for remote_name, _ in extra_git_remotes:
            checkout_full_cmd_list.append(f"git fetch {remote_name}")

    checkout_full_cmd = " && ".join(checkout_full_cmd_list)

    mr_cmd = ["mr", "config", relpath, f"checkout={checkout_full_cmd}"]
    return mr_cmd


def get_relpath(path: str, config_path: str = CONFIG_PATH) -> str:
    full_path = os.path.join(os.getcwd(), path)
    common_prefix = os.path.commonprefix([full_path, config_path])
    relpath = os.path.relpath(full_path, common_prefix)
    return relpath


def get_repos(config: configparser.ConfigParser = CONFIG) -> list[str]:
    return list(config.sections())


def config_repo(
    checkout_dir: str,
    checkout_cmd: str,
    checkout: bool,
    config_path: str = CONFIG_PATH,
    extra_git_remotes: list[(str, str)] = None,
    git_configs: list[(str, str)] = None,
) -> int:
    mr_cmd = get_config_repo_cmd(
        checkout_dir=checkout_dir,
        checkout_cmd=checkout_cmd,
        config_path=config_path,
        extra_git_remotes=extra_git_remotes,
        git_configs=git_configs,
    )
    res = subprocess.run(mr_cmd)

    if not checkout:
        return res.returncode

    if res.returncode != 0:
        return res.returncode

    checkout_dirname = os.path.dirname(checkout_dir)
    checkout_basename = os.path.basename(checkout_dir)
    checkout_cmd = ["mr", "-d", checkout_basename, "co"]
    if checkout_dirname:
        pathlib.Path(checkout_dirname).mkdir(parents=True, exist_ok=True)
        res = subprocess.run(checkout_cmd, cwd=checkout_dirname)
    else:
        res = subprocess.run(checkout_cmd)
    return res.returncode


def find_repo(
    query: list[str], config: configparser.ConfigParser = CONFIG
) -> list[str]:
    import re

    repos = get_repos(config)
    r = f".*{'.*'.join(query)}.*"
    return [os.path.expanduser(f"~/{repo}") for repo in repos if re.match(r, repo)]


def sort(config: configparser.ConfigParser = CONFIG) -> configparser.ConfigParser:
    sorted_config = configparser.ConfigParser()
    for sec in sorted(config.sections()):
        sorted_config.add_section(sec)
        for k, v in config[sec].items():
            sorted_config[sec][k] = v
    return sorted_config
