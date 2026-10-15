import tkinter as tk

THEMES = {
    "dark": {
        "bg": "#1e1e1e", "top_bar": "#252526", "fg": "white", 
        "btn_bg": "#333333", "btn_fg": "white", "active_bg": "#3e3e42",
        "entry_bg": "#2d2d2d", "entry_fg": "white"
    },
    "light": {
        "bg": "#f3f3f3", "top_bar": "#e1e1e1", "fg": "black", 
        "btn_bg": "#e5e5e5", "btn_fg": "black", "active_bg": "#cccccc",
        "entry_bg": "#ffffff", "entry_fg": "black"
    }
}
current_theme = "dark"

root = tk.Tk()
root.geometry("400x550")
root.title("AI Calculator Pro")
root.minsize(300, 450)

top_bar = tk.Frame(root, height=40)
top_bar.pack(fill="x")

title_label = tk.Label(top_bar, text="AI Calculator Pro", font=("Arial", 11, "bold"))
title_label.pack(side="left", padx=10, pady=5)

def toggle_maximize():
    if root.state() == "zoomed":
        root.state("normal")
    else:
        root.state("zoomed")

close_btn = tk.Button(top_bar, text="✕", bd=0, padx=10, command=root.destroy)
close_btn.pack(side="right", fill="y")

maximize_btn = tk.Button(top_bar, text="🗖", bd=0, padx=10, command=toggle_maximize)
maximize_btn.pack(side="right", fill="y")

def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = THEMES[theme_name]
    
    root.configure(bg=theme["bg"])
    top_bar.configure(bg=theme["top_bar"])
    title_label.configure(bg=theme["top_bar"], fg=theme["fg"])
    maximize_btn.configure(bg=theme["top_bar"], fg=theme["fg"], activebackground=theme["active_bg"])
    close_btn.configure(bg=theme["top_bar"], fg=theme["fg"])
    theme_btn.configure(bg=theme["top_bar"], fg=theme["fg"])
    display.configure(bg=theme["entry_bg"], fg=theme["entry_fg"])
    
    for btn in calc_buttons:
        btn.configure(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["active_bg"])

def toggle_theme():
    new_theme = "light" if current_theme == "dark" else "dark"
    apply_theme(new_theme)

theme_btn = tk.Button(top_bar, text="🌓", bd=0, padx=10, command=toggle_theme)
theme_btn.pack(side="right", fill="y")

display_frame = tk.Frame(root, pady=15, padx=15)
display_frame.pack(fill="x")

display = tk.Entry(display_frame, font=("Arial", 22), borderwidth=0, relief="flat", justify="right")
display.pack(fill="x", ipady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(expand=True, fill="both", padx=15, pady=10)

def button_click(value):
    if value == "C":
        display.delete(0, tk.END)
    elif value == "=":
        try:
            res = eval(display.get())
            display.delete(0, tk.END)
            display.insert(0, str(res))
        except:
            display.delete(0, tk.END)
            display.insert(0, "Error")
    else:
        display.insert(tk.END, value)

buttons = [
    ('C', 0, 0), ('(', 0, 1), (')', 0, 2), ('/', 0, 3),
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2)
]

calc_buttons = []

for (text, row, col) in buttons:
    btn = tk.Button(

        buttons_frame, text=text, font=("Arial", 14, "bold"), bd=0,
        command=lambda t=text: button_click(t)
    )
    if text == '=':
        btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=3, pady=3)
    else:
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
    calc_buttons.append(btn)

for i in range(4):
    buttons_frame.columnconfigure(i, weight=1)
for i in range(5):
    buttons_frame.rowconfigure(i, weight=1)

apply_theme(current_theme)
root.mainloop()
try:
    root.iconbitmap("icon.ico")
except:
    pass
