import tkinter as tk
from tkinter import messagebox
import math

# ---------------------------------
# إنشاء النافذة
# ---------------------------------
root = tk.Tk()
root.title("AI Calculator Pro")
root.geometry("500x750")
root.configure(bg="#1e1e1e")
root.resizable(True, True)

# ---------------------------------
# شريط علوي
# ---------------------------------
top_bar = tk.Frame(root, bg="#252526", height=40)
top_bar.pack(fill="x")

title_label = tk.Label(
    top_bar,
    text="AI Calculator Pro",
    bg="#252526",
    fg="white",
    font=("Arial", 12, "bold")
)
title_label.pack(side="left", padx=10)

def toggle_maximize():
    if root.state() == "zoomed":
        root.state("normal")
    else:
        root.state("zoomed")

tk.Button(
    top_bar,
    text="−",
    command=root.iconify,
    bg="#555555",
    fg="white",
    bd=0,
    width=4
).pack(side="right", padx=2)

tk.Button(
    top_bar,
    text="□",
    command=toggle_maximize,
    bg="#555555",
    fg="white",
    bd=0,
    width=4
).pack(side="right", padx=2)

tk.Button(
    top_bar,
    text="✕",
    command=root.destroy,
    bg="#c42b1c",
    fg="white",
    bd=0,
    width=4
).pack(side="right", padx=2)

# ---------------------------------
# شاشة العرض
# ---------------------------------
display = tk.Entry(
    root,
    font=("Arial", 24),
    bg="#252526",
    fg="white",
    justify="right",
    bd=0
)
display.pack(fill="x", padx=10, pady=10, ipady=15)

# ---------------------------------
# سجل العمليات
# ---------------------------------
history_box = tk.Text(
    root,
    height=6,
    bg="#252526",
    fg="white",
    font=("Consolas", 10)
)
history_box.pack(fill="x", padx=10, pady=5)

def add_history(text):
    history_box.insert(tk.END, text + "\n")
    history_box.see(tk.END)

# ---------------------------------
# الدوال
# ---------------------------------
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
        display.insert(0, result)

        add_history(f"√{value} = {result}")
    except:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")

def percentage():
    try:
        value = float(display.get())
        result = value / 100

        display.delete(0, tk.END)
        display.insert(0, result)

        add_history(f"{value}% = {result}")

    except:
        display.delete(0, tk.END)
        display.insert(0, "خطأ")

def ai_assistant():
    text = display.get()

    if not text:
        messagebox.showinfo(
            "AI Assistant",
            "أدخل عملية أو سؤالاً."
        )
        return

    try:
        result = eval(text.replace("^", "**"))

        messagebox.showinfo(
            "AI Assistant