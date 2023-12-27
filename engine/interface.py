import tkinter as ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from Ai import *
from API.RequestAPI import ask
from dataAPI import GetAllMovies
import time



class Start():
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation Engine")

        self.label = ttk.Label(self.root, text="Welcome to the Movie Recommendation Engine App")
        self.label.pack(pady=5)

        self.button = ttk.Button(self.root, text="Geçiş", command=self.switch_to_Age_class)
        self.button.pack(pady=5)

    def switch_to_Age_class(self):
        self.label.pack_forget()
        self.button.pack_forget()
        Age(self.root)
        
        
class Age():
    def __init__(self,root):
        self.root = root
        self.root.title("Please Enter Your Age")
        self.root.configure(bg="black")
        
        custom_font = ('Helvetica', 54)
        self.ask = ttk.Label(text="Please Enter Your Age",foreground="white",bg="black")
        self.ask.configure(font=custom_font)
        self.ask.pack(pady=200)
        
        entry_font = ('Helvetica',40)
        self.validate_entry_cmd = root.register(self.validate_entry)
        
        self.entry = ttk.Entry(validate='key',
                               validatecommand=(self.validate_entry_cmd,'%P'),
                               fg="red",
                               bg="black",
                               width=5,
                               font=entry_font,
                               justify="center")
        
        self.entry.pack(pady=5)

        self.button = ttk.Button(self.root,text="continue",command=self.getAge)
        self.button.pack(pady=5)
    
    def validate_entry(self,text):
        return (len(text) <=3 and text.isdigit())

    def getAge(self):
        age = int(self.entry.get())
        if age< 0:
            self.ask.configure(text="Age can not be smaller than 0")
            return
        # Remove current packs for next class 
        self.ask.pack_forget()
        self.entry.pack_forget()
        self.button.pack_forget()
        
        if age < 18:
            self.ask.configure(text=f"your age is {age} : child")
            Recommendation(self.root,False)        
            
        elif age >= 18:
            self.ask.configure(text=f"your age is {age} : adult")
            Recommendation(self.root,True)        


class Recommendation():
    
    def __init__(self,root,isAdult):
        self.root = root
        #timer
        start_time = time.time()
        self.AllMovies = GetAllMovies(isAdult)
        #endtimer
        end_time = time.time() 
        print(f"TIME ===== {end_time-start_time}")
        self.approve = self.Approve_Image()
        self.notapprove = self.NotApprove_Image()
        
        # Stores Only Current Shown Movies, It should update after every interaction
        self.currentMovies = []
        # Stores Only Current Shown Movies Pictures, It should update after every interaction
        self.images = self.getPictures()
        
        
        self.labels = []
        self.buttons = []
        
        
        self.label = ttk.Label(self.root, text=f"Are You adult : {isAdult}",foreground="white", background="black")        
        self.label.pack()
        
        self.button = ttk.Button(self.root)
        self.label.grid(row=0, column=0, columnspan=len(self.images), pady=5)

            # self.currentMovies instead self.images
        for index,img in enumerate(self.images):
            frame = ttk.Frame(root,bg="black")
            frame.grid(row=1, column=index, sticky="nsew")
            
            label = ttk.Label(frame, image=img,justify="center")
            label.grid(row=0, column=0, padx=5, pady=5)
            self.labels.append(label)
            
            #INTERESTED BUTTON
            buttonY = ttk.Button(frame,image=self.approve, width=100, height=100,background="black",  borderwidth=0,activebackground=root.cget("background")) # ADD  ==  command = add_knowledge(Movie)  as interested
            buttonY.grid(row=1, column=0, padx=(30,2), pady=2, sticky='w')
            self.buttons.append(buttonY)
            
            #NOT INTERESTED BUTTON
            buttonN = ttk.Button(frame, image=self.notapprove, width=100, height=100,background="black" , borderwidth=0,activebackground=root.cget("background"))
            buttonN.grid(row=1, column=0, padx=(2,30), pady=2, sticky='e')
            self.buttons.append(buttonN)
            
            # Sütunların eşit oranda genişlemesi için
            root.grid_columnconfigure(index, weight=1)  
            root.grid_rowconfigure(1, weight=1)
            
        ## ERR 
        self.labels.pack(pady=5)
        
    def movieNames(self):
        namelist = [ 
            "the Godfather",
            "finding Nemo",
            "Avatar",
            "Narnia",
            "Tron"  
        ]
        
        temp = [ 
            "the Godfather",
        ]
        
        return namelist

    def genres(self):
        genres =[
            ["Adult","Crime","Family"],
            ["Short","Sci-Fi","Romance"],
            ["Game-Show","Comedy","Crime"],
            ["History","Film-Noir","Drama"],
            ["News","Fantasy","Crime"],
            ["Musical","Music","Family"],
            ["Talk-Show","Documentary","News"],
            ["Music","Reality-Tv","Romance"],
            ["Film-Noir","History","Drama"],
            ["Crime","Sport","Thriller"],
        ]

        return genres

    def getPictures(self):
        images = []
        for movie in self.movieNames():
            url = ask(movie)
            print(f"{movie} : {url}")
            response=requests.get(url)
            img_data = response.content
            # Resmi PIL ile aç
            image = Image.open(BytesIO(img_data))

            # Resmi PhotoImage olarak dönüştür
            photo = ImageTk.PhotoImage(image)
            
            images.append(photo)
        return images
    
    def Approve_Image(self):
        img = Image.open("engine\\Images\\approve.png")
        
        img = img.resize((100,100))
        
        photo = ImageTk.PhotoImage(img)
        return photo
   
    def NotApprove_Image(self):
        img = Image.open("engine\\Images\\notapprove.png")
        
        img = img.resize((100,100))
        
        photo = ImageTk.PhotoImage(img)
        return photo
    
        