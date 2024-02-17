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

import click
import json
import os
import sys
from . import utils, __version__


@click.group()
def cli():
    pass


@cli.command(help="configure a new repository")
@click.argument("checkout_dir", type=str)
@click.argument("checkout_cmd", type=str)
@click.option("--checkout/--no-checkout", default=True, show_default=True)
@click.option("--config-path", type=str, default=utils.CONFIG_PATH)
@click.option(
    "--extra-git-remotes", nargs=2, type=click.Tuple([str, str]), multiple=True
)
@click.option("--git-configs", nargs=2, type=click.Tuple([str, str]), multiple=True)
def config(
    checkout_dir: str,
    checkout_cmd: str,
    checkout: bool,
    config_path: str,
    extra_git_remotes: list[(str, str)],
    git_configs: list[(str, str)],
):
    utils.config_repo(
        checkout_dir=checkout_dir,
        checkout_cmd=checkout_cmd,
        checkout=checkout,
        config_path=config_path,
        extra_git_remotes=extra_git_remotes,
        git_configs=git_configs,
    )


@cli.command(help="find repo directories tracked by myrepos")
@click.argument("query", nargs=-1)
def find(query: list[str]):
    matches = utils.find_repo(query)
    for repo in matches:
        click.echo(repo)


@cli.command(help="sort ~/.mrconfig")
def sort():
    sorted_config = utils.sort()
    with open(os.path.expanduser("~/.mrconfig"), "w") as f:
        sorted_config.write(f)


@cli.command(help="show version information")
def version():
    click.echo(__version__)
