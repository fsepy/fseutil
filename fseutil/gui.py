import os
import base64
import typing
from typing import Callable
import tempfile
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from fseutil import __version__ as _ver

from fseutil.lib.fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187
from fseutil.etc.b4_br187 import OFR_LOGO_LARGE_PNG_BASE64, OFR_LOGO_SMALL_PNG_BASE64
from fseutil.etc.b4_br187 import PARALLEL_LARGE_FIGURE_PNG_BASE64, PERPENDICULAR_LARGE_FIGURE_PNG_BASE64


class Messenger(tk.Tk):
    def __init__(self, msg, title=None):
        tk.Tk.__init__(self)

        title = "" if title is None else title
        self.wm_title(title)
        label = ttk.Label(self, text=msg, font=("Helvetica", 10))
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(self, text="OK", command=self.destroy)
        B1.pack()
        self.mainloop()


class Calculator(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.notebook = ttk.Notebook()

        # General App Setting
        # ===================
        self.app_name = "B4 BR187 Calculator"  # app name
        self.app_version = _ver  # app version

        self.init_ui()

        self.notebook.grid(row=0)

        self.mainloop()

    def init_ui(self):

        # SETTINGS
        # ========

        # set window icon
        _, fp_icon = tempfile.mkstemp()
        with open(fp_icon, "wb") as f:
            f.write(base64.b64decode(OFR_LOGO_SMALL_PNG_BASE64))
        self.notebook.master.iconbitmap(fp_icon)
        # self.master.iconbitmap(fp_icon)

        self.notebook.master.title(self.app_name)

        # STYLES
        # ======

        style = ttk.Style()
        style.configure(
            "TLabel",
            foreground="black",
            background=self.notebook.master.cget("bg"),
            font=("Helvetica", 9),
        )
        style.configure(
            "TCheckbutton",
            foreground="black",
            background=self.notebook.master.cget("bg"),
            font=("Helvetica", 9),
        )
        self.columnconfigure(0, pad=10)
        self.rowconfigure(0, pad=10)

        self.tab_parallel = CalculatorParallelPanels(
            parent=self.notebook,
            app_name="B4 BR187 Calculator",
            app_version=_ver,
            app_description='Thermal radiation calculator\nemitter and receiver pair\nin parallel.',
            app_figure_main_base64=PARALLEL_LARGE_FIGURE_PNG_BASE64,
            app_phi_func=phi_parallel_any_br187
        )
        self.tab_perpendicular = CalculatorPerpendicularPanels(self.notebook)

        self.notebook.add(self.tab_parallel, text='Parallel Panels', compound=tk.TOP)
        self.notebook.add(self.tab_perpendicular, text='Perpendicular Panels', compound=tk.TOP)

        self.bind(sequence="<Return>", func=self.key_bind_enter)

    def key_bind_enter(self, _=None):
        if 'parallel' in str(self.notebook.tab(self.notebook.select(), "text")).lower():
            self.tab_parallel.calculate_resultant_heat_flux()
        elif 'perpendicular' in str(self.notebook.tab(self.notebook.select(), "text")).lower():
            self.tab_perpendicular.calculate_resultant_heat_flux()


def main():
    Calculator()


if __name__ == "__main__":
    main()
