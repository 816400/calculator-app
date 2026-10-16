import tkinter as tk
from tkinter import messagebox
import math, os, base64

class AICalculatorPro:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x600")
        self.root.title("AI Calculator Pro")
        self.root.configure(bg="#1e1e1e")

        self.is_pro = False
        if os.path.exists("license.dat"):
            try:
                with open("license.dat", "r") as lf:
                    if base64.b64decode(lf.read().strip()).decode() == "AI-PRO-2026-816400":
                        self.is_pro = True
            except:
                pass

        self.display = tk.Entry(root, font=("Arial", 24), bg="#2d2d2d", fg="white", justify="right", borderwidth=0)
        self.display.pack(fill="x", padx=15, pady=15, ipady=10)

        frm = tk.Frame(root, bg="#1e1e1e")
        frm.pack(expand=True, fill="both", padx=15, pady=5)

        btns = [
            ("C",0,0,"#ff3b30"), ("(",0,1,"#333333"), (")",0,2,"#333333"), ("÷",0,3,"#ff9500"),
            ("7",1,0,"#333333"), ("8",1,1,"#333333"), ("9",1,2,"#333333"), ("×",1,3,"#ff9500"),
            ("4",2,0,"#333333"), ("5",2,1,"#333333"), ("6",2,2,"#333333"), ("-",2,3,"#ff9500"),
            ("1",3,0,"#333333"), ("2",3,1,"#333333"), ("3",3,2,"#333333"), ("+",3,3,"#ff9500"),
            ("0",4,0,"#333333"), (".",4,1,"#333333"), ("⌫",4,2,"#ff3b30"), ("=",4,3,"#34c759"),
            ("PRO (Scientific)",5,0,"#5856d6")
        ]

        for t,r,c,b in btns:
            if t == "PRO (Scientific)":
                tk.Button(frm, text=t, font=("Arial", 12, "bold"), bg=b, fg="white", bd=0, command=self.pro_action).grid(row=r, column=c, columnspan=4, sticky="nsew", padx=4, pady=4)
            else:
                tk.Button(frm, text=t, font=("Arial", 16, "bold"), bg=b, fg="white", bd=0, command=lambda x=t: self.click(x)).grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        for i in range(4): frm.columnconfigure(i, weight=1)
        for i in range(6): frm.rowconfigure(i, weight=1)

        up_frm = tk.Frame(root, bg="#252526", height=40)
        up_frm.pack(fill="x", side="bottom")

        self.lbl = tk.Label(up_frm, text="PRO Activated ✔" if self.is_pro else "Free Version", bg="#252526", fg="#34c759" if self.is_pro else "#ff9500", font=("Arial", 10, "bold"))
        self.lbl.pack(side="left", padx=10, pady=8)

        if not self.is_pro:
            tk.Button(up_frm, text="Activate Pro 🔑", bg="#ff9500", fg="white", bd=0, padx=10, command=self.act_win).pack(side="right", padx=10, pady=5)

    def click(self, val):
        if val == "C":
            self.display.delete(0, tk.END)
        elif val == "⌫":
            self.display.delete(len(self.display.get())-1, tk.END)
        elif val == "=":
            try:
                res = eval(self.display.get().replace("×", "*").replace("÷", "/"))
                self.display.delete(0, tk.END)
                self.display.insert(0, str(res))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        else:
            self.display.insert(tk.END, val)

    def pro_action(self):
        if not self.is_pro:
            messagebox.showwarning("Locked 🔒", "هذه الميزة مدفوعة! الرجاء إدخال مفتاح التفعيل.")
            self.act_win()
        else:
            try:
                res = math.sqrt(float(self.display.get()))
                self.display.delete(0, tk.END)
                self.display.insert(0, f"PRO √ = {res}")
            except:
                messagebox.showinfo("Pro Mode", "النسخة الاحترافية مفعلة بنجاح!")

    def act_win(self):
        w = tk.Toplevel(self.root)
        w.geometry("320x180")
        w.title("Activate")
        w.configure(bg="#1e1e1e")
        w.grab_set()

        tk.Label(w, text="Enter License Key:", bg="#1e1e1e", fg="white", font=("Arial", 11, "bold")).pack(pady=15)
        e = tk.Entry(w, font=("Arial", 14), justify="center", width=20)
        e.pack(pady=5)

        def verify():
            if e.get().strip() == "AI-PRO-2026-816400":
                self.is_pro = True
                with open("license.dat", "w") as f:
                    f.write(base64.b64encode(b"AI-PRO-2026-816400").decode())
                self.lbl.config(text="PRO Activated ✔", fg="#34c759")
                messagebox.showinfo("Success", "تم التفعيل بنجاح!")
                w.destroy()
            else:
                messagebox.showerror("Error", "المفتاح غير صحيح.")

        tk.Button(w, text="Activate Now", bg="#34c759", fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=verify).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = AICalculatorPro(root)
    root.mainloop()