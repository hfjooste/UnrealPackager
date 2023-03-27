# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

import os
import json
import shutil
import requests
import subprocess
from modules.packager import Packager
from modules.plugin import Plugin
from modules.project import Project


def run_pre_task(config):
    """ Run the pre-task """
    if config.task_pre and not config.task_pre.isspace():
        print("Running pre-task")
        os.system(f"python \"{config.task_pre}\"")

def run_post_task(config):
    """ Run the post-task """
    if config.task_post and not config.task_post.isspace():
        print("Running post-task")
        os.system(f"python \"{config.task_post}\"")


def package_plugin(config):
    """ Package the plugin """
    if config.plugin_path and not config.plugin_path.isspace():
        plugin = Plugin(config.plugin_path, config.output)
        for unreal_version in config.plugin_unreal_versions:
            packager = Packager(config.unreal_install_dir, unreal_version)
            packager.package_plugin(plugin, config.plugin_visual_studio)

def package_project(config):
    """ Package the project """
    if config.project_path and not config.project_path.isspace():
        project = Project(config.project_path, config.output)
        for platform in config.project_platforms:
            packager = Packager(config.unreal_install_dir, config.project_unreal_version)
            packager.package_project(project, platform)

def deploy_docs(config):
    """ Deploy the documentation """
    if config.mkdocs_auto_deploy:
        print("Deploying documentation")
        subprocess.run(rf'mkdocs gh-deploy --force --config-file "{os.path.join(config.mkdocs_path, "mkdocs.yml")}"')

def get_documentation_pdf_path(config):
    """ Get the path to the documentation PDF """
    if config.plugin_path and not config.plugin_path.isspace():
        plugin = Plugin(config.plugin_path, config.output)
        return os.path.join(config.output, f"{plugin.name}Documentation-v{plugin.version}.pdf")
    if config.project_path and not config.project_path.isspace():
        project = Project(config.project_path, config.output)
        return os.path.join(config.output, f"{project.name}Documentation-v{project.version}.pdf")
    return os.path.join(config.output, f"Documentation.pdf")

def get_documentation_website_path(config):
    """ Get the path to the documentation website archive """
    if config.plugin_path and not config.plugin_path.isspace():
        plugin = Plugin(config.plugin_path, config.output)
        return os.path.join(config.output, f"{plugin.name}Documentation-v{plugin.version}.zip")
    if config.project_path and not config.project_path.isspace():
        project = Project(config.project_path, config.output)
        return os.path.join(config.output, f"{project.name}Documentation-v{project.version}.zip")
    return os.path.join(config.output, f"Documentation.zip")

def save_docs_pdf(config):
    """ Save the documentation PDF """
    if not config.mkdocs_include_pdf:
        return
    print("Copying documentation PDF to output directory")
    pdf = os.path.join(config.mkdocs_path, "site\\pdf\\document.pdf")
    if not os.path.exists(pdf):
        raise Exception("PDF file could not be found")
    documentation_pdf_path = get_documentation_pdf_path(config)
    if os.path.exists(documentation_pdf_path):
        os.remove(documentation_pdf_path)
    shutil.copy2(pdf, documentation_pdf_path)

def create_docs_zip(config):
    """ Create a ZIP of the documentation website """
    if not config.mkdocs_create_zip:
        return
    print("Creating ZIP for documentation website")
    site = os.path.join(config.mkdocs_path, "site")
    if not os.path.exists(site):
        raise Exception("Documentation could not be found")
    documentation_website_path = get_documentation_website_path(config)
    if os.path.exists(documentation_website_path):
        os.remove(documentation_website_path)
    shutil.make_archive(site, "zip", site)
    shutil.move(f"{site}.zip", documentation_website_path)

def create_release(args, config):
    """ Create a release on GitHub """
    if not config.github_create_release:
        return
    print("\nCreating new release on GitHub")
    with open(config.github_release_notes, mode="r") as release_notes_file:
        release_notes = release_notes_file.read()
    url = f"https://api.github.com/repos/{config.github_owner}/{config.github_repo}/releases"
    plugin = None
    if config.plugin_path and not config.plugin_path.isspace():
        plugin = Plugin(config.plugin_path, config.output)
    project = None
    if config.project_path and not config.project_path.isspace():
        project = Project(config.project_path, config.output)
    release = ""
    if plugin != None:
        release = plugin.version
    elif project != None:
        release = project.version
    version = release
    if args.github_version and not args.github_version.isspace():
        version = args.github_version.strip()
    tag = release
    if args.github_tag and not args.github_tag.isspace():
        tag = args.github_tag.strip()
    commit = config.github_commit
    if args.github_commit and not args.github_commit.isspace():
        commit = args.github_commit.strip()
    data = {
        "tag_name" : tag,
        "target_commitish": config.github_commit,
        "name" : f"Version {version}",
        "body" : release_notes,
        "prerelease" : args.github_prerelease
    }
    headers = {
        'Accept' : 'application/vnd.github+json',
        'Authorization' : f'Bearer {config.github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
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
            headers = {
                'Accept' : 'application/vnd.github+json',
                'Authorization' : f'Bearer {config.github_token}',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/octet-stream'
            }
            response = requests.post(url, data=content, headers=headers)
            if not response.ok:
                print(response.content)
                raise Exception(f"Failed to upload {file_name}")
    release_url = release['html_url']
    print(f"Release created: {release_url}")