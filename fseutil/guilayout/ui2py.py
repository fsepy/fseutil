

def ui2py():
    import os
    import subprocess

    list_ui_file_names = [
        'main.ui',
        'dialog_1_1_adb_datasheet_1.ui',
        'dialog_1_11_heat_detector_activation.ui',
        'dialog_4_1_br187_parallel_simple.ui',
        'dialog_4_2_br187_perpendicular_simple.ui',
        'dialog_4_3_br187_parallel_complex.ui',
        'dialog_4_4_br187_perpendicular_complex.ui',
        'dialog_6_1_naming_convention.ui',
    ]

    cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui')
    destination_dir = os.path.dirname(os.path.realpath(__file__))

    cmds_list = list()
    for ui_file_name in list_ui_file_names:
        cmd = [
            'pyside2-uic',
            '--output', f'{os.path.join(destination_dir, ui_file_name.replace(".ui", ".py"))}',
            f'{os.path.join(cwd, ui_file_name)}'
        ]
        cmds_list.append(cmd)
    procs_list = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in cmds_list]
    for proc in procs_list:
        proc.wait()


if __name__ == '__main__':
    ui2py()
