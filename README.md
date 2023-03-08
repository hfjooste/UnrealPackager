# Unreal Packager
Automate packaging Unreal Engine plugins for multiple engine versions

## Requirements
Python 3 is required to run the tool. You can find more information on how to set it up here: https://www.python.org.

## Supported Unreal Engine Versions
Only Unreal Engine 5.0 and 5.1 is supported, but it should work on earlier versions (not tested)

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
        <td>unreal_versions</td>
        <td>environment</td>
        <td>A comma-seperated list of all Unreal Engine versions used to build the plugin</td>
    </tr>
    <tr>
        <td>visual_studio</td>
        <td>environment</td>
        <td>The version of Visual Studio used to compile the plugin (VS2019 is used by default)</td>
    </tr>
    <tr>
        <td>plugin</td>
        <td>project</td>
        <td>The path to the uplugin file</td>
    </tr>
    <tr>
        <td>output</td>
        <td>project</td>
        <td>The path where the packaged builds will be stored</td>
    </tr>
    <tr>
        <td>create_zip</td>
        <td>project</td>
        <td>Should the release also be added to a ZIP file? (default is True)</td>
    </tr>
<table>

## Using the tool
<ol>
    <li>Download the latest release from <a href="https://github.com/hfjooste/UnrealPackager/releases" target="_blank">GitHub</a></li>
    <li>Copy the <code>unrealpackager.py</code> and <code>unrealpackager.conf</code> files to your project (optional)
    <li>Update the <code>unrealpackager.conf</code> with your project details</li>
    <li>Run the tool: <code>python3 unrealpackager.py</code></li>
</ol>

## Support
If you have any questions, feel free to contact me through <a href="https://mastodon.social/@hfjooste" target="_blank">Mastodon</a> or send me an email at <a href="mailto:henryjooste95@gmail.com?subject=Unreal%20Packager">henryjooste95@gmail.com</a>. You can also use the Discussions or Issues tab on GitHub to discuss problems/features or report any issues