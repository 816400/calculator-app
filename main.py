import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import webbrowser

# إعداد النافذة الرئيسية (Landscape Edition)
root = tk.Tk()
root.title("AI Calculator Pro - Landscape Edition")
root.geometry("500x320")
root.resizable(False, False)
root.configure(bg="#222222")

# متغير لتخزين النص المدخل
expression = ""
input_text = tk.StringVar()

# --- دالة فحص التحديثات والأمان التلقائي ---
def check_updates_and_security():
    try:
        url = "https://raw.githubusercontent.com/816400/calculator-app/main/beta_version.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            
            # 1. فحص التنبيهات الأمنية أولاً
            if data.get("security_alert", False):
                sec_msg = data.get("security_message", "تحذير أمني هام: يرجى تحديث التطبيق فوراً!")
                messagebox.showerror("تنبيه أمني حرَج 🛡️", sec_msg)
            
            # 2. فحص الإصدارات الجديدة
            remote_version = data.get("version", "1.0.0-beta")
            current_version = "1.0.0-beta"
            
            if remote_version != current_version:
                download_url = data.get("download_url", "")
                if messagebox.askyesno("تحديث جديد متوفر 🚀", f"يتوفر إصدار جديد ({remote_version}). هل تريد التحميل الآن؟"):
                    if download_url:
                        webbrowser.open(download_url)
    except Exception as e:
        # عدم إزعاج المستخدم إذا لم تتوفر إنترنت
        print(f"فشل الاتصال بخادم التحديثات: {e}")

# شاشة العرض (Display)
text_field = tk.Entry(
    root, 
    font=('Arial', 24, 'bold'), 
    textvariable=input_text, 
    width=26, 
    bg="#333333", 
    fg="#ffffff", 
    bd=0, 
    justify="right"
)
text_field.pack(padx=20, pady=20, ipady=10)

# دوال الحاسبة
def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

def btn_clear():
    global expression
    expression = ""
    input_text.set("")

def btn_backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)

def btn_equal():
    global expression
    try:
        # استبدال علامة الضرب المرئية بعملية بايثون
        calc_expression = expression.replace('×', '*')
        result = str(eval(calc_expression))
        input_text.set(result)
        expression = result
    except Exception:
        messagebox.showerror("خطأ", "عملية غير صالحة")
        expression = ""
        input_text.set("")

# إطار الأزرار (تصميم أفقي/Landscape)
btns_frame = tk.Frame(root, bg="#222222")
btns_frame.pack()

# تخطيط الأزرار
buttons = [
    ('C', 1, 0, '#d9534f', btn_clear),
    ('⌫', 1, 1, '#f0ad4e', btn_backspace),
    ('/', 1, 2, '#5bc0de', lambda: btn_click('/')),
    ('×', 1, 3, '#5bc0de', lambda: btn_click('×')),
    
    ('7', 2, 0, '#444444', lambda: btn_click('7')),
    ('8', 2, 1, '#444444', lambda: btn_click('8')),
    ('9', 2, 2, '#444444', lambda: btn_click('9')),
    ('-', 2, 3, '#5bc0de', lambda: btn_click('-')),
    
    ('4', 3, 0, '#444444', lambda: btn_click('4')),
    ('5', 3, 1, '#444444', lambda: btn_click('5')),
    ('6', 3, 2, '#444444', lambda: btn_click('6')),
    ('+', 3, 3, '#5bc0de', lambda: btn_click('+')),
    
    ('1', 4, 0, '#444444', lambda: btn_click('1')),
    ('2', 4, 1, '#444444', lambda: btn_click('2')),
    ('3', 4, 2, '#444444', lambda: btn_click('3')),
    ('=', 4, 3, '#5cb85c', btn_equal),
    
    ('0', 5, 0, '#444444', lambda: btn_click('0')),
    ('.', 5, 1, '#444444', lambda: btn_click('.'))
]

for (text, row, col, bg_color, command) in buttons:
    if text == '0':
        btn = tk.Button(btns_frame, text=text, fg="#ffffff", bg=bg_color, width=17, height=2, bd=0, font=('Arial', 14, 'bold'), command=command)
        btn.grid(row=row, column=col, columnspan=2, padx=3, pady=3)
    else:
        span = 2 if text == '=' else 1
        btn = tk.Button(btns_frame, text=text, fg="#ffffff", bg=bg_color, width=8, height=2, bd=0, font=('Arial', 14, 'bold'), command=command)
        btn.grid(row=row, column=col, columnspan=span, padx=3, pady=3)

# تشغيل فحص التحديثات والأمان في الخلفية عند فتح التطبيق
root.after(1000, check_updates_and_security)

root.mainloop()