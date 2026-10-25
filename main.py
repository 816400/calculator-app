import os
import sys
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox

# ==================== إعدادات التحديث التلقائي ====================
CURRENT_VERSION = "1.0.1-beta"
VERSION_URL = "https://raw.githubusercontent.com/816400/calculator-app/main/beta_version.json"

def check_for_updates():
    """التحقق من وجود تحديث جديد تلقائياً"""
    try:
        response = requests.get(VERSION_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            remote_version = data.get("version")
            download_url = data.get("download_url")
            
            if remote_version and remote_version != CURRENT_VERSION:
                if messagebox.askyesno("تحديث متوفر", f"توفر إصدار جديد ({remote_version}). هل تريد التحديث الآن؟"):
                    download_and_apply_update(download_url)
    except Exception as e:
        pass

def download_and_apply_update(download_url):
    """تحميل الملف الجديد واستبداله عبر ملف باتش (Batch)"""
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            temp_exe = os.path.join(os.environ["TEMP"], "new_calculator.exe")
            with open(temp_exe, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            current_exe = sys.executable
            bat_path = os.path.join(os.environ["TEMP"], "update.bat")
            with open(bat_path, "w", encoding="utf-8") as bat_file:
                bat_file.write(f"""
@echo off
timeout /t 2 /nobreak > nul
del /f /q "{current_exe}"
move /y "{temp_exe}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
""")
            subprocess.Popen(bat_path, shell=True)
            sys.exit(0)
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل عملية التحديث: {str(e)}")

# ==================== واجهة الآلة الحاسبة الملونة والمرنة ====================
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Calculator Pro (v1.0.1-beta)")
        self.root.geometry("320x450")
        self.root.minsize(280, 380) # أقل حجم ممكن للنافذة
        
        self.expression = ""
        
        # ضبط أوزان النافذة لكي تتمدد الأزرار بمرونة عند تكبير النافذة
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # شاشة العرض (حقل الإدخال)
        self.input_text = tk.StringVar()
        
        display_frame = tk.Frame(self.root, bg="#222222")
        display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        display_frame.rowconfigure(0, weight=1)
        display_frame.columnconfigure(0, weight=1)

        input_field = tk.Entry(
            display_frame, 
            textvariable=self.input_text, 
            font=('Segoe UI', 22, 'bold'), 
            bd=0, 
            bg="#222222", 
            fg="#00ffcc", 
            justify='right',
            insertbackground="white"
        )
        input_field.grid(row=0, column=0, sticky="nsew", ipady=15, padx=10)

        # إطار الأزرار
        btns_frame = tk.Frame(self.root, bg="#1e1e1e")
        btns_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # جعل صفوف وأعمدة الأزرار تتوزع بالتساوي وتتوسع مع النافذة
        for i in range(6):
            btns_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btns_frame.columnconfigure(j, weight=1)

        # تصميم الأزرار مع الألوان والأيقونات
        buttons = [
            ('C', 1, 0, "#ff4d4d", "white"), ('(', 1, 1, "#444444", "white"), (')', 1, 2, "#444444", "white"), ('/', 1, 3, "#ff9500", "white"),
            ('7', 2, 0, "#2d2d2d", "white"), ('8', 2, 1, "#2d2d2d", "white"), ('9', 2, 2, "#2d2d2d", "white"), ('*', 2, 3, "#ff9500", "white"),
            ('4', 3, 0, "#2d2d2d", "white"), ('5', 3, 1, "#2d2d2d", "white"), ('6', 3, 2, "#2d2d2d", "white"), ('-', 3, 3, "#ff9500", "white"),
            ('1', 4, 0, "#2d2d2d", "white"), ('2', 4, 1, "#2d2d2d", "white"), ('3', 4, 2, "#2d2d2d", "white"), ('+', 4, 3, "#ff9500", "white"),
            ('0', 5, 0, "#2d2d2d", "white"), ('.', 5, 1, "#2d2d2d", "white"), ('=', 5, 2, 2, "#00b894", "white")
        ]
        
        for btn_info in buttons:
            text = btn_info[0]
            row = btn_info[1]
            col = btn_info[2]
            bg_color = btn_info[3]
            fg_color = btn_info[4]
            
            colspan = btn_info[5] if len(btn_info) > 5 else 1
            
            if text == '=':
                btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'), bd=0, command=self.btn_equal)
            elif text == 'C':
                btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'), bd=0, command=self.btn_clear)
            else:
                btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'), bd=0, command=lambda x=text: self.btn_click(x))
            
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

        # فحص التحديثات في الخلفية بعد تشغيل البرنامج بثانيتين
        self.root.after(2000, check_for_updates)

    def btn_click(self, item):
        self.expression += str(item)
        self.input_text.set(self.expression)

    def btn_clear(self, *args):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self, *args):
        try:
            result = str(eval(self.expression.replace('×', '*').replace('÷', '/')))
            self.input_text.set(result)
            self.expression = result
        except Exception:
            self.input_text.set("خطأ")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()