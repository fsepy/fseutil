import base64
import tempfile
import tkinter as tk
from tkinter import ttk

from fseutil.etc.icon import ofr_colour_618_618_base64
from fseutil.lib.fse_b4_br187 import phi_parallel_any_br187


class Calculator(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.frame_centre = ttk.Frame(self, width=450, height=50, pady=3)

        self.label_W = ttk.Label(self, text='W [m]')
        self.entry_W = ttk.Entry(self)
        self.label_H = ttk.Label(self, text='H [m]')
        self.entry_H = ttk.Entry(self)
        self.label_w = ttk.Label(self, text='w [m]')
        self.entry_w = ttk.Entry(self)
        self.label_h = ttk.Label(self, text='h [m]')
        self.entry_h = ttk.Entry(self)
        self.label_S = ttk.Label(self, text='S [m]')
        self.entry_S = ttk.Entry(self)
        self.label_Q = ttk.Label(self, text='Q [kW/m2]')
        self.entry_Q = ttk.Entry(self)
        self.label_result = ttk.Label(self, text='Resultant Q [kW/m2]')
        self.entry_result = ttk.Entry(self)

        self.button_calculate = ttk.Button(self, text="Calculate", command=self.command_calculate_phi)

        self.init_ui()

    def init_ui(self):
        _, fp_icon = tempfile.mkstemp()
        with open(fp_icon, "wb") as f:
            f.write(base64.b64decode(ofr_colour_618_618_base64))
        self.master.iconbitmap(fp_icon)

        self.master.title("Phi Calculator")
        self.master.geometry(newGeometry="400x150")
        self.master.resizable(0, 0)

        self.pack(fill=tk.BOTH, expand=True)

        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(1, pad=2)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)

        self.label_W.grid(row=1, column=0, sticky='w')
        self.entry_W.grid(row=1, column=1, sticky='we')
        self.label_H.grid(row=2, column=0, sticky=tk.W)
        self.entry_H.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.label_w.grid(row=3, column=0, sticky=tk.W)
        self.entry_w.grid(row=3, column=1, sticky=tk.W + tk.E)
        self.label_h.grid(row=4, column=0, sticky=tk.W)
        self.entry_h.grid(row=4, column=1, sticky=tk.W + tk.E)
        self.label_S.grid(row=5, column=0, sticky=tk.W)
        self.entry_S.grid(row=5, column=1, sticky=tk.W + tk.E)
        self.label_Q.grid(row=6, column=0, sticky=tk.W)
        self.entry_Q.grid(row=6, column=1, sticky=tk.W + tk.E)
        self.label_result.grid(row=7, column=0, sticky=tk.W)
        self.entry_result.grid(row=7, column=1, sticky=tk.W + tk.E)

        self.entry_result.config(stat='readonly')
        self.entry_result.delete(0, tk.END)
        self.entry_result.insert(tk.END, 156)

        self.button_calculate.grid(row=7, column=2)

    def command_calculate_phi(self):
        try:
            out = phi_parallel_any_br187(
                W_m=float(self.entry_W.get()),
                H_m=float(self.entry_H.get()),
                w_m=float(self.entry_w.get()),
                h_m=float(self.entry_h.get()),
                S_m=float(self.entry_S.get())
            )
            out *= float(self.entry_Q.get())
            out = f'{out:.2f}'
        except Exception as e:
            if hasattr(e, 'message'):
                out = e.message
            else:
                out = e

        self.entry_result.config(stat=tk.NORMAL)
        self.entry_result.delete(0, tk.END)
        self.entry_result.insert(tk.END, out)
        self.entry_result.config(stat='readonly')


def main():
    root = tk.Tk()
    my_gui = Calculator()
    root.mainloop()


if __name__ == '__main__':
    main()
