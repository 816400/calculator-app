import os
import sys
import subprocess
import threading
import requests
import tkinter as tk
from tkinter import messagebox
import math

# =============================
# نظام التحديثات المدمج
# =============================
GITHUB_REPO = "your-username/your-repo-name"
CURRENT_VERSION = "v1.0.0"

def check_for_updates_detailed():
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("tag_name")
            release_notes = data.get("body", "لا توجد ملاحظات متوفرة.")
            assets = data.get("assets", [])

            download_url = None
            for asset in assets:
                if asset["name"].endswith(".exe"):
                    download_url = asset["browser_download_url"]
                    break

            if latest_version and latest_version != CURRENT_VERSION and download_url:
                return True, latest_version, download_url, release_notes
            return False, latest_version, None, release_notes
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
    
    return False, CURRENT_VERSION, None, "تعسّر الاتصال بخادم التحديثات."

def apply_update(download_url):
    try:
        response = requests.get(download_url, stream=True)
        temp_exe = "update_temp.exe"
        with open(temp_exe, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if getattr(sys, 'frozen', False):
            current_exe = sys.executable
        else:
            current_exe = os.path.abspath("dist/main.exe")

        current_dir = os.path.dirname(current_exe)
        exe_name = os.path.basename(current_exe)

        bat_script_path = os.path.join(current_dir, "update_installer.bat")
        bat_content = f"""@echo off
timeout /t 2 /nobreak > nul
taskkill /f /im "{exe_name}" > nul 2>&1
move /y "{temp_exe}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""
        with open(bat_script_path, "w", encoding="utf-8") as f:
            f.write(bat_content)

        subprocess.Popen([bat_script_path], shell=True, cwd=current_dir)
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("خطأ في التحديث", f"فشل تثبيت التحديث:\n{e}")

def start_update_check_async(root_window=None):
    def worker():
        has_update, new_version, download_url, notes = check_for_updates_detailed()
        if has_update:
            def show_dialog():
                msg = f"يتوفر إصدار جديد ({new_version})!\n\nملاحظات الإصدار:\n{notes}\n\nهل تريد التحديث الآن؟"
                if messagebox.askyesno("تحديث جديد متوفر", msg):
                    apply_update(download_url)

            if root_window:
                root_window.after(0, show_dialog)
            else:
                show_dialog()

    threading.Thread(target=worker, daemon=True).start()


# =============================
# إنشاء النافذة
# =============================
root = tk.Tk()
root.title("AI Calculator Pro")
root.geometry("500x750")
root.configure(bg="#1e1e1e")
root.resizable(True, True)

# =============================
# شريط العنوان
# =============================
top_bar = tk.Frame(root, bg="#252526", height=40)
top_bar.pack(fill="x")


def toggle_maximize():
    if root.state() == "zoomed":
        root.state("normal")
    else:
        root.state("zoomed")


title_label = tk.Label(
    top_bar,
    text="AI Calculator Pro",
    bg="#252526",
    fg="white",
    font=("Arial", 12, "bold")
)
title_label.pack(side="left", padx=10)

btn_close = tk.Button(
    top_bar,
    text="✕",
    command=root.destroy,
    bg="#c42b1c",
    fg="white",
    bd=0,
    width=4
)
btn_close.pack(side="right", padx=2)

btn_max = tk.Button(
    top_bar,
    text="□",
    command=toggle_maximize,
    bg="#555555",
    fg="white",
    bd=0,
    width=4
)
btn_max.pack(side="right", padx=2)

btn_min = tk.Button(
    top_bar,
    text="−",
    command=root.iconify,
    bg="#555555",
    fg="white",
    bd=0,
    width=4
)
btn_min.pack(side="right", padx=2)

# =============================
# شاشة العرض
# =============================
display = tk.Entry(
    root,
    font=("Arial", 24),
    justify="right",
    bg="#252526",
    fg="white"
)
display.pack(fill="x", padx=10, pady=10, ipady=15)

# =============================
# سجل العمليات
# =============================
history = tk.Text(
    root,
    height=6,
    bg="#252526",
    fg="white",
    font=("Consolas", 10)
)
history.pack(fill="x", padx=10, pady=5)


def add_history(text):
    history.insert(tk.END, text + "\n")
    history.see(tk.END)

# =============================
# الدوال
# =============================
def press(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)


def backspace():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


def calculate():
    try:
        expression = display.get().replace("^", "**")
        result = eval(expression)

        add_history(f"{expression} = {result}")

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")


def square_root():
    try:
        value = float(display.get())
        result = math.sqrt(value)

        display.delete(0, tk.END)
        display.insert(0, str(result))

        add_history(f"√{value} = {result}")

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")


def percentage():
    try:
        value = float(display.get())
        result = value / 100

        display.delete(0, tk.END)
        display.insert(0, str(result))

        add_history(f"{value}% = {result}")

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")


def ai_assistant():
    text = display.get()

    if not text:
        messagebox.showinfo(
            "AI Assistant",
            "أدخل عملية حسابية أولاً"
        )
        return

    try:
        result = eval(text.replace("^", "**"))

        messagebox.showinfo(
            "AI Assistant",
            f"النتيجة:\n{text} = {result}"
        )

        add_history(f"AI: {text} = {result}")

    except Exception:
        messagebox.showerror(
            "AI Assistant",
            "تعذر فهم العملية"
        )

# =============================
# الأزرار
# =============================
buttons_frame = tk.Frame(root, bg="#1e1e1e")
buttons_frame.pack(pady=5)

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "^", "+"
]

row = 0
col = 0

for btn in buttons:
    tk.Button(
        buttons_frame,
        text=btn,
        width=8,
        height=2,
        font=("Arial", 14),
        bg="#333333",
        fg="white",
        command=lambda b=btn: press(b)
    ).grid(row=row, column=col, padx=5, pady=5)

    col += 1

    if col == 4:
        col = 0
        row += 1

# =============================
# أزرار التحكم
# =============================
tk.Button(
    root,
    text="=",
    command=calculate,
    bg="#0078D7",
    fg="white",
    font=("Arial", 14, "bold")
).pack(fill="x", padx=10, pady=3)

tk.Button(
    root,
    text="C",
    command=clear
).pack(fill="x", padx=10, pady=3)

tk.Button(
    root,
    text="⌫",
    command=backspace
).pack(fill="x", padx=10, pady=3)

tk.Button(
    root,
    text="√",
    command=square_root
).pack(fill="x", padx=10, pady=3)

tk.Button(
    root,
    text="%",
    command=percentage
).pack(fill="x", padx=10, pady=3)

tk.Button(
    root,
    text="AI Assistant",
    command=ai_assistant,
    bg="#28a745",
    fg="white",
    font=("Arial", 12, "bold")
).pack(fill="x", padx=10, pady=5)

# =============================
# تفعيل فحص التحديثات في الخلفية
# =============================
start_update_check_async(root_window=root)

# =============================
# تشغيل البرنامج
# =============================
root.mainloop()