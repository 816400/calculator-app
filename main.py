import json
import tkinter as tk
from tkinter import messagebox
import urllib.request
import webbrowser

# --- إعدادات التحديث التلقائي ---
CURRENT_VERSION = "1.0.0"
# (مهم): استبدل USERNAME باسم حسابك على جيت هب و calculator-app باسم مستودعك
GITHUB_REPO_API = (
    "https://api.github.com/repos/USERNAME/calculator-app/releases/latest"
)


def check_for_updates():
  try:
    req = urllib.request.Request(
        GITHUB_REPO_API, headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=4) as response:
      data = json.loads(response.read().decode())
      latest_version = data.get("tag_name", "").lstrip("v")
      release_url = data.get("html_url", "")

      if latest_version and latest_version != CURRENT_VERSION:
        answer = messagebox.askyesno(
            "تحديث جديد متوفر!",
            f"يتوفر إصدار جديد ({latest_version}). هل تريد الانتقال لصفحة التحميل؟",
        )
        if answer:
          webbrowser.open(release_url)
      else:
        messagebox.showinfo("التحديثات", "أنت تستخدم أحدث إصدار بالفعل!")
  except Exception:
    # في حال عدم وجود إنترنت أو خطأ في الاتصال، يتم تخطي الأمر بصمت لكي لا يتعطل البرنامج
    pass


class CalculatorApp:

  def __init__(self, root):
    self.root = root
    self.root.title("AI Calculator Pro")
    self.root.geometry("360x500")
    self.root.config(bg="#1e1e1e")
    self.root.resizable(False, False)

    # --- إضافة شريط القوائم (لتضمين زر التحديثات) ---
    menubar = tk.Menu(self.root)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="فحص التحديثات", command=check_for_updates)
    menubar.add_cascade(label="المساعدة", menu=help_menu)
    self.root.config(menu=menubar)

    self.expression = ""
    self.display_var = tk.StringVar()

    display_frame = tk.Frame(self.root, bg="#1e1e1e")
    display_frame.pack(expand=True, fill="both", padx=10, pady=10)

    self.display_entry = tk.Entry(
        display_frame,
        textvariable=self.display_var,
        font=("Arial", 28, "bold"),
        bg="#2d2d2d",
        fg="#ffffff",
        bd=0,
        justify="right",
    )
    self.display_entry.pack(expand=True, fill="both", ipady=15)

    btns_frame = tk.Frame(self.root, bg="#1e1e1e")
    btns_frame.pack(expand=True, fill="both", padx=10, pady=10)

    button_layout = [
        ("C", 0, 0, 1, "#d9534f"),
        ("(", 0, 1, 1, "#444444"),
        (")", 0, 2, 1, "#444444"),
        ("/", 0, 3, 1, "#f0ad4e"),
        ("7", 1, 0, 1, "#333333"),
        ("8", 1, 1, 1, "#333333"),
        ("9", 1, 2, 1, "#333333"),
        ("*", 1, 3, 1, "#f0ad4e"),
        ("4", 2, 0, 1, "#333333"),
        ("5", 2, 1, 1, "#333333"),
        ("6", 2, 2, 1, "#333333"),
        ("-", 2, 3, 1, "#f0ad4e"),
        ("1", 3, 0, 1, "#333333"),
        ("2", 3, 1, 1, "#333333"),
        ("3", 3, 2, 1, "#333333"),
        ("+", 3, 3, 1, "#f0ad4e"),
        ("0", 4, 0, 1, "#333333"),
        (".", 4, 1, 1, "#333333"),
        ("=", 4, 2, 2, "#5cb85c"),
    ]

    for btn in button_layout:
      text, row, col, colspan, bg_color = btn
      b = tk.Button(
          btns_frame,
          text=text,
          font=("Arial", 16, "bold"),
          bg=bg_color,
          fg="#ffffff",
          bd=0,
          cursor="hand2",
          command=lambda t=text: self.on_click(t),
      )
      b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    for i in range(5):
      btns_frame.rowconfigure(i, weight=1)
    for i in range(4):
      btns_frame.columnconfigure(i, weight=1)

  def on_click(self, char):
    if char == "C":
      self.expression = ""
      self.display_var.set("")
    elif char == "=":
      try:
        result = str(eval(self.expression))
        self.display_var.set(result)
        self.expression = result
      except Exception:
        messagebox.showerror("خطأ", "عملية حسابية غير صالحة")
        self.expression = ""
        self.display_var.set("")
    else:
      self.expression += str(char)
      self.display_var.set(self.expression)


if __name__ == "__main__":
  root = tk.Tk()
  app = CalculatorApp(root)
  root.mainloop()