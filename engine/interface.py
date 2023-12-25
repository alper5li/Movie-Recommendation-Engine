import tkinter as ttk

class Age():
    def __init__(self,root):
        self.root = root
        self.root.title("Please Enter Your Age")
        self.ask = ttk.Label(text="Please Enter Your Age")
        self.ask.pack(pady=5)


class ATR():
    def __init__(self, root):
        self.root = root
        self.root.title("İlk Ekran")

        self.label = ttk.Label(self.root, text="Bu ilk sınıfın ekranı")
        self.label.pack(pady=10)

        self.button = ttk.Button(self.root, text="Geçiş", command=self.switch_to_Age_class)
        self.button.pack(pady=5)

    def switch_to_Age_class(self):
        self.label.pack_forget()
        self.button.pack_forget()
        Age(self.root)
        