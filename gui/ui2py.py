

def ui2py():
    import os
    import subprocess

    list_ui_file_names = [
        'main.ui',
        'dialog_1_1_adb_datasheet_1.ui',
        'dialog_4_1_br187_parallel_simple.ui',
        'dialog_4_3_br187_parallel_complex.ui'
    ]

    cwd = os.path.dirname(os.path.realpath(__file__))
    destination_dir = os.path.join(os.path.dirname(cwd), 'fseutil', 'ui')

    for ui_file_name in list_ui_file_names:
        cmd = f'pyside2-uic {os.path.join(cwd, ui_file_name)} > {os.path.join(destination_dir, ui_file_name.replace(".ui", ".py"))}'
        print(cmd)
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    ui2py()
