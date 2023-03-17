# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import json
import shutil
import requests
import subprocess
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


class Plugin:
    """ Class containing information about the plugin """
    path = ""
    version = ""
    build_path_without_ue_version = ""
    documentation_pdf_path = ""
    documentation_website_path = ""

    def __init__(self, plugin, output):
        with open(plugin) as plugin_file:
            plugin_data = json.load(plugin_file)
        name = plugin_data['FriendlyName'].replace(" ", "")
        self.version = plugin_data['VersionName']
        self.path = plugin
        self.build_path_without_ue_version = os.path.join(output, f"{name}-UE-v{self.version}")
        self.documentation_pdf_path = os.path.join(output, f"{name}Documentation-v{self.version}.pdf")
        self.documentation_website_path = os.path.join(output, f"{name}Documentation-v{self.version}.zip")

    def getbuildpath(self, unreal_version):
        """ Get the output directory for the build using a specific version of Unreal Engine """
        return self.build_path_without_ue_version.replace("-UE-v", f"-UE{unreal_version}-v")


class Project:
    """ Class containing information about the project """
    path = ""
    name = ""
    version = ""
    build_path = ""

    def __init__(self, project, output):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(project), "Config", "DefaultGame.ini"))
        self.path = project
        self.name = config.get("/Script/EngineSettings.GeneralProjectSettings", "ProjectName", fallback="UnrealProject").replace(" ", "")
        self.version = config.get("/Script/EngineSettings.GeneralProjectSettings", "ProjectVersion", fallback="1.0.0")
        self.build_path = os.path.join(output, f"{self.name}-v{self.version}-PLATFORM_ID")

    def getbuildpath(self, platform):
        """ Get the output directory for the build using a specific platform """
        return self.build_path.replace("-PLATFORM_ID", f"-{platform}")

class UnrealPackager:
    """ Automate packaging an Unreal Engine projects and plugins """
    unreal_install_dir = ""
    unreal_version = ""

    def __init__(self, unreal_install_dir, unreal_version):
        self.unreal_install_dir = unreal_install_dir
        self.unreal_version = unreal_version

    def package_plugin(self, plugin, visual_studio):
        """ Package the plugin """
        output = plugin.getbuildpath(self.unreal_version)
        print()
        print(f"Packaging plugin using Unreal Engine {self.unreal_version}")
        print(f"Plugin : {plugin.path}")
        print(f"Output : {output}")
        print()
        if os.path.exists(output):
            shutil.rmtree(output)
        script = rf'{self.unreal_install_dir}\\UE_{self.unreal_version}\\Engine\\Build\\BatchFiles\\RunUAT.bat'
        command = rf'"{script}" BuildPlugin -Plugin="{plugin.path}" -Package="{output}" -VS{visual_studio} -Rocket'
        print(f"Executing command : {command}")
        print()
        subprocess.run(command)
        if os.path.exists(f"{output}.zip"):
            os.remove(f"{output}.zip")
        shutil.make_archive(output, "zip", output)
            

    def package_project(self, project, platform):
        """ Package the project """
        output = project.getbuildpath(platform)
        print()
        print(f"Packaging project using Unreal Engine {self.unreal_version}")
        print(f"Plugin : {project.path}")
        print(f"Output : {output}")
        print()
        if os.path.exists(output):
            shutil.rmtree(output)
        script = rf'{self.unreal_install_dir}\\UE_{self.unreal_version}\\Engine\\Build\\BatchFiles\\RunUAT.bat'
        command = rf'"{script}" BuildCookRun -project="{project.path}" -targetplatform={platform} -cook -allmaps -build -stage -pak -archive -archivedirectory="{output}"'
        print(f"Executing command : {command}")
        subprocess.run(command)
        if os.path.exists(f"{output}.zip"):
            os.remove(f"{output}.zip")
        shutil.make_archive(output, "zip", output)


config = Config()
config.verify()

print()
print("==============================================")
print("| Unreal Packager v2.0.0                     |")
print("| Created by Henry Jooste                    |")
print("| https://github.com/hfjooste/UnrealPackager |")
print("==============================================")
print()

if config.plugin_path and not config.plugin_path.isspace():
    plugin = Plugin(config.plugin_path, config.output)
    for unreal_version in config.plugin_unreal_versions:
        packager = UnrealPackager(config.unreal_install_dir, unreal_version)
        packager.package_plugin(plugin, config.plugin_visual_studio)

if config.project_path and not config.project_path.isspace():
    project = Project(config.project_path, config.output)
    for platform in config.project_platforms:
        packager = UnrealPackager(config.unreal_install_dir, config.project_unreal_version)
        packager.package_project(project, platform)

if config.mkdocs_auto_deploy:
    print("Deploying documentation")
    subprocess.run(rf'mkdocs gh-deploy --force --config-file "{os.path.join(config.mkdocs_path, "mkdocs.yml")}"')

if config.mkdocs_include_pdf:
    print("Copying documentation PDF to output directory")
    pdf = os.path.join(config.mkdocs_path, "site\\pdf\\document.pdf")
    if not os.path.exists(pdf):
        raise Exception("PDF file could not be found")
    if os.path.exists(plugin.documentation_pdf_path):
        os.remove(plugin.documentation_pdf_path)
    shutil.copy2(pdf, plugin.documentation_pdf_path)

if config.mkdocs_create_zip:
    print("Creating ZIP for documentation website")
    site = os.path.join(config.mkdocs_path, "site")
    if not os.path.exists(site):
        raise Exception("Documentation could not be found")
    if os.path.exists(plugin.documentation_website_path):
        os.remove(plugin.documentation_website_path)
    shutil.make_archive(site, "zip", site)
    shutil.move(f"{site}.zip", plugin.documentation_website_path)

if config.github_create_release:
    print()
    print("Creating new release on GitHub")
    with open(config.github_release_notes, mode="r") as release_notes_file:
        release_notes = release_notes_file.read()
    url = f"https://api.github.com/repos/{config.github_owner}/{config.github_repo}/releases"
    data = { "tag_name" : plugin.version, "target_commitish": config.github_commit, "name" : f"Version {plugin.version}", "body" : release_notes }
    headers = { 'Accept' : 'application/vnd.github+json', 'Authorization' : f'Bearer {config.github_token}', 'X-GitHub-Api-Version': '2022-11-28'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if not response.ok:
        print(response.content)
        raise Exception("Failed to create new release on Github")
    release = json.loads(response.content)
    release_id = release['id']
    for file_name in os.listdir(config.output):
        file_path = os.path.join(config.output, file_name)
        if os.path.isfile(file_path):
            print(f"Uploading {file_name}")
            with open(file_path, mode="rb") as release_file:
                content = release_file.read()
            url = f'https://uploads.github.com/repos/{config.github_owner}/{config.github_repo}/releases/{release_id}/assets?name={file_name}'
            headers = { 'Accept' : 'application/vnd.github+json', 'Authorization' : f'Bearer {config.github_token}', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/octet-stream' }
            response = requests.post(url, data=content, headers=headers)
            if not response.ok:
                print(response.content)
                raise Exception(f"Failed to upload {file_name}")
    release_url = release['html_url']
    print(f"Release created: {release_url}")