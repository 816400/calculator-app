import os
import sys
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox

# ==================== إعدادات التحديث التلقائي ====================
CURRENT_VERSION = "1.0.0-beta"
# الرابط المباشر الصحيح لملف beta_version.json على مستودعك
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
        # تجاهل الأخطاء بصمت لكي لا يتأثر تشغيل التطبيق حال انقطاع الإنترنت
        pass

def download_and_apply_update(download_url):
    """تحميل الملف الجديد واستبداله عبر ملف باتش (Batch)"""
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            # مسار التنزيل المؤقت
            temp_exe = os.path.join(os.environ["TEMP"], "new_calculator.exe")
            with open(temp_exe, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # مسار البرنامج الحالي
            current_exe = sys.executable
            
            # كتابة سكريبت التحديث الخارجي لتجاوز قيود قفل الملفات في ويندوز
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
            
            # تشغيل السكريبت وإغلاق التطبيق الحالي
            subprocess.Popen(bat_path, shell=True)
            sys.exit()
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل عملية التحديث: {str(e)}")

# ==================== واجهة الآلة الحاسبة ====================
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Calculator Pro (Beta)")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        self.expression = ""
        
        # حقل الإدخال
        input_frame = tk.Frame(self.root, width=300, height=50)
        input_frame.pack(side=tk.TOP)
        
        self.input_text = tk.StringVar()
        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('arial', 18, 'bold'), bd=10, insertwidth=4, width=14, bg="#eee", justify='right')
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=10)
        
        # أزرار الآلة الحاسبة
        btns_frame = tk.Frame(self.root, width=300, height=350, bg="grey")
        btns_frame.pack()
        
        # تصميم الأزرار
        buttons = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2)
        ]
        
        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(btns_frame, text=text, fg="white", bg="orange", width=11, height=3, bd=0, command=self.btn_equal)
                btn.grid(row=row, column=col, columnspan=2, padx=1, pady=1)
            elif text == 'C':
                btn = tk.Button(btns_frame, text=text, fg="white", bg="red", width=5, height=3, bd=0, command=self.btn_clear)
                btn.grid(row=row, column=col, padx=1, pady=1)
            else:
                btn = tk.Button(btns_frame, text=text, fg="black", bg="white", width=5, height=3, bd=0, command=lambda x=text: self.btn_click(x))
                btn.grid(row=row, column=col, padx=1, pady=1)

        # فحص التحديثات في الخلفية بعد تشغيل البرنامج بثانيتين
        self.root.after(2000, check_for_updates)

    def btn_click(self, item):
        self.expression += str(item)
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception:
            self.input_text.set("خطأ")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()