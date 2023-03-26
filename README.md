# Unreal Packager
Automate packaging Unreal Engine projects and plugins. It also supports multiple platforms (projects) and multiple multiple engine versions (plugins). The tool can also be used to deploy documentation using Mkdocs and upload new releases to GitHub

## Requirements
Python 3 is required to run the tool. You can find more information on how to set it up here: https://www.python.org.

Unreal Packager relies on a few external packages. It will automatically check the dependencies when you run the script and offer to install the missing dependencies. Pip is required to install these packages. You can find more information on how to set it up here: https://pip.pypa.io/en/stable/installation/

## Supported Unreal Engine Versions
Only Unreal Engine 5.0 and 5.1 is supported, but it should work on earlier versions (not tested)

## Arguments
The following arguments can be specified to override the values specified in the config file:
<table>
    <tr>
        <th>Argument</th>
        <th>Optional</th>
        <th>Description</th>
        <th>Default Value</th>
    </tr>
    <tr>
        <td>--help</td>
        <td>Yes</td>
        <td>Get a list of all available arguments</td>
        <td></td>
    </tr>
    <tr>
        <td>--version</td>
        <td>Yes</td>
        <td>Check the version number of Unreal Packager</td>
        <td></td>
    </tr>
    <tr>
        <td>--gh-version</td>
        <td>Yes</td>
        <td>Specify the version used on GitHub</td>
        <td>Extracted from project file</td>
    </tr>
    <tr>
        <td>--gh-tag</td>
        <td>Yes</td>
        <td>Specify the tag used on GitHub</td>
        <td>Extracted from project file</td>
    </tr>
    <tr>
        <td>--gh-commit</td>
        <td>Yes</td>
        <td>Specify the commit or branch used when creating the tag on GitHub</td>
        <td>Extracted from config file</td>
    </tr>
    <tr>
        <td>--gh-prerelease</td>
        <td>Yes</td>
        <td>Should the release be marked as a pre-release on GitHub?</td>
        <td>True</td>
    </tr>
</table>

## Configuration
The configuration for the tool is stored in the <code>unrealpackager.conf</code> file. The following settings can be configured in this file:
<table>
    <tr>
        <th>Configuration</th>
        <th>Section</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>unreal_install_dir</td>
        <td>environment</td>
        <td>The directory where all Unreal Engine builds are installed</td>
    </tr>
    <tr>
        <td>output</td>
        <td>environment</td>
        <td>The path where the packaged builds will be stored</td>
    </tr>
    <tr>
        <td>path</td>
        <td>project</td>
        <td>The path to the uproject file</td>
    </tr>
    <tr>
        <td>platforms</td>
        <td>project</td>
        <td>A comma-seperated list of all supported platforms (Win64, HoloLens, Mac, IOS, Android, Linux, LinuxArm64 and TVOS)</td>
    </tr>
    <tr>
        <td>unreal_version</td>
        <td>project</td>
        <td>The version of Unreal Engine used to build the project</td>
    </tr>
    <tr>
        <td>path</td>
        <td>plugin</td>
        <td>The path to the uplugin file</td>
    </tr>
    <tr>
        <td>unreal_versions</td>
        <td>plugin</td>
        <td>A comma-seperated list of all Unreal Engine versions used to build the plugin</td>
    </tr>
    <tr>
        <td>visual_studio</td>
        <td>plugin</td>
        <td>The version of Visual Studio used to compile the plugin (VS2019 is used by default)</td>
    </tr>
    <tr>
        <td>path</td>
        <td>mkdocs</td>
        <td>The path to the directory where the mkdocs.yml file is stored</td>
    </tr>
    <tr>
        <td>auto_deploy</td>
        <td>mkdocs</td>
        <td>Should the latest documentation automatically be deployed using the <code>mkdocs gh-deploy</code> command? (default is False)</td>
    </tr>
    <tr>
        <td>include_pdf</td>
        <td>mkdocs</td>
        <td>Should the PDF documentation be included in the output directory? (default is False)</td>
    </tr>
    <tr>
        <td>create_zip</td>
        <td>mkdocs</td>
        <td>Should the documentation also be added to a ZIP file? (default is False)</td>
    </tr>
    <tr>
        <td>create_release</td>
        <td>github</td>
        <td>Should a new release automatically be created on GitHub (default is False)</td>
    </tr>
    <tr>
        <td>owner</td>
        <td>github</td>
        <td>The account owner of the repo where the new release will be created (not case sensitive)</td>
    </tr>
    <tr>
        <td>repo</td>
        <td>github</td>
        <td>The name of repository where the release will be created (not case sensitive)</td>
    </tr>
    <tr>
        <td>token</td>
        <td>github</td>
        <td>The GitHub authorization token that will be used to create the new release</td>
    </tr>
    <tr>
        <td>commit</td>
        <td>github</td>
        <td>Specifies the commitish value that determines where the Git tag is created from. Can be any branch or commit SHA</td>
    </tr>
    <tr>
        <td>release_notes</td>
        <td>github</td>
        <td>A path to the release notes used for the new release</td>
    </tr>
<table>

## Github API Token
You need to create a new token before you can automate releases on GitHub. You can follow this guide: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token. It's important that the Contents repository permission is enabled, otherwise all releases will fail

## Using the tool
<ol>
    <li>Download the latest release from <a href="https://github.com/hfjooste/UnrealPackager/releases" target="_blank">GitHub</a> or add the project as a submodule (<code>git submodule add git@github.com:hfjooste/UnrealPackager.git</code>)</li>
    <li>Update the <code>unrealpackager.conf</code> with your project details</li>
    <li>Run the tool: <code>python unrealpackager.py</code></li>
</ol>

## Support
If you have any questions, feel free to contact me through <a href="https://twitter.com/hfjooste" target="_blank">Twitter</a> or <a href="https://mastodon.social/@hfjooste" target="_blank">Mastodon</a>. You can also send me an email at <a href="mailto:henryjooste95@gmail.com?subject=Unreal%20Packager">henryjooste95@gmail.com</a>