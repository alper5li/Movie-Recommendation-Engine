import threading
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
from dataAPI import GetAllMovies


def schedule_check(t):
    """
    Schedule the execution of the `check_if_done()` function after
    one second.
    """
    root.after(1000, check_if_done, t)


def check_if_done(t):
    # If the thread has finished, re-enable the button and show a message.
    if not t.is_alive():
        info_label["text"] = "File successfully downloaded!"
        download_button["state"] = "normal"
    else:
        # Otherwise check again after one second.
        schedule_check(t)


def download_file():
    info_label["text"] = "Downloading file..."
    # Disable the button while downloading the file.
    download_button["state"] = "disabled"
    # Start the download in a new thread.
    t = threading.Thread(target=lambda:GetAllMovies(True))
    t.start()
    # Start checking periodically if the thread has finished.
    schedule_check(t)


root = tk.Tk()
root.title("Download file with Tcl/Tk")
info_label = ttk.Label(text="Click the button to download the file.")
info_label.pack()
download_button = ttk.Button(text="Download file", command=download_file)
download_button.pack()
root.mainloop()