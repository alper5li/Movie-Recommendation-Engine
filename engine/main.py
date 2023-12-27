from Ai import example
import tkinter as ttk
from interface import Start


# Main Window
window = ttk.Tk()

# Settings for Window

window.geometry("1600x700")

'''
widgets are added here
'''

start = Start(window)

example()
# End Window
window.mainloop()