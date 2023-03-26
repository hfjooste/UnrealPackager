import os
import shutil
import requests
import subprocess
from modules.packager import Packager
from modules.plugin import Plugin
from modules.project import Project


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

def save_docs_pdf(config):
    """ Save the documentation PDF """
    if not config.mkdocs_include_pdf:
        return
    print("Copying documentation PDF to output directory")
    pdf = os.path.join(config.mkdocs_path, "site\\pdf\\document.pdf")
    if not os.path.exists(pdf):
        raise Exception("PDF file could not be found")
    if os.path.exists(plugin.documentation_pdf_path):
        os.remove(plugin.documentation_pdf_path)
    shutil.copy2(pdf, plugin.documentation_pdf_path)

def create_docs_zip(config):
    """ Create a ZIP of the documentation website """
    if not config.mkdocs_create_zip:
        return
    print("Creating ZIP for documentation website")
    site = os.path.join(config.mkdocs_path, "site")
    if not os.path.exists(site):
        raise Exception("Documentation could not be found")
    if os.path.exists(plugin.documentation_website_path):
        os.remove(plugin.documentation_website_path)
    shutil.make_archive(site, "zip", site)
    shutil.move(f"{site}.zip", plugin.documentation_website_path)

def create_release(args, config):
    """ Create a release on GitHub """
    if not config.github_create_release:
        return
    print("\nCreating new release on GitHub")
    with open(config.github_release_notes, mode="r") as release_notes_file:
        release_notes = release_notes_file.read()
    url = f"https://api.github.com/repos/{config.github_owner}/{config.github_repo}/releases"
    version = plugin.version
    if args.github_version and not args.github_version.isspace():
        version = args.github_version.strip()
    tag = plugin.version
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