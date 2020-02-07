# -*- coding: utf-8 -*-
import os
import sys
import subprocess


def build_gui(app_name: str = 'FSEUTIL', fp_target_py: str = 'gui.py', options: list = None):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    cmd_option_list = [
        f'-n={app_name}',
        "--icon=" + os.path.realpath(os.path.join("etc", "ofr_logo_1_80_80.ico")),
    ]
    if options:
        cmd_option_list.extend(options)

    # add encryption to pyz
    try:
        with open('key.txt', 'r') as f:
            key = f.read()
            if len(key) > 0:
                cmd_option_list.append(f'--key={key}')
                print('Encryption is enabled.')
            else:
                print('Encryption is not enabled.')
    except FileNotFoundError:
        print('Encryption is not enabled.')

    cmd = ['pyinstaller'] + cmd_option_list + [fp_target_py]
    print('\n'*5, ' '.join(cmd))

    with open('gui_build.log', 'wb') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c.decode('utf-8'))
            f.write(c)


if __name__ == "__main__":
    build_gui(
        options=[
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
