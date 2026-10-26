import sys
import os
import tkinter as tk
from tkinter import messagebox

class AICalculatorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Calculator Pro v1.0.1")
        self.root.geometry("360x520")
        self.root.resizable(False, False)
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

        # ترتيب الأزرار بدقة: (النص، الصف، العمود، لون الخلفية)
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