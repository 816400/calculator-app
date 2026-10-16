import tkinter as tk
root = tk.Tk()
root.geometry("400x550")
root.title("AI Calculator Pro")
root.configure(bg="#1e1e1e")
display = tk.Entry(root, font=("Arial", 24), bg="#2d2d2d", fg="white", justify="right", borderwidth=0)
display.pack(fill="x", padx=15, pady=20, ipady=10)
def btn_click(val):
    if val == "C": display.delete(0, tk.END)
    elif val == "⌫": display.delete(len(display.get())-1, tk.END)
    elif val == "=":
        try:
            res = eval(display.get().replace("×", "*").replace(\> "÷", "/"))
            display.delete(0, tk.END); display.insert(0, str(res))
        except: display.delete(0, tk.END); display.insert(0, "Error")
    else: display.insert(tk.END, val)
buttons_frame = tk.Frame(root, bg="#1e1e1e"); buttons_frame.pack(expand=True, fill="both", padx=15, pady=10)
buttons = [("C", 0, 0, "#ff3b30"), ("(", 0, 1, "#333333"), (")", 0, 2, "#333333"), ("÷", 0, 3, "#ff9500"), ("7", 1, 0, "#333333"), ("8", 1, 1, "#333333"), ("9", 1, 2, "#333333"), ("×", 1, 3, "#ff9500"), ("4", 2, 0, "#333333"), ("5", 2, 1, "#333333"), ("6", 2, 2, "#333333"), ("-", 2, 3, "#ff9500"), ("1", 3, 0, "#333333"), ("2", 3, 1, "#333333"), ("3", 3, 2, "#333333"), ("+", 3, 3, "#ff9500"), ("0", 4, 0, "#333333"), (".", 4, 1, "#333333"), ("⌫", 4, 2, "#ff3b30"), ("=", 4, 3, "#34c759")]
for text, row, col, bg_color in buttons:
    btn = tk.Button(buttons_frame, text=text, font=("Arial", 16, "bold"), bg=bg_color, fg="white", bd=0, command=lambda t=text: btn_click(t))
    btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
for i in range(4): buttons_frame.columnconfigure(i, weight=1)
for i in range(5): buttons_frame.rowconfigure(i, weight=1)
root.mainloop()