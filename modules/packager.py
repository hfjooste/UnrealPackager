# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import shutil
import subprocess

class Packager:
    """ Automate packaging an Unreal Engine projects and plugins """
    unreal_install_dir = ""
    unreal_version = ""

    def __init__(self, unreal_install_dir, unreal_version):
        self.unreal_install_dir = unreal_install_dir
        self.unreal_version = unreal_version

    def package_plugin(self, plugin, visual_studio):
        """ Package the plugin """
        output = plugin.getbuildpath(self.unreal_version)
        print(f"\nPackaging plugin using Unreal Engine {self.unreal_version}")
        print(f"Plugin : {plugin.path}")
        print(f"Output : {output}")
        if os.path.exists(output):
            shutil.rmtree(output)
        script = rf'{self.unreal_install_dir}\\UE_{self.unreal_version}\\Engine\\Build\\BatchFiles\\RunUAT.bat'
        command = rf'"{script}" BuildPlugin -Plugin="{plugin.path}" -Package="{output}" -VS{visual_studio} -Rocket'
        print(f"\nExecuting command : {command}\n")
        subprocess.run(command)
        if os.path.exists(f"{output}.zip"):
            os.remove(f"{output}.zip")
        shutil.make_archive(output, "zip", output)
            

    def package_project(self, project, platform):
        """ Package the project """
        output = project.getbuildpath(platform)
        print(f"\nPackaging project using Unreal Engine {self.unreal_version}")
        print(f"Project : {project.path}")
        print(f"Output : {output}")
        if os.path.exists(output):
            shutil.rmtree(output)
        script = rf'{self.unreal_install_dir}\\UE_{self.unreal_version}\\Engine\\Build\\BatchFiles\\RunUAT.bat'
        command = rf'"{script}" BuildCookRun -project="{project.path}" -targetplatform={platform} -cook -allmaps -build -stage -pak -archive -archivedirectory="{output}"'
        print(f"\nExecuting command : {command}\n")
        subprocess.run(command)
        if os.path.exists(f"{output}.zip"):
            os.remove(f"{output}.zip")
        shutil.make_archive(output, "zip", output)
