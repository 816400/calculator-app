import tkinter as tk
from tkinter import messagebox
import re
import threading
import urllib.request

class AICalculatorPro:
    def __init__(self, root):
        self.root = root
        self.version = "1.2.0"  # الإصدار الحالي
        self.root.title(f"AI Calculator Pro v{self.version}")
        self.root.geometry("360x520")
        
        # --- تفعيل التكبير والتصغير بالكامل ---
        self.root.resizable(True, True)
        self.root.minsize(300, 450)
        # -------------------------------------
        
        self.root.configure(bg="#1e1e2e")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        
        display_frame = tk.Frame(self.root, bg="#1e1e2e", bd=10)
        display_frame.pack(expand=True, fill="both")

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Consolas", 28, "bold"),
            anchor="e",
            bg="#181825",
            fg="#cdd6f4",
            padx=15,
            pady=15
        )
        self.display_label.pack(expand=True, fill="both")

        buttons_frame = tk.Frame(self.root, bg="#1e1e2e")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ('C', 0, 0, "#f38ba8"), ('(', 0, 1, "#89b4fa"), (')', 0, 2, "#89b4fa"), ('/', 0, 3, "#fab387"),
            ('7', 1, 0, "#313244"), ('8', 1, 1, "#313244"), ('9', 1, 2, "#313244"), ('*', 1, 3, "#fab387"),
            ('4', 2, 0, "#313244"), ('5', 2, 1, "#313244"), ('6', 2, 2, "#313244"), ('-', 2, 3, "#fab387"),
            ('1', 3, 0, "#313244"), ('2', 3, 1, "#313244"), ('3', 3, 2, "#313244"), ('+', 3, 3, "#fab387"),
            ('0', 4, 0, "#313244"), ('.', 4, 1, "#313244"), ('DEL', 4, 2, "#f38ba8"), ('=', 4, 3, "#a6e3a1")
        ]

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)

        for text, row, col, color in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg="#11111b" if color in ["#f38ba8", "#89b4fa", "#fab387", "#a6e3a1"] else "#cdd6f4",
                activebackground="#45475a",
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        # ربط لوحة المفاتيح
        self.root.bind("<Key>", self.on_key_press)

        # فحص التحديثات في الخلفية بصمت تام ودون إزعاج
        self.check_for_updates_silently()

    def check_for_updates_silently(self):
        """فحص التحديثات في الخلفية دون تعطيل أو إزعاج التطبيق"""
        def background_task():
            try:
                url = "https://raw.githubusercontent.com/816400/calculator-app/main/version.txt"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as response:
                    latest_version = response.read().decode('utf-8').strip()
                    # إذا كان الإصدار على الإنترنت أحدث، يظهر تنبيه لطيف فقط
                    if latest_version > self.version:
                        self.root.after(0, lambda: messagebox.showinfo(
                            "تحديث متوفر", 
                            f"يتوفر إصدار جديد ({latest_version})!\nيمكنك تحديث نسختك من مستودع GitHub."
                        ))
            except Exception:
                pass  # يتجاهل أي خطأ في الاتصال أو عدم توفر الملف بصمت تام

        # تشغيل في خيط منفصل لكي لا يؤدي لبطء فتح الحاسبة
        threading.Thread(target=background_task, daemon=True).start()

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
                result = eval(self.expression)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.display_var.set(str(result))
                self.expression = str(result)
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