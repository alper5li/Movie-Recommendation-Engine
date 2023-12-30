import tkinter as ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from Ai import *
from API.RequestAPI import ask
import time
import threading
from tkinter.ttk import Progressbar as PB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# It will shown Welcome Page for the user.
class Start():
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation Engine")
        self.root.configure(bg="black")
        self.bindReference = self.root.bind('<Return>', self.switch_to_Age_class)
        self.main()

    def switch_to_Age_class(self,event=None):
        self.label.place_forget()
        self.label2.place_forget()
        self.root.unbind('<Return>', self.bindReference)
        Age(self.root)
    
    def main(self):
        custom_font1 = ('Helvetica', 34)
        custom_font2 = ('Helvetica', 24)

        self.label = ttk.Label(self.root, text="Welcome to the Movie Recommendation Engine App",background="black",fg="yellow")
        self.label.configure(font=custom_font1)
        self.label.place(anchor = "center", relx = .5, rely = .2)
        
        self.label2 = ttk.Label(self.root, text="Press ENTER to continue...",background="black",fg="green")
        self.label2.configure(font=custom_font2)
        self.label2.place(anchor = "center", relx = .5, rely = .4)
        
# Age Class gets age as a input from user to decide User is Adult or Not    
class Age():
    def __init__(self,root):
        self.root = root
        
        self.main()
    
    def validate_entry(self,text):
        return (len(text) <=3 and text.isdigit())

    def getAge(self):
        age = int(self.entry.get())
        if age< 0:
            self.ask.configure(text="Age can not be smaller than 0")
            return
        # Remove current packs for next class 
        self.ask.place_forget()
        self.entry.place_forget()
        self.button.place_forget()
        
        if age < 18:
            self.ask.configure(text=f"your age is {age} : child")
            Recommendation(self.root,False)        
            
        elif age >= 18:
            self.ask.configure(text=f"your age is {age} : adult")
            Recommendation(self.root,True)        

    def main(self):
        self.root.title("Please Enter Your Age")
        
        custom_font = ('Helvetica', 54)
        self.ask = ttk.Label(text="Please Enter Your Age",foreground="white",bg="black")
        self.ask.configure(font=custom_font)
        self.ask.place(anchor = "center", relx = .5, rely = .3)
        
        entry_font = ('Helvetica',40)
        self.validate_entry_cmd = self.root.register(self.validate_entry)
        
        self.entry = ttk.Entry(validate='key',
                               validatecommand=(self.validate_entry_cmd,'%P'),
                               fg="red",
                               bg="black",
                               width=5,
                               font=entry_font,
                               justify="center")
        
        self.entry.place(anchor = "center", relx = .5, rely = .5)

        self.button = ttk.Button(self.root,text="continue",command=self.getAge)
        self.button.place(anchor = "center", relx = .5, rely = .7)

# The Main Recommendation Program.
class Recommendation():
    
    '''
    THREADING 
    '''
    
    # Set information widgets while threading and starts threading 
    def getMovies(self):
        self.info_label["text"] = "Downloading File..."
        self.info_label.place(anchor = "center", relx = .5, rely = .2)
        self.follow_progress["text"] = f"remaining files {0}/{0}"
        self.follow_progress.place(anchor = "center", relx = .5, rely = .45)
        t = threading.Thread(target=self.getData)
        t.start()
        # Start checking periodically if the thread has finished.
        self.schedule_check(t)
        
    # Gets Data From Local Dataset
    def getData(self):
        raw = pd.read_csv("engine\\new_data.csv", delimiter=',', encoding='utf-8', low_memory=False)
        movieListAll = []
        if self.isAdult:
            rowNumber = raw.shape[0] # 195730
            rowNumber = 33
            for i in range(rowNumber):
                self.follow_progress["text"] = f"remaining files {i}/{rowNumber}"
                self.progress_var.set((i/rowNumber) * 100)
                createMovie = Movie(raw.iloc[i][0],raw.iloc[i][2],raw.iloc[i][3],raw.iloc[i][4],raw.iloc[i][5],raw.iloc[i][6],raw.iloc[i][7])
                movieListAll.append(createMovie)
        
        else:
            raw = raw[raw['isAdult'] == 0] # 195078
            rowNumber = raw.shape[0]
            for i in range(rowNumber):
                self.follow_progress["text"] = f"remaining files {i}/{rowNumber}"
                self.progress_var.set((i/rowNumber) * 100)
                createMovie = Movie(raw.iloc[i][0],raw.iloc[i][2],raw.iloc[i][3],raw.iloc[i][4],raw.iloc[i][5],raw.iloc[i][6],raw.iloc[i][7])
                movieListAll.append(createMovie)
        
        self.AllMovies = movieListAll
        self.length = len(self.AllMovies) - 1
   
    # Checking Periodically if the task is ended     
    def schedule_check(self,task):
        self.root.after(1000, self.check_if_done, task)
    
    # If task is ended, it will route to the main function. If not checks again.
    def check_if_done(self,task):
        if not task.is_alive():
            self.info_label["text"] = "File successfully downloaded!"
            self.info_label.place_forget()
            self.main()

        else:
            self.progress_var.set(50)
            self.schedule_check(task)
   
    '''
    END THREADING
    '''        
    
    # Assignin Ai and Threading Widgets.
    def __init__(self,root,isAdult=21):
        self.root = root
        self.isAdult = isAdult
        
        # Initialize Ai
        self.Ai = MovieAi()
        
        # Set custom fonts
        custom_font = ('Helvetica',40)
        custom_font2 = ('Helvetica',14)
        
        # Set Threading Information Label
        self.info_label = ttk.Label(foreground="green",bg="black")
        self.info_label.configure(font=custom_font)
        
        # Set Threading Following Progress label
        self.follow_progress = ttk.Label(foreground="green",bg="black")
        self.follow_progress.configure(font=custom_font2)
        
        # Set Threading Loading Bar
        self.progress_var = ttk.DoubleVar()
        self.progress = PB(self.root, variable=self.progress_var, length=600)
        self.progress.place(anchor="center", relx=0.5, rely=0.5)

        self.root.title("Loading Movies")
        self.movies = self.getMovies()

    # assignin random movies into self.currentMovies for startup. You can specify movie count by setting length variable
    def assignRandomMovies(self,length=5):
        movies = []
        for _ in range(length):
            movies.append(self.generateRandomMovie())
        return movies
    
    # it will return image of specified movie, assign poster into allocated memory using self.images and returns itself
    def getPoster(self,index,movie):
        try:
            print(type(movie))
            url = ask(movie.id)
            print(f"{movie} : {url}")
            response=requests.get(url)
            img_data = response.content
            # Resmi PIL ile aç
            image = Image.open(BytesIO(img_data))
            # Resmi PhotoImage olarak dönüştür
            photo = ImageTk.PhotoImage(image)
                
            self.images[index] = photo  
            return self.images[index]  
                
        except requests.exceptions.MissingSchema:
            self.Exception_getPoster(index)  
    
    # If Exception occurs during getPoster, it will try to generate another movie which has an image at API database
    def Exception_getPoster(self,index):
        newMovie = self.generateRandomMovie()
        self.showPoster(index,newMovie) 

    # Gets Local Image for using at the [Interested] button
    def Approve_Image(self):
        img = Image.open("engine\\Images\\approve.png")
        
        img = img.resize((100,100))
        
        photo = ImageTk.PhotoImage(img)
        return photo
    
    # Gets Local Image for using at the [Not interested] button
    def NotApprove_Image(self):
        img = Image.open("engine\\Images\\notapprove.png")
        
        img = img.resize((100,100))
        
        photo = ImageTk.PhotoImage(img)
        return photo
    
    # Outputs Current Ai information
    def Ai_Info(self):
        print(f"Interested = {sorted(list(self.Ai.Interested))}")
        print(f"Not Interested = {sorted(list(self.Ai.NotInterested))}")
        print(f"used Types = {sorted(list(self.Ai.usedTypes))}")
        print(f"knowledge = {sorted(list(self.Ai.knowledge))}")
        print(f"Advice Types = {sorted(list(self.Ai.adviceTypes))}")
        print(f"Advice Types = {returnType(self.Ai.adviceTypes)}")
        print(f"Combinated Advice Types = {list(self.Ai.advice_combinations)}")        
        print(f"Count of Combined Advice Types : [{len(self.Ai.advice_combinations)}]") 
        
    # Adding Movie into Ai's knowledge as interested
    def add_Interested(self,movie,index):
        self.Ai.add_knowledge(movie,1)
        # reset the posters and movies
        newMovie = self.generateRandomMovie() 
        self.currentMovies[index] = newMovie
        self.showPoster(index,newMovie)
        self.Ai_Info()

    # Adding Movie into Ai's knowledge as not interested    
    def add_NotInterested(self,movie,index):
        self.Ai.add_knowledge(movie,0)
        # reset the posters and movies
        
        newMovie = self.generateRandomMovie() 
        self.currentMovies[index] = newMovie
        self.showPoster(index,newMovie)
        self.Ai_Info()

    # Gets Random Movie from AllMovies
    def generateRandomMovie(self):
        length = self.length
        x = random.randint(0,length)
        movie = self.AllMovies[x]
        return movie
        
    # main widgets here
    def main(self):
        '''
        # Stores All Movies
        self.AllMovies = []
        self.length = len(self.AllMovies)

        '''
        
        # Setting Approve Icon
        self.approve = self.Approve_Image()
        # Setting Not Approve Icon
        self.notapprove = self.NotApprove_Image()
        # Stores Only Current Shown Movies, It should update after every interaction, 
        self.currentMovies = self.assignRandomMovies(5)
        # Stores Only Current Shown Movies Pictures, It should update after every interaction
        self.images = [
            'poster1',
            'poster2',
            'poster3',
            'poster4',
            'poster5'
        ]
        # Stores Labels which holds current Images
        self.labels = []
        # Represents User is either Adult Or Not.        
        self.label = ttk.Label(self.root, text=f"Are You adult : {self.isAdult}",foreground="white", background="black")        
        self.label.grid(row=0, column=0, columnspan=len(self.images), pady=5)
        #
        #self.button = ttk.Button(self.root)

        for index,movie in enumerate(self.currentMovies):
            self.showPoster(index,movie)
        
        ## ERR 
        self.labels.grid(pady=5)
    
    # Shows and Updates Poster 
    def showPoster(self,index,movie):
            frame = ttk.Frame(self.root,bg="black")
            frame.grid(row=1, column=index, sticky="nsew")
            
            label = ttk.Label(frame, image=self.getPoster(index,movie),justify="center",)
            label.grid(row=0, column=0, padx=5, pady=5)
            self.labels.append(label)
            
            #INTERESTED BUTTON
            buttonY = ttk.Button(frame,image=self.approve, width=100, height=100,background="black",  
                                 borderwidth=0,activebackground=self.root.cget("background"),
                                 command=lambda: [self.add_Interested(movie,index)]
                                 ) 
            
            buttonY.grid(row=1, column=0, padx=(30,2), pady=2, sticky='w')
            
            #NOT INTERESTED BUTTON
            buttonN = ttk.Button(frame, image=self.notapprove, width=100, height=100,background="black",
                                 borderwidth=0,activebackground=self.root.cget("background"),
                                  command=lambda: [self.add_NotInterested(movie,index)])
            buttonN.grid(row=1, column=0, padx=(2,30), pady=2, sticky='e')
            
            # Sütunların eşit oranda genişlemesi için
            self.root.grid_columnconfigure(index, weight=1)  
            self.root.grid_rowconfigure(1, weight=1)    