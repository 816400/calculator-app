import tkinter as tk
from tkinter import messagebox
import re
import urllib.request

class AICalculatorPro:
    def __init__(self, root):
        self.root = root
        self.version = "1.5.0"
        self.root.title(f"AI Calculator Pro v{self.version}")
        self.root.geometry("540x550")
        self.root.resizable(True, True)
        self.root.minsize(400, 480)
        self.root.configure(bg="#1e1e2e")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        main_layout = tk.Frame(self.root, bg="#1e1e2e")
        main_layout.pack(expand=True, fill="both", padx=10, pady=10)

        main_layout.grid_columnconfigure(0, weight=3)
        main_layout.grid_columnconfigure(1, weight=2)
        main_layout.grid_rowconfigure(0, weight=1)

        # إطار الحاسبة (اليسار)
        calc_frame = tk.Frame(main_layout, bg="#1e1e2e")
        calc_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        calc_frame.grid_rowconfigure(1, weight=1)
        calc_frame.grid_columnconfigure(0, weight=1)

        display_frame = tk.Frame(calc_frame, bg="#1e1e2e", bd=5)
        display_frame.grid(row=0, column=0, sticky="nsew")

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Consolas", 24, "bold"),
            anchor="e",
            bg="#181825",
            fg="#cdd6f4",
            padx=15,
            pady=15
        )
        self.display_label.pack(expand=True, fill="both")

        buttons_frame = tk.Frame(calc_frame, bg="#1e1e2e")
        buttons_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 0))

        buttons = [
            ('C', 0, 0, "#f38ba8"), ('(', 0, 1, "#89b4fa"), (')', 0, 2, "#89b4fa"), ('/', 0, 3, "#fab387"),
            ('7', 1, 0, "#313244"), ('8', 1, 1, "#313244"), ('9', 1, 2, "#313244"), ('*', 1, 3, "#fab387"),
            ('4', 2, 0, "#313244"), ('5', 2, 1, "#313244"), ('6', 2, 2, "#313244"), ('-', 2, 3, "#fab387"),
            ('1', 3, 0, "#313244"), ('2', 3, 1, "#313244"), ('3', 3, 2, "#313244"), ('+', 3, 3, "#fab387"),
            ('0', 4, 0, "#313244"), ('.', 4, 1, "#313244"), ('DEL', 4, 2, "#f38ba8"), ('=', 4, 3, "#a6e3a1")
        ]

        for i in range(5): buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4): buttons_frame.grid_columnconfigure(j, weight=1)

        for text, row, col, color in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Arial", 13, "bold"),
                bg=color,
                fg="#11111b" if color in ["#f38ba8", "#89b4fa", "#fab387", "#a6e3a1"] else "#cdd6f4",
                activebackground="#45475a",
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

        # إطار السجل والأزرار (اليمين)
        history_frame = tk.Frame(main_layout, bg="#181825", bd=2)
        history_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        history_frame.grid_rowconfigure(1, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)

        history_title = tk.Label(
            history_frame,
            text="سجل العمليات",
            font=("Arial", 12, "bold"),
            bg="#181825",
            fg="#89b4fa",
            pady=8
        )
        history_title.grid(row=0, column=0, sticky="ew")

        self.history_listbox = tk.Listbox(
            history_frame,
            bg="#11111b",
            fg="#cdd6f4",
            font=("Consolas", 11),
            selectbackground="#313244",
            selectforeground="#a6e3a1",
            relief="flat",
            bd=0
        )
        self.history_listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        action_frame = tk.Frame(history_frame, bg="#181825")
        action_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)

        clear_history_btn = tk.Button(
            action_frame,
            text="مسح السجل",
            font=("Arial", 9, "bold"),
            bg="#313244",
            fg="#f38ba8",
            activebackground="#45475a",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            command=self.clear_history
        )
        clear_history_btn.grid(row=0, column=0, sticky="ew", padx=(0, 2), pady=2)

        update_btn = tk.Button(
            action_frame,
            text="فحص التحديثات",
            font=("Arial", 9, "bold"),
            bg="#313244",
            fg="#89b4fa",
            activebackground="#45475a",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            command=self.check_for_updates_manual
        )
        update_btn.grid(row=0, column=1, sticky="ew", padx=(2, 0), pady=2)

        self.root.bind("<Key>", self.on_key_press)

    def clear_history(self):
        self.history_listbox.delete(0, tk.END)

    def parse_version(self, v_str):
        try:
            return [int(x) for x in re.findall(r'\d+', v_str)]
        except Exception:
            return [0, 0, 0]

    def check_for_updates_manual(self):
        try:
            url = "https://raw.githubusercontent.com/816400/calculator-app/main/version.txt"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                remote_version_str = response.read().decode('utf-8').strip()
                current_v = self.parse_version(self.version)
                remote_v = self.parse_version(remote_version_str)
                
                if remote_v > current_v:
                    messagebox.showinfo("تحديث متوفر", f"يتوفر إصدار جديد ({remote_version_str})!\nإصدارك الحالي هو ({self.version}).")
                else:
                    messagebox.showinfo("تحديث", "أنت تستخدم أحدث إصدار بالفعل!")
        except Exception:
            messagebox.showerror("خطأ", "تعذر الاتصال بالخادم. تأكد من اتصالك بالإنترنت.")

    def on_key_press(self, event):
        char = event.char
        if char in "0123456789+-*/().":
            self.on_button_click(char)
        elif event.keysym in ("Return", "KP_Enter"):
            self.on_button_click("=")
        elif event.keysym == "BackSpace":
            self.on_button_click("DEL")
        elif event.keysym in ("Escape", "c", "C"):
            self.on_button_click("C")

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        elif char == "=":
            try:
                calc_str = self.expression
                result = eval(self.expression)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                result_str = str(result)
                self.display_var.set(result_str)
                if calc_str:
                    self.history_listbox.insert(tk.END, f"{calc_str} = {result_str}")
                    self.history_listbox.see(tk.END)
                self.expression = result_str
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
        else:
            if char == ".":
                parts = re.split(r'[\+\-\*\/\(\)]', self.expression)
                current_number = parts[-1] if parts else ""
                if "." in current_number:
                    return
            if self.display_var.get() == "0" and char not in ".+-*/":
                self.expression = char
            else:
                self.expression += str(char)
            self.display_var.set(self.expression)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AICalculatorPro(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"An unexpected error occurred:\n{e}")