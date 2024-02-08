import PyQt5
import minecraft_launcher_lib
import uuid
import random_username
import subprocess

version = input(f'Enter Minecraft version: ')
username = input(f'Enter Username: ')
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'deflauncher')

minecraft_launcher_lib.install.install_minecraft_version(versionid=version, minecraft_directory=minecraft_directory)

options = {
    'username': username,
    'uuid': '',
    'token': ''
}
subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=version, minecraft_directory=minecraft_directory, options=options))