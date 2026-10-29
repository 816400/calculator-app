import sys
import os
import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import webbrowser

# معلومات الإصدار الحقيقي والتحديث
CURRENT_VERSION = "v1.0.0"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/816400/calculator-app/main/beta_version.json"

class AICalculatorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Calculator Pro")
        self.root.geometry("360" "520")
        self.root.config(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        # إنشاء واجهة الحاسبة
        self.create_widgets()
        
        # التحقق من وجود تحديثات تلقائية عند فتح التطبيق
        self.check_for_updates()

    def create_widgets(self):
        # شاشة العرض (Display)
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(pady=20)

        input_field = tk.Entry(
            input_frame, 
            font=('Arial', 24, 'bold'), 
            textvariable=self.input_text, 
            width=16, 
            bg="#2d2d2d", 
            fg="#ffffff", 
            bd=0, 
            justify=tk.RIGHT
        )
        input_field.grid(row=0, column=0, ipady=15)

        # إطار الأزرار
        btns_frame = tk.Frame(self.root, bg="#1e1e1e")
        btns_frame.pack()

        # تصميم الأزرار (النص، الصف، العمود)
        buttons = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('AI', 5, 3)
        ]

        for (text, row, col) in buttons:
            if text == '=':
                bg_color = "#007acc"
                fg_color = "#ffffff"
                command = self.calculate
            elif text == 'C':
                bg_color = "#d9534f"
                fg_color = "#ffffff"
                command = self.clear
            elif text == 'AI':
                bg_color = "#8a2be2"
                fg_color = "#ffffff"
                command = self.ai_assist
            else:
                bg_color = "#333333"
                fg_color = "#ffffff"
                command = lambda t=text: self.btn_click(t)

            btn = tk.Button(
                btns_frame, 
                text=text, 
                font=('Arial', 14, 'bold'), 
                fg=fg_color, 
                bg=bg_color, 
                bd=0, 
                width=5, 
                height=2, 
                command=command
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

    def btn_click(self, item):
        self.expression += str(item)
        self.input_text.set(self.expression)

    def clear(self):
        self.expression = ""
        self.input_text.set("")

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception:
            messagebox.showerror("خطأ", "عملية غير صالحة")
            self.expression = ""
            self.input_text.set("")

    def ai_assist(self):
        messagebox.showinfo("مساعد الذكاء الاصطناعي", "مرحباً بك! نظام الذكاء الاصطناعي جاهز لمساعدتك في العمليات المعقدة والتحليلات البرمجية.")

    def check_for_updates(self):
        try:
            req = urllib.request.Request(
                GITHUB_VERSION_URL, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("version")
                
                if latest_version and latest_version != CURRENT_VERSION:
                    if messagebox.askyesno("تحديث جديد متوفر", f"توفر إصدار جديد ({latest_version}). هل تريد الانتقال لصفحة التحميل؟"):
                        webbrowser.open("https://github.com/816400/calculator-app/releases")
        except Exception:
            # تجاهل أخطاء الاتصال بالإنترنت بصمت لكي لا يتوقف التطبيق
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AICalculatorPro(root)
    root.mainloop()