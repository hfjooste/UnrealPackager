# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import sys
import argparse


class Args:
    """ Class responsible for enforcing, extracting and formatting arguments passed to the script. """
    parser = None
    github_version = None
    github_tag = None
    github_commit = None
    github_prerelease = False

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--version", action="store_true",
                                 help="Check the version number of Unreal Packager", required=False)
        self.parser.add_argument("--gh-version", metavar="\b",
                                 help="Specify the version used on GitHub", required=False)
        self.parser.add_argument("--gh-tag", metavar="\b",
                                 help="Specify the tag used on GitHub", required=False)
        self.parser.add_argument("--gh-commit", metavar="\b",
                                 help="Specify the commit or branch used when creating the tag on GitHub", required=False)
        self.parser.add_argument("--gh-prerelease", metavar="\b",
                                 help="Should the release be marked as a pre-release on GitHub?",
                                 required=False, default="false")
        self.parse()

    def parse(self):
        """ Parse the arguments passed to the script. """
        args = self.parser.parse_args()
        if args.version:
            sys.exit(0)
        self.github_version = args.gh_version
        self.github_tag = args.gh_tag
        self.github_commit = args.gh_commit
        self.github_prerelease = args.gh_prerelease.lower().strip() == "true"
        self.print_override("GitHub Version", self.github_version, None)
        self.print_override("GitHub Tag", self.github_tag, None)
        self.print_override("GitHub Commit", self.github_commit, None)
        self.print_override("GitHub Pre-Release", self.github_prerelease, False)

    def print_override(self, name, value, default):
        """ Print a message if the value is not the default. """
        if value == default:
            return
        print(f"Overriding {name}: {value}")

