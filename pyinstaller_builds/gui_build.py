# -*- coding: utf-8 -*-
import os
import subprocess


def build_gui(app_name: str = 'OFRUTIL', fp_target_py: str = 'gui.py'):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    cmd_option_list = [
        f'-n "{app_name}"',
        "--noconsole",
        "--onefile",
        "--windowed",
        "--icon=" + os.path.realpath(os.path.join("etc", "ofr-colour-618_618.ico")),
    ]

    cmd_options = " ".join(cmd_option_list)
    cmd_options = cmd_options + " " if len(cmd_options) > 0 else ""

    cmd = f"pyinstaller {cmd_options}{fp_target_py}"

    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    build_gui()
