# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import json


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
