import base64
import tempfile
import tkinter as tk

from fseutil.etc.icon import ofr_colour_618_618_base64
from fseutil.lib.b4_br187 import phi_parallel_any_br187


class Calculator(tk.Frame):

    def __init__(self):
        super().__init__()

        self.l1 = tk.Label(self, text='Emitter Width [m]')
        self.e1 = tk.Entry(self)
        self.l2 = tk.Label(self, text='Emitter Height [m]')
        self.e2 = tk.Entry(self)
        self.l3 = tk.Label(self, text='Receiver Loc. X [m]')
        self.e3 = tk.Entry(self)
        self.l4 = tk.Label(self, text='Receiver Loc. Y [m]')
        self.e4 = tk.Entry(self)
        self.l5 = tk.Label(self, text='Separation [m]')
        self.e5 = tk.Entry(self)
        self.l6 = tk.Label(self, text='Emitter Heat Flux [kW/m2]')
        self.e6 = tk.Entry(self)
        self.l7 = tk.Label(self, text='Received Heat Flux [kW/m2]')
        self.e7 = tk.Entry(self)

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
        self.columnconfigure(1, pad=10)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)

        self.l1.grid(row=1, column=0, sticky=tk.W)
        self.e1.grid(row=1, column=1, sticky=tk.W+tk.E)
        self.l2.grid(row=2, column=0, sticky=tk.W)
        self.e2.grid(row=2, column=1, sticky=tk.W+tk.E)
        self.l3.grid(row=3, column=0, sticky=tk.W)
        self.e3.grid(row=3, column=1, sticky=tk.W+tk.E)
        self.l4.grid(row=4, column=0, sticky=tk.W)
        self.e4.grid(row=4, column=1, sticky=tk.W+tk.E)
        self.l5.grid(row=5, column=0, sticky=tk.W)
        self.e5.grid(row=5, column=1, sticky=tk.W+tk.E)
        self.l6.grid(row=6, column=0, sticky=tk.W)
        self.e6.grid(row=6, column=1, sticky=tk.W+tk.E)
        self.l7.grid(row=7, column=0, sticky=tk.W)
        self.e7.grid(row=7, column=1, sticky=tk.W+tk.E)

        self.e7.config(stat=tk.DISABLED)
        self.e7.delete(0, tk.END)
        self.e7.insert(tk.END, 156)

        b1 = tk.Button(self, text="Calculate", command=self.command_calculate_phi)
        b1.grid(row=7, column=2)

    def command_calculate_phi(self):
        try:
            out = phi_parallel_any_br187(
                W_m=float(self.e1.get()),
                H_m=float(self.e2.get()),
                w_m=float(self.e3.get()),
                h_m=float(self.e4.get()),
                S_m=float(self.e5.get())
            )
            out *= float(self.e6.get())
        except Exception as e:
            if hasattr(e, 'message'):
                out = e.message
            else:
                out = e

        self.e7.config(stat=tk.NORMAL)
        self.e7.delete(0, tk.END)
        self.e7.insert(tk.END, out)
        self.e7.config(stat='readonly')


def main():
    root = tk.Tk()
    my_gui = Calculator()
    root.mainloop()


if __name__ == '__main__':
    main()
