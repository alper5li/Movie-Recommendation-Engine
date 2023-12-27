from Ai import example
import tkinter as ttk
from interface import Start


# Main Window
window = ttk.Tk()

# Settings for Window

window.geometry("1600x700")

start = Start(window)

# End Window
window.mainloop()