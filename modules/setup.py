# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import subprocess

dependencies = [ 'argparse', 'configparser', 'requests' ]

def run_setup():
    """ Ensure that all the dependencies are installed """
    for dependency in dependencies:
        if subprocess.run(f'python -c "import {dependency}"', capture_output=True).returncode == 0:
            continue
        print(f"Error: {dependency} is not installed")
        install = input(f"Do you want to install {dependency} (yes/no): ")
        print(install)
        if install.lower().strip() != "yes" and install.lower().strip() != "y":
            raise Exception("Failed to run Unreal Packager. Please install the missing dependencies and try again")
        if os.system(f"pip install {dependency}") != 0:
            raise Exception(f"Failed to install {dependency}")
