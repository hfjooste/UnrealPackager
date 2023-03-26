# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import configparser


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
