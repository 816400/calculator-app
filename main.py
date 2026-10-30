import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import webbrowser
import math

# إعداد النافذة الرئيسية (Modern Landscape Edition with Toggle)
root = tk.Tk()
root.title("AI Calculator Pro - Modern Landscape Edition")
root.geometry("620x380")
root.minsize(500, 320)
root.configure(bg="#1e1e2e")

# متغيرات النظام
expression = ""
input_text = tk.StringVar()
is_maximized = False

# --- دالة فحص التحديثات والأمان التلقائي ---
def check_updates_and_security():
    try:
        url = "https://raw.githubusercontent.com/816400/calculator-app/main/beta_version.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            
            # 1. التنبيهات الأمنية الحرجة
            if data.get("security_alert", False):
                sec_msg = data.get("security_message", "تحذير أمني هام: يرجى تحديث التطبيق فوراً!")
                messagebox.showerror("تنبيه أمني حرَج 🛡️", sec_msg)
            
            # 2. فحص التحديثات
            remote_version = data.get("version", "1.0.0-beta")
            current_version = "1.0.0-beta"
            
            if remote_version != current_version:
                download_url = data.get("download_url", "")
                if messagebox.askyesno("تحديث جديد متوفر 🚀", f"يتوفر إصدار جديد ({remote_version}). هل تريد التحميل الآن؟"):
                    if download_url:
                        webbrowser.open(download_url)
    except Exception as e:
        print(f"فشل الاتصال بخادم التحديثات: {e}")

# --- إطار الشاشة العلوية ---
display_frame = tk.Frame(root, bg="#1e1e2e")
display_frame.pack(fill="x", padx=15, pady=(15, 10))

text_field = tk.Entry(
    display_frame, 
    font=('Segoe UI', 26, 'bold'), 
    textvariable=input_text, 
    bg="#181825", 
    fg="#cdd6f4", 
    bd=0, 
    relief="flat",
    justify="right",
    insertbackground="#cdd6f4"
)
text_field.pack(fill="x", ipady=12, padx=5)

# --- دوال الحاسبة والعمليات المتقدمة ---
def btn_click(item):
    global expression
    expression += str(item)
    input_text.set(expression)

def btn_clear():
    global expression
    expression = ""
    input_text.set("")

def btn_backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)

def btn_sqrt():
    global expression
    try:
        if expression:
            val = float(eval(expression.replace('×', '*').replace('÷', '/').replace('^', '**')))
            if val < 0:
                messagebox.showerror("خطأ", "لا يمكن حساب الجذر لعدد سالب")
                return
            res = math.sqrt(val)
            expression = str(int(res) if res.is_integer() else res)
            input_text.set(expression)
    except Exception:
        messagebox.showerror("خطأ", "عملية غير صالحة")
        expression = ""
        input_text.set("")

def btn_percent():
    global expression
    try:
        if expression:
            val = float(eval(expression.replace('×', '*').replace('÷', '/').replace('^', '**')))
            res = val / 100
            expression = str(res)
            input_text.set(expression)
    except Exception:
        messagebox.showerror("خطأ", "عملية غير صالحة")
        expression = ""
        input_text.set("")

def btn_equal():
    global expression
    try:
        calc_exp = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
        result = eval(calc_exp)
        res_str = str(int(result) if isinstance(result, float) and result.is_integer() else result)
        input_text.set(res_str)
        expression = res_str
    except Exception:
        messagebox.showerror("خطأ", "عملية غير صالحة")
        expression = ""
        input_text.set("")

# --- دالة تكبير وتصغير النافذة (Toggle Size) ---
def toggle_size():
    global is_maximized
    if not is_maximized:
        root.geometry("820x520")
        btn_resize.config(text="🔍 تصغير النافذة")
        is_maximized = True
    else:
        root.geometry("620x380")
        btn_resize.config(text="🔍 تكبير النافذة")
        is_maximized = False

# --- زر التحكم بالتكبير والتصغير ---
top_control_frame = tk.Frame(root, bg="#1e1e2e")
top_control_frame.pack(fill="x", padx=15, pady=(0, 5))

btn_resize = tk.Button(
    top_control_frame, 
    text="🔍 تكبير النافذة", 
    font=('Segoe UI', 10, 'bold'), 
    fg="#a6adc8", 
    bg="#313244", 
    activebackground="#45475a",
    activeforeground="#ffffff",
    bd=0, 
    cursor="hand2",
    command=toggle_size
)
btn_resize.pack(side="left", padx=5, ipady=3)

# --- إطار الأزرار (شبكة تفاعلية) ---
btns_frame = tk.Frame(root, bg="#1e1e2e")
btns_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

for i in range(5):
    btns_frame.rowconfigure(i, weight=1)
for j in range(5):
    btns_frame.columnconfigure(j, weight=1)

# جدول الأزرار المحدث بالكامل
buttons = [
    ('C', 0, 0, '#f38ba8', '#11111b', btn_clear),
    ('⌫', 0, 1, '#fab387', '#11111b', btn_backspace),
    ('√', 0, 2, '#89b4fa', '#11111b', btn_sqrt),
    ('%', 0, 3, '#89b4fa', '#11111b', btn_percent),
    ('÷', 0, 4, '#89b4fa', '#11111b', lambda: btn_click('÷')),
    
    ('7', 1, 0, '#313244', '#cdd6f4', lambda: btn_click('7')),
    ('8', 1, 1, '#313244', '#cdd6f4', lambda: btn_click('8')),
    ('9', 1, 2, '#313244', '#cdd6f4', lambda: btn_click('9')),
    ('^', 1, 3, '#89b4fa', '#11111b', lambda: btn_click('^')),
    ('×', 1, 4, '#89b4fa', '#11111b', lambda: btn_click('×')),
    
    ('4', 2, 0, '#313244', '#cdd6f4', lambda: btn_click('4')),
    ('5', 2, 1, '#313244', '#cdd6f4', lambda: btn_click('5')),
    ('6', 2, 2, '#313244', '#cdd6f4', lambda: btn_click('6')),
    ('-', 2, 3, '#89b4fa', '#11111b', lambda: btn_click('-')),
    ('+', 2, 4, '#89b4fa', '#11111b', lambda: btn_click('+')),
    
    ('1', 3, 0, '#313244', '#cdd6f4', lambda: btn_click('1')),
    ('2', 3, 1, '#313244', '#cdd6f4', lambda: btn_click('2')),
    ('3', 3, 2, '#313244', '#cdd6f4', lambda: btn_click('3')),
    ('=', 3, 3, '#a6e3a1', '#11111b', btn_equal),
    
    ('0', 4, 0, '#313244', '#cdd6f4', lambda: btn_click('0')),
    ('.', 4, 2, '#313244', '#cdd6f4', lambda: btn_click('.'))
]

for item in buttons:
    text, row, col, bg_color, fg_color, command = item
    if text == '=':
        btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 16, 'bold'), bd=0, cursor="hand2", command=command)
        btn.grid(row=row, column=col, rowspan=2, columnspan=2, sticky="nsew", padx=3, pady=3)
    elif text == '0':
        btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 14, 'bold'), bd=0, cursor="hand2", command=command)
        btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=3, pady=3)
    elif text == '.':
        btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 14, 'bold'), bd=0, cursor="hand2", command=command)
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
    else:
        btn = tk.Button(btns_frame, text=text, fg=fg_color, bg=bg_color, font=('Segoe UI', 14, 'bold'), bd=0, cursor="hand2", command=command)
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

root.after(1000, check_updates_and_security)
root.mainloop()