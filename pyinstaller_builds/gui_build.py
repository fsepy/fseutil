# -*- coding: utf-8 -*-
import os
import subprocess


def build_gui():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(os.getcwd())

    cmd_pyinstaller = "python -m PyInstaller"
    cmd_pyinstaller = "pyinstaller"

    cmd_option_list = [
        '-n "OFR B4 BR187 Calculator"',
        "--noconsole",
        "--onefile",
        "--windowed",
        "--icon="
        + os.path.realpath(os.path.join("etc", "ofr-colour-618_618.ico")),
    ]
    cmd_extra_files_list = []
    cmd_script = "fse_thermal_radiation_gui.py"

    cmd_options = " ".join(cmd_option_list)
    cmd_extra_files = " ".join(cmd_extra_files_list)

    cmd_options = cmd_options + " " if len(cmd_options) > 0 else ""
    cmd_extra_files = cmd_extra_files + " " if len(cmd_extra_files) > 0 else ""

    cmd = f"{cmd_pyinstaller} {cmd_options}{cmd_extra_files}{cmd_script}"

    print(cmd)
    subprocess.call(cmd)


if __name__ == "__main__":
    build_gui()
