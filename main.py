(
echo import os
echo import sys
echo import requests
echo import subprocess
echo import tkinter as tk
echo from tkinter import messagebox
echo.
echo CURRENT_VERSION = "1.0.1-beta"
echo VERSION_URL = "https://raw.githubusercontent.com/816400/calculator-app/main/beta_version.json"
echo.
echo def check_for_updates():
echo     try:
echo         response = requests.get(VERSION_URL, timeout=5)
echo         if response.status_code == 200:
echo             data = response.json()
echo             remote_version = data.get^("version"^)
echo             download_url = data.get^("download_url"^)
echo             if remote_version and remote_version != CURRENT_VERSION:
echo                 if messagebox.askyesno^("تحديث متوفر", f"توفر إصدار جديد ({remote_version}). هل تريد التحديث الآن؟"^):
echo                     download_and_apply_update(download_url^)
echo     except Exception as e:
echo         pass
echo.
echo def download_and_apply_update(download_url^):
echo     try:
echo         response = requests.get(download_url, stream=True^)
echo         if response.status_code == 200:
echo             temp_exe = os.path.join(os.environ["TEMP"], "new_calculator.exe"^)
echo             with open(temp_exe, "wb"^) as f:
echo                 for chunk in response.iter_content(chunk_size=8192^):
echo                     f.write(chunk^)
echo             current_exe = sys.executable
echo             bat_path = os.path.join(os.environ["TEMP"], "update.bat"^)
echo             with open(bat_path, "w", encoding="utf-8"^) as bat_file:
echo                 bat_file.write^("""
echo @echo off
echo timeout /t 2 /nobreak > nul
echo del /f /q "{current_exe}"
echo move /y "{temp_exe}" "{current_exe}"
echo start "" "{current_exe}"
echo del "%~f0"
echo """^)
echo             subprocess.Popen(bat_path, shell=True^)
echo             sys.exit(^0^)
echo     except Exception as e:
echo         messagebox.showerror^("خطأ", f"فشل عملية التحديث: {str(e)}"^)
echo.
echo class CalculatorApp:
echo     def __init__(self, root^):
echo         self.root = root
echo         self.root.title("AI Calculator Pro (v1.0.1-beta)"^)
echo         self.root.geometry("320x450"^)
echo         self.root.minsize(280, 380^)
echo         self.expression = ""
echo         self.root.rowconfigure(1, weight=1^)
echo         self.root.columnconfigure(0, weight=1^)
echo         self.input_text = tk.StringVar(^)
echo         display_frame = tk.Frame(self.root, bg="#222222"^)
echo         display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10^)
echo         display_frame.rowconfigure(0, weight=1^)
echo         display_frame.columnconfigure(0, weight=1^)
echo         input_field = tk.Entry(display_frame, textvariable=self.input_text, font=('Segoe UI', 22, 'bold'^+ ' bold'^), bd=0, bg="#222222", fg="#00ffcc", justify='right', insertbackground="white"^)
echo         input_field.grid(row=0, column=0, sticky="nsew", ipady=15, padx=10^)
echo         btns_frame = tk.Frame(self.root, bg="#1e1e1e"^)
echo         btns_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10^))
echo         for i in range(6^):
echo             btns_frame.rowconfigure(i, weight=1^)
echo         for j in range(4^):
echo             btns_frame.columnconfigure(j, weight=1^)
echo         buttons = [
echo             ('C', 1, 0, "#ff4d4d", "white"), ('(', 1, 1, "#444444", "white"), (')', 1, 2, "#444444", "white"), ('/', 1, 3, "#ff9500", "white"),
echo             ('7', 2, 0, "#2d2d2d", "white"), ('8', 2, 1, "#2d2d2d", "white"), ('9', 2, 2, "#2d2d2d", "white"), ('*', 2, 3, "#ff9500", "white"),
echo             ('4', 3, 0, "#2d2d2d", "white"), ('5', 3, 1, "#2d2d2d", "white"), ('6', 3, 2, "#2d2d2d", "white"), ('-', 3, 3, "#ff9500", "white"),
echo             ('1', 4, 0, "#2d2d2d", "white"), ('2', 4, 1, "#2d2d2d", "white"), ('3', 4, 2, "#2d2d2d", "white"), ('+', 4, 3, "#ff9500", "white"),
echo             ('0', 5, 0, "#2d2d2d", "white"), ('.', 5, 1, "#2d2d2d", "white"), ('=', 5, 2, 2, "#00b894", "white")
echo         ]
echo         for btn_info in buttons:
echo             text = btn_info[0]
echo             row = btn_info[1]
echo             col = btn_info[2]
echo             bg_color = btn_info[3]
echo             fg_color = btn_info[4]
echo             colspan = btn_info[5] if len(btn_info^) ^> 5 else 1
echo             if text == '=':
echo                 btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'^), bd=0, command=self.btn_equal^)
echo             elif text == 'C':
echo                 btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'^), bd=0, command=self.btn_clear^)
echo             else:
echo                 btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'^), bd=0, command=lambda x=text: self.btn_click(x^))
echo             btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2^)
echo         self.root.after(2000, check_for_updates^)
echo.
echo     def btn_click(self, item^):
echo         self.expression += str(item^)
echo         self.input_text.set(self.expression^)
echo.
echo     def btn_clear(self, *args^):
echo         self.expression = ""
echo         self.input_text.set(""^)
echo.
echo     def btn_equal(self, *args^):
echo         try:
echo             result = str(eval(self.expression^.replace^('×', '*'^).replace^('÷', '/'^)^)^)
echo             self.input_text.set(result^)
echo             self.expression = result
echo         except Exception:
echo             self.input_text.set("خطأ"^)
echo             self.expression = ""
echo.
echo if __name__ == "__main__":
echo     root = tk.Tk(^)
echo     app = CalculatorApp(root^)
echo     root.mainloop(^)
) > main.py