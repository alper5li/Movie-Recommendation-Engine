from Ai import example
import tkinter as ttk
from interface import Start,Recommendation,NetworkError
from API.Network import checkNetwork
url_API = "https://www.omdbapi.com"
icon_path = r"C:\Users\alper\PCSC\Movie-Recommendation-Engine\engine\Images\logo.ico"
def checkStatus():
    _,status = checkNetwork(url_API)
    return status


# Main Window
window = ttk.Tk()

window.iconbitmap(icon_path)


# Settings for Window
window.geometry("1600x700")

if(checkStatus()):
    root = Start(window)
else:
    netwErr = NetworkError(window,url_API)
# End Window
window.mainloop()

