# -*- coding: utf-8 -*-
import os
import subprocess


def build_gui(app_name: str = 'OFR BOX', fp_target_py: str = 'gui.py', options: list = None):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    cmd_option_list = [
        f'-n "{app_name}"',
        "--icon=" + os.path.realpath(os.path.join("etc", "ofr_logo_1_80_80.ico")),
    ]
    if options:
        cmd_option_list.extend(options)

    cmd_options = " ".join(cmd_option_list)
    cmd_options = cmd_options + " " if len(cmd_options) > 0 else ""

    cmd = f"pyinstaller {cmd_options}{fp_target_py}"

    subprocess.call(cmd)


if __name__ == "__main__":
    build_gui(
        options=[
            "--noconsole",  # disable console display
            "--onedir",  # output unpacked dist to one directory, including an .exe file
            "--windowed",  # make it a windowed application
            "--noconfirm",  # replace output directory without asking for confirmation
            "--clean",  # clean pyinstaller cache and remove temporary files
        ]
    )
    build_gui(
        options=[
            "--noconsole",  # disable console display
            "--onefile",  # output one .exe file
            "--windowed",  # make it a windowed application
            "--noconfirm",  # replace output directory without asking for confirmation
        ]
    )
