import tkinter as tk
from tkinter import ttk
root = tk.Tk()
def change_theme(theme_name):
    style.theme_use(theme_name)
available_themes = ttk.Style().theme_names()
style = ttk.Style()

# Create checkboxes with each theme
for theme in available_themes:
    ttk.Checkbutton(root, text=f"Theme: {theme}", command=lambda t=theme: change_theme(t)).pack()
root.mainloop()