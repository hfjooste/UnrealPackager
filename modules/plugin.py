# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import json


class Plugin:
    """ Class containing information about the plugin """
    name = ""
    path = ""
    version = ""
    build_path_without_ue_version = ""

    def __init__(self, plugin, output):
        with open(plugin) as plugin_file:
            plugin_data = json.load(plugin_file)
        self.name = plugin_data['FriendlyName'].replace(" ", "")
        self.version = plugin_data['VersionName']
        self.path = plugin
        self.build_path_without_ue_version = os.path.join(output, f"{self.name}-UE-v{self.version}")

    def getbuildpath(self, unreal_version):
        """ Get the output directory for the build using a specific version of Unreal Engine """
        return self.build_path_without_ue_version.replace("-UE-v", f"-UE{unreal_version}-v")
