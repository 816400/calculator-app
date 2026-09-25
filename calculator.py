import tkinter as tk
from tkinter import messagebox
import math

# --------------------
# النافذة الرئيسية
# --------------------
root = tk.Tk()
root.title("AI Calculator")
root.geometry("500x750")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

# --------------------
# شاشة العرض
# --------------------
display = tk.Entry(
    root,
    font=("Arial", 24),
    bg="#252526",
    fg="white",
    justify="right",
    bd=0
)

display.pack(fill="x", padx=10, pady=10, ipady=15)

# --------------------
# سجل العمليات
# --------------------
history_box = tk.Text(
    root,
    height=8,
    bg="#252526",
    fg="white",
    font=("Consolas", 10)
)

history_box.pack(fill="x", padx=10, pady=5)

# --------------------
# الدوال
# --------------------
def add_history(text):
    history_box.insert(tk.END, text + "\n")
    history_box.see(tk.END)


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
        expression = display.get()

        expression = expression.replace("^", "**")

        result = eval(expression)

        add_history(f"{expression} = {result}")

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")


def square_root():

    try:
        value = float(display.get())

        result = math.sqrt(value)

        display.delete(0, tk.END)
        display.insert(0, str(result))

        add_history(f"√{value} = {result}")

    except:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")


def percentage():

    try:
        value = float(display.get())

        result = value / 100

        display.delete(0, tk.END)
        display.insert(0, str(result))

        add_history(f"{value}% = {result}")

    except:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")


# --------------------
# مساعد ذكي محلي
# --------------------
def ai_assistant():

    text = display.get().lower().strip()

    if text == "":
        messagebox.showinfo(
            "AI Assistant",
            "أدخل سؤالاً أو عملية حسابية."
        )
        return

    try:

        if "جذر" in text:
            number = float(text.replace("جذر", ""))
            result = math.sqrt(number)

            messagebox.showinfo(
                "AI Assistant",
                f"الجذر التربيعي = {result}"
            )

        elif "نسبة" in text:
            messagebox.showinfo(
                "AI Assistant",
                "لحساب النسبة استخدم:\nالعدد × النسبة ÷ 100"
            )

        elif "+" in text:
            result = eval(text)

            messagebox.showinfo(
                "AI Assistant",
                f"هذه عملية جمع.\nالنتيجة = {result}"
            )

        elif "-" in text:
            result = eval(text)

            messagebox.showinfo(
                "AI Assistant",
                f"هذه عملية طرح.\nالنتيجة = {result}"
            )

        elif "*" in text:
            result = eval(text)

            messagebox.showinfo(
                "AI Assistant",
                f"هذه عملية ضرب.\nالنتيجة = {result}"
            )

        elif "/" in text:
            result = eval(text)

            messagebox.showinfo(
                "AI Assistant",
                f"هذه عملية قسمة.\nالنتيجة = {result}"
            )

        else:
            messagebox.showinfo(
                "AI Assistant",
                "لم أفهم الطلب."
            )

    except:
        messagebox.showinfo(
            "AI Assistant",
            "تعذر تحليل العملية."
        )


# --------------------
# الأزرار
# --------------------
buttons_frame = tk.Frame(root, bg="#1e1e1e")
buttons_frame.pack(expand=True, fill="both")

buttons = [
    ["C", "⌫", "√", "%", "/"],
    ["7", "8", "9", "^", "*"],
    ["4", "5", "6", "(", "-"],
    ["1", "2", "3", ")", "+"],
    ["AI", "0", ".", "="]
]

for r, row in enumerate(buttons):

    for c, btn in enumerate(row):

        color = "#3c3c3c"

        if btn == "=":
            command = calculate
            color = "#0e639c"

        elif btn == "C":
            command = clear
            color = "#c42b1c"

        elif btn == "⌫":
            command = backspace
            color = "#666666"

        elif btn == "AI":
            command = ai_assistant
            color = "#8e44ad"

        elif btn == "√":
            command = square_root
            color = "#444444"

        elif btn == "%":
            command = percentage
            color = "#444444"

        else:
            command = lambda x=btn: press(x)

        tk.Button(
            buttons_frame,
            text=btn,
            font=("Arial", 18, "bold"),
            bg=color,
            fg="white",
            bd=0,
            command=command
        ).grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=3,
            pady=3
        )

for i in range(5):
    buttons_frame.rowconfigure(i, weight=1)

for j in range(5):
    buttons_frame.columnconfigure(j, weight=1)

root.mainloop()
