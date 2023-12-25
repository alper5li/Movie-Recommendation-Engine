from Ai import example
import tkinter as ttk
from interface import ATR


# Main Window
window = ttk.Tk()

# Settings for Window

window.geometry("1366x768")
'''
widgets are added here
'''

atr = ATR(window)
example()
# End Window
window.mainloop()