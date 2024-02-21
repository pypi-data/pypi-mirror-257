#!/usr/bin/env python

"""CLI tool to scan for Python VENVs"""

import os
from os.path import abspath, join, getsize
import configparser
import click

CFG_FILE = "pyvenv.cfg"
SECTION_STR = "DEFAULT"
VERSION_STR = "version"
SITE_STR = "include-system-site-packages"


def read_config(config_file):
    """Parses a VENV config file for selected details. Returns the information as tuple."""
    with open(config_file, encoding="UTF-8") as file:
        config_string = file.read()
        config_string = f"[{SECTION_STR}]\n" + config_string  # add configparser prefix
        parser = configparser.ConfigParser()
        parser.read_string(config_string)
        return parser.get(section=SECTION_STR, option=VERSION_STR), parser.get(
            section=SECTION_STR, option=SITE_STR
        )


def get_size_in_mb(root, decimals):
    """Traverses a root path for total size. Returns the size in Megabytes (MB)."""
    size = 0
    for parent, _, files in os.walk(root):
        for file in files:
            size += getsize(join(parent, file))
    return round(size / 1_048_576, decimals)


def scan_envs(root, sizing):
    """Traverses a root path for Python VENVs. Returns a dict with details about found VENVs."""
    print()
    print(f"Searching for VENVs in '{abspath(root)}':")
    envs = {}
    for parent, folders, files in os.walk(root):
        if CFG_FILE in files:
            version_str, site_str = read_config(abspath(join(parent, CFG_FILE)))
            size_str = get_size_in_mb(parent, 2) if sizing else 0
            envs[parent] = {
                "ver": version_str,
                "site": site_str,
                "size": size_str,
            }
            folders.clear()  # skip scanning VENV folder contents
    return envs


def print_envs(root, envs, sizing):
    """Pretty-prints a dict with details about VENVs."""
    print()
    if len(envs) > 0:
        for env in envs:
            print("  Folder  :", env.lstrip(root))
            print("  Python  :", envs[env]["ver"])
            print("  Sys-Pkgs:", envs[env]["site"])
            if sizing:
                print("  Size    :", envs[env]["size"], "MB")
            print()
    else:
        print("No VENVs found.")
    print()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-s", "--sizing", default=True, help="Calculate size of environments. Default: True"
)
def main(path, sizing):
    """
    Scans for Python virtual environments.

    PATH to be recursively scanned.
    """

    envs = scan_envs(path, sizing)
    print_envs(path, envs, sizing)


if __name__ == "__main__":
    # pylint: disable=E1120
    main()
