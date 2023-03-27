# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import shutil
import configparser


class Config:
    """ Helper class used to read the config file, extract values and verify the configuration """
    unreal_install_dir = ""
    output = ""
    project_path = ""
    project_platforms = []
    project_unreal_version = ""
    plugin_path = ""
    plugin_unreal_versions = []
    plugin_visual_studio = ""
    mkdocs_path = ""
    mkdocs_auto_deploy = False
    mkdocs_include_pdf = False
    mkdocs_create_zip = False
    github_create_release = False
    github_owner = ""
    github_repo = ""
    github_token = ""
    github_commit = ""
    github_release_notes = ""
    task_pre = None
    task_post = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("unrealpackager.conf")
        self.unreal_install_dir = config.get("environment", "unreal_install_dir", fallback="")
        self.output = config.get("environment", "output", fallback="")
        self.project_path = config.get("project", "path", fallback="")
        self.project_platforms = list(filter(None, config.get("project", "platforms", fallback="").replace(" ", "").split(",")))
        self.project_unreal_version = config.get("project", "unreal_version", fallback="")
        self.plugin_path = config.get("plugin", "path", fallback="")
        self.plugin_unreal_versions = list(filter(None, config.get("plugin", "unreal_versions", fallback="").replace(" ", "").split(",")))
        self.plugin_visual_studio = config.get("plugin", "visual_studio", fallback="2019")
        self.mkdocs_path = config.get("mkdocs", "path", fallback=".")
        self.mkdocs_auto_deploy = config.get("mkdocs", "auto_deploy", fallback="false").replace(" ", "").lower() != "false"
        self.mkdocs_include_pdf = config.get("mkdocs", "include_pdf", fallback="false").replace(" ", "").lower() != "false"
        self.mkdocs_create_zip = config.get("mkdocs", "create_zip", fallback="false").replace(" ", "").lower() != "false"
        self.github_create_release = config.get("github", "create_release", fallback="false").replace(" ", "").lower() != "false"
        self.github_owner = config.get("github", "owner", fallback="")
        self.github_repo = config.get("github", "repo", fallback="")
        self.github_token = config.get("github", "token", fallback="")
        self.github_commit = config.get("github", "commit", fallback="")
        self.github_release_notes = config.get("github", "release_notes", fallback="")
        self.task_pre = config.get("tasks", "pre", fallback=None)
        self.task_post = config.get("tasks", "post", fallback=None)
        self.verify()

    def verify(self):
        """ Verify the values extracted from the configuration file """
        if not self.unreal_install_dir or self.unreal_install_dir.isspace():
            raise Exception("Unreal Engine installation directory not specified in config file")
        self.unreal_install_dir = os.path.abspath(self.unreal_install_dir)
        if not os.path.exists(self.unreal_install_dir):
            raise Exception("Invalid Unreal Engine installation directory")
        if not self.output or self.output.isspace():
            raise Exception("Output path not specified in config file")
        self.output = os.path.abspath(self.output)
        if os.path.exists(self.output):
            shutil.rmtree(self.output)
        os.makedirs(self.output, exist_ok=True)
        if self.plugin_path and not self.plugin_path.isspace():
            self.plugin_path = os.path.abspath(self.plugin_path)
            if not os.path.exists(self.plugin_path):
                raise Exception("Plugin does not exist")
            if not self.plugin_path.endswith(".uplugin"):
                raise Exception("Invalid plugin path. Must end with .uplugin")
            if not self.plugin_unreal_versions:
                raise Exception("No Unreal Engine versions specified in config file")
            for unreal_version in self.plugin_unreal_versions:
                if not os.path.exists(os.path.join(self.unreal_install_dir, f"UE_{unreal_version}")):
                    raise Exception(f"Unreal Engine {unreal_version} is not installed")
            if not self.plugin_visual_studio.isdigit():
                raise Exception("Invalid Visual Studio version number provided. Only integers are allowed")
        if self.project_path and not self.project_path.isspace():
            self.project_path = os.path.abspath(self.project_path)
            if not os.path.exists(self.project_path):
                raise Exception("Project does not exist")
            if not self.project_path.endswith(".uproject"):
                raise Exception("Invalid project path. Must end with .uproject")
            if not self.project_platforms:
                raise Exception("No Unreal Engine versions specified in config file")
            for platform in self.project_platforms:
                if platform not in [ "Win64", "HoloLens", "Mac", "IOS", "Android", "Linux", "LinuxArm64", "TVOS"]:
                    raise Exception(f"{platform} is not a supported platform. Only Win64, HoloLens, Mac, IOS, Android, Linux, LinuxArm64 and TVOS is supported")
            if not self.project_unreal_version or self.project_unreal_version.isspace():
                raise Exception("No Unreal Engine versions specified in config file")
            if not os.path.exists(os.path.join(self.unreal_install_dir, f"UE_{self.project_unreal_version}")):
                raise Exception(f"Unreal Engine {self.project_unreal_version} is not installed")
        if self.mkdocs_auto_deploy or self.mkdocs_include_pdf or self.mkdocs_create_zip:
            self.mkdocs_path = os.path.abspath(self.mkdocs_path)
            if not os.path.exists(os.path.join(self.mkdocs_path, "mkdocs.yml")):
                raise Exception("Mkdocs integration is enabled but the mkdocs.yml file could not be found")
        if self.github_create_release:
            if not self.github_owner or self.github_owner.isspace():
                raise Exception("Github release is enabled but owner is not specified in config file")
            if not self.github_repo or self.github_repo.isspace():
                raise Exception("Github release is enabled but repo is not specified in config file")
            if not self.github_token or self.github_token.isspace():
                raise Exception("Github release is enabled but token is not specified in config file")
            if not self.github_commit or self.github_commit.isspace():
                raise Exception("Github release is enabled but commit is not specified in config file")
            if not self.github_release_notes or self.github_release_notes.isspace():
                raise Exception("Github release is enabled but release notes file is not specified in config file")
            self.github_release_notes = os.path.abspath(self.github_release_notes)
            if not os.path.exists(self.github_release_notes):
                raise Exception("Release notes file could not be found")
        if self.task_pre and not self.task_pre.isspace():
            self.task_pre = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\", self.task_pre))
            if not os.path.exists(self.task_pre):
                raise Exception(f"Pre-task {self.task_pre} does not exist")
            if not self.task_pre.endswith(".py"):
                raise Exception("Invalid pre-task. Only Python scripts are currently supported")
        if self.task_post and not self.task_post.isspace():
            self.task_post = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\", self.task_post))
            if not os.path.exists(self.task_post):
                raise Exception(f"Post-task {self.task_post} does not exist")
            if not self.task_post.endswith(".py"):
                raise Exception("Invalid post-task. Only Python scripts are currently supported")
