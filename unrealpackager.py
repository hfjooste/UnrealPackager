# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import sys
import json
import shutil
import subprocess
import configparser


class Config:
    """ Helper class used to read the config file, extract values and verify the configuration """
    unreal_install_dir = ""
    unreal_versions = []
    visual_studio = ""
    plugin = ""
    output = ""
    create_zip = True

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("unrealpackager.conf")
        self.unreal_install_dir = config.get("environment", "unreal_install_dir", fallback="")
        self.unreal_versions = list(filter(None, config.get("environment", "unreal_versions", fallback="").replace(" ", "").split(",")))
        self.visual_studio = config.get("environment", "visual_studio", fallback="2019")
        self.plugin = config.get("project", "plugin", fallback="")
        self.output = config.get("project", "output", fallback="")
        self.create_zip = config.get("project", "create_zip", fallback="true").replace(" ", "").lower() != "false"

    def verify(self):
        """ Verify the values extracted from the configuration file """
        if not self.unreal_install_dir or self.unreal_install_dir.isspace():
            raise Exception("Unreal Engine installation directory not specified in config file")
        self.unreal_install_dir = os.path.abspath(self.unreal_install_dir)
        if not os.path.exists(self.unreal_install_dir):
            raise Exception("Invalid Unreal Engine installation directory")
        if not self.unreal_versions:
            raise Exception("No Unreal Engine versions specified in config file")
        for unreal_version in self.unreal_versions:
            if not os.path.exists(os.path.join(self.unreal_install_dir, f"UE_{unreal_version}")):
                raise Exception(f"Unreal Engine {unreal_version} is not installed")
        if not self.visual_studio.isdigit():
            raise Exception("Invalid Visual Studio version number provided. Only integers are allowed")
        if not self.plugin or self.plugin.isspace():
            raise Exception("Plugin path not specified in config file")
        self.plugin = os.path.abspath(self.plugin)
        if not os.path.exists(self.plugin):
            raise Exception("Plugin does not exist")
        if not self.plugin.endswith(".uplugin"):
            raise Exception("Invalid plugin path. Must end with .uplugin")
        if not self.output or self.output.isspace():
            raise Exception("Output path not specified in config file")
        self.output = os.path.abspath(self.output)


class UnrealPackager:
    """ Automate packaging an Unreal Engine plugin """
    unreal_install_dir = ""
    unreal_version = ""
    visual_studio = ""

    def __init__(self, unreal_install_dir, unreal_version, visual_studio):
        self.unreal_install_dir = unreal_install_dir
        self.unreal_version = unreal_version
        self.visual_studio = visual_studio

    def package(self, plugin, output, create_zip):
        """ Package the plugin """
        with open(plugin) as plugin_file:
            plugin_data = json.load(plugin_file)
        name = plugin_data['FriendlyName'].replace(" ", "")
        version = plugin_data['VersionName']
        final_output = os.path.join(output, f"{name}-UE{unreal_version}-v{version}")
        print()
        print(f"Packaging plugin using Unreal Engine {unreal_version}")
        print(f"Plugin : {plugin}")
        print(f"Output : {final_output}")
        if os.path.exists(final_output):
            shutil.rmtree(final_output)
        script = rf'{self.unreal_install_dir}\\UE_{self.unreal_version}\\Engine\\Build\\BatchFiles\\RunUAT.bat'
        command = rf'"{script}" BuildPlugin -Plugin="{plugin}" -Package="{final_output}" -VS{self.visual_studio} -Rocket'
        subprocess.run(command)
        if create_zip:
            if os.path.exists(f"{final_output}.zip"):
                os.remove(f"{final_output}.zip")
            shutil.make_archive(final_output, "zip", final_output)


config = Config()
config.verify()

print()
print("==============================================")
print("| Unreal Packager v1.0.0                     |")
print("| Created by Henry Jooste                    |")
print("| https://github.com/hfjooste/UnrealPackager |")
print("==============================================")
print()

for unreal_version in config.unreal_versions:
    packager = UnrealPackager(config.unreal_install_dir, unreal_version, config.visual_studio)
    packager.package(config.plugin, config.output, config.create_zip)