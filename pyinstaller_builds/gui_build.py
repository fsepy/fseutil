# -*- coding: utf-8 -*-
import os
import subprocess


def build_gui():

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    cmd_option_list = [
        '-n "OFR B4 BR187 Calculator"',
        "--noconsole",
        "--onefile",
        "--windowed",
        "--icon=" + os.path.realpath(os.path.join("etc", "ofr-colour-618_618.ico")),
    ]
    cmd_script = "gui.py"

    cmd_pyinstaller = "pyinstaller"
    cmd_options = " ".join(cmd_option_list)
    cmd_options = cmd_options + " " if len(cmd_options) > 0 else ""

    cmd = f"{cmd_pyinstaller} {cmd_options}{cmd_script}"

    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    build_gui()
