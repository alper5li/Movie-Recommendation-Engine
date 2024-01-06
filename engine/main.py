import tkinter as ttk
from interface import Start,Recommendation,NetworkError
from API.Network import checkNetwork
url_API = "https://www.omdbapi.com"
icon_path = r"engine\Images\logo.ico"

def checkStatus():
    _,status = checkNetwork(url_API)
    return status

def checkNetw(root):
    if(checkStatus()):
        root = Start(window)
    else:
        netwErr = NetworkError(window,url_API)


# Main Window
window = ttk.Tk()

# Setting window icon
window.iconbitmap(icon_path)

# Setting window size
window.geometry("1600x700")


# Check Network
checkNetw(window)


# End Window
window.mainloop()

