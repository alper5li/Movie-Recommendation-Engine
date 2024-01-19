from Dictionary.printcolors import printGreen,printBlue,printRed,printYellow
from Dictionary.classify import returnType,returnSingleType
from Helpers.gif_animation import AnimatedGIFLabel
from tkinter.ttk import Progressbar as PB
from API.Network import checkNetwork
import matplotlib.pyplot as plt
from API.RequestAPI import ask
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as ttk
from tqdm import tqdm
import pandas as pd
from Ai import *
import threading
import requests
import random

algorithm_type = 'keywords'

def set_algorithm_type(algorithm):
    global algorithm_type
    algorithm_type = algorithm
    

class NetworkError():
    '''
    If program will face with Network Error, this class will be called.
    '''
    
    def __init__(self,root,url):
        self.root = root
        self.url = url
        self.center_window(800,300)
        self.root.title("Network Error")
        self.root.configure(bg="black")
        self.status = True
        self.retry_count = 1
        
        font = ('Helvetica',24)
        
        self.info = ttk.Label(text="Failed to connect API server.",foreground='red',background='black',font=font)
        self.info_request = ttk.Label(foreground='red',background='black',wraplength=600,font=font)
        self.info_count = ttk.Label(text='1',foreground='yellow',background='black')
        self.retry_button  = ttk.Button(text='Retry',foreground="green",bg='black',command=self.Retry)
        
        self.info.place(anchor = "center", relx = .5, rely = .2)
        self.info_request.place(anchor = "center", relx = .5, rely = .5)
        self.info_count.place(anchor = "center", relx = .5, rely = .7)
        self.retry_button.place(anchor="center",relx=.5,rely=.8)
        
            
    def Retry(self):
        url = self.url
        self.retry_count += 1
        info_request,status = checkNetwork(url)
        self.info_request.configure(text=info_request)
        self.info_count.configure(text=self.retry_count)
        if(status):
            self.forgot_all()
            self.status=False
            Start(self.root)

    def forgot_all(self):
        self.remove_widgets(self.root)
    
    # Removes all root widgets 
    def remove_widgets(self,root):
        for widget in root.winfo_children():
            widget.destroy()
            
    def center_window(self,width,height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = (screen_width - width) / 2
        y_coordinate = (screen_height - height) / 2
        self.root.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")

class Start():
    '''
    It will shown Welcome Page for the user.
    '''
    def __init__(self, root):
        self.root = root
        self.center_window(1600,700)
        self.root.title("Movie Recommendation Engine")
        self.root.configure(bg="black")
        self.bindReference = self.root.bind('<Return>', self.switch_to_Age_class)
        self.main()

    def center_window(self,width,height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = (screen_width - width) / 2
        y_coordinate = (screen_height - height) / 2
        self.root.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")
        
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
        
class Age():
    '''
    Age Class gets age as a input from user to decide User is Adult or Not 
    '''
    
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

class Recommendation():
    '''
    The Main Recommendation Program.
    '''
    
    '''
    THREADING PART
    '''
    
    # Set information widgets while threading and starts threading 
    def getMovies(self):
        self.info_label["text"] = "Loading Data ..."
        self.info_label.place(anchor = "center", relx = .5, rely = .2)
        self.follow_progress["text"] = f"remaining files {0}/{0}"
        self.follow_progress.place(anchor = "center", relx = .5, rely = .45)
        t = threading.Thread(target=self.getData)
        t.start()
        # Start checking periodically if the thread has finished.
        self.schedule_check(t)
        
    # Gets Data From Local Dataset
    def getData(self):
        raw = pd.read_csv(r"engine\Datasets\keywords.csv", delimiter=',', encoding='utf-8', low_memory=False)
        keywords = pd.read_csv(r"engine\Datasets\key_ids.csv", delimiter=',', encoding='utf-8', low_memory=False)
        movieListAll = []
        if self.isAdult:
            rowNumber = raw.shape[0] 
            for i in range(rowNumber):
                self.follow_progress["text"] = f"remaining files {i}/{rowNumber}"
                self.progress_var.set((i/rowNumber) * 100)
                createMovie = Movie(raw.iloc[i][0],raw.iloc[i][2],raw.iloc[i][3],raw.iloc[i][4],raw.iloc[i][5],raw.iloc[i][6],raw.iloc[i][7],keywords.iloc[i][1])
                movieListAll.append(createMovie)
        
        else:
            raw = raw[raw['isAdult'] == 0] 
            rowNumber = raw.shape[0]
            for i in range(rowNumber):
                self.follow_progress["text"] = f"remaining files {i}/{rowNumber}"
                self.progress_var.set((i/rowNumber) * 100)
                createMovie = Movie(raw.iloc[i][0],raw.iloc[i][2],raw.iloc[i][3],raw.iloc[i][4],raw.iloc[i][5],raw.iloc[i][6],raw.iloc[i][7],keywords.iloc[i][1])
                movieListAll.append(createMovie)
        
        self.AllMovies = movieListAll
        self.length = len(self.AllMovies) - 1
   
    # Checking Periodically if the task is ended     
    def schedule_check(self,task):
        self.root.after(1000, self.check_if_done, task)
    
    # If task is ended, it will route to the main function. If not checks again.
    def check_if_done(self,task):
        if not task.is_alive():
            self.info_label.configure(text="File successfully downloaded!") 
            self.info_label.place_forget()
            self.main()
        else:
            self.progress_var.set(50)
            self.schedule_check(task)
   
    '''
    END OF THREADING PART
    '''        
    
    # Assignin Ai and Threading Widgets.
    def __init__(self,root,isAdult=21):
        self.root = root
        self.isAdult = isAdult
        
        # Setting Our Loading Duck
        duck_gif1 = r"engine\Images\duck.gif"
        self.duck1 = AnimatedGIFLabel(self.root,duck_gif1)
        self.duck1.place(anchor = "center", relx = .15, rely = .5)
        
        # Setting Our Loading Duck
        duck_gif2 = r"engine\Images\duck_r.gif"
        self.duck2 = AnimatedGIFLabel(self.root,duck_gif2)
        self.duck2.place(anchor = "center", relx = .85, rely = .5)
        
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
            movies.append(self.generateRandomMovie(1000))
        return movies
    
    # it will return image of specified movie, assign poster into allocated memory using self.images and returns itself
    def API_Data(self,index,movie):
        try:
            result = ask(movie.id)
            url = result[0]
            Plot = result[1]
            printBlue(f"{movie.name} : {url}")
            response=requests.get(url)
            img_data = response.content
            # Resmi PIL ile aç
            image = Image.open(BytesIO(img_data))
            # Resmi PhotoImage olarak dönüştür
            photo = ImageTk.PhotoImage(image)
                
            self.images[index] = photo  
            self.plots[index] = Plot
            return self.images[index]  
                
        except requests.exceptions.MissingSchema:
            self.Exception_API_Data(index)  
    
    # If Exception occurs during API_Data, it will try to generate another movie which has an image at API database
    def Exception_API_Data(self,index):
        newMovie = self.generateRandomMovie(1000)
        self.showPoster(index,newMovie) 

    # Gets Local Image for using at the [Interested] button
    def Approve_Image(self):
        img = Image.open(r"engine\Images\approve.png")
        
        img = img.resize((100,100))
        
        photo = ImageTk.PhotoImage(img)
        return photo
    
    # Gets Local Image for using at the [Not interested] button
    def NotApprove_Image(self):
        img = Image.open(r"engine\Images\notapprove.png")
        
        img = img.resize((100,100))
        
        photo = ImageTk.PhotoImage(img)
        return photo
    
    # Outputs Current Ai information
    def Ai_Info(self):
        print()
        printGreen(f"Interested Types= {sorted(list(self.Ai.Interested))}")
        printRed(f"Not Interested Types = {sorted(list(self.Ai.NotInterested))}")
        printYellow(f"Before Used Types = {sorted(list(self.Ai.usedTypes))}")
        printBlue(f"Ai Knowledge of Types = {sorted(list(self.Ai.knowledge))}")
        print()
        printGreen(f"Advice Types = {sorted(list(self.Ai.adviceTypes))}")
        printGreen(f"Advice Types = {returnType(sorted(list(self.Ai.adviceTypes)))}")
        printGreen(f"Combinations of Adviced Types = {list(self.Ai.advice_combinations)}")        
        printGreen(f"Length of Combined Advice Types : [{len(self.Ai.advice_combinations)}]") 
        print()
        printYellow(f"Interested keywords : {self.Ai.interested_keywords}")
        printYellow(f"Not Interested keywords : {self.Ai.not_interested_keywords}")
        printYellow(f"Advice Keywords : {self.Ai.keywords_knowledge}")
        printYellow(f"length of advice keywords : {len(self.Ai.keywords_knowledge)}")
        printYellow(f"advised types : {self.advised_types}")
        print()

    # Adding Movie into Ai's knowledge as interested
    def add_Interested(self,movie,index):
        # setting keywords of movie using its own plot
        movie.setKeywords(self.plots[index])
        
        printYellow(f"interested keywords length {len(self.plots[index])}")
        printYellow(f"interested keywords {','.join((self.plots[index]).split())}")

        self.Ai.add_knowledge(movie,1)
        self.count += 1
        
        # reset the current poster and movie
        newMovie = self.generateRandomMovie(1000) 
        self.currentMovies[index] = newMovie
        self.showPoster(index,newMovie)
        
        # Prints current Ai information
        self.Ai_Info()
        
        # Checks if its done, if no, generates another movie
        self.checkAdvice()

    # Adding Movie into Ai's knowledge as not interested    
    def add_NotInterested(self,movie,index):
        # setting keywords of movie using its own plot
        movie.setKeywords(self.plots[index])
        
        self.Ai.add_knowledge(movie,0)
        self.count += 1

        # reset the current poster and movie
        newMovie = self.generateRandomMovie(1000) 
        self.currentMovies[index] = newMovie
        self.showPoster(index,newMovie)
        # Prints current Ai information
        self.Ai_Info()
        
        # Checks if its done, if no, generates another movie
        self.checkAdvice()

    # Gets Random Movie from AllMovies
    def generateRandomMovie(self,recursion_count):
        if recursion_count >100:
            length = self.length
            x = random.randint(0,length)
            if not self.AllMovies[x].sentence.types.isdisjoint(self.advised_types) and len(self.advised_types) < 15:
                # Generate another movie
                recursion_count -= 1
                return self.generateRandomMovie(recursion_count) 
            else:
                movie = self.AllMovies[x]
                self.advised_types.update(movie.sentence.types)
                return movie
        else:
            print(f"Generating another random movie...")
            for x in tqdm(range(len(self.AllMovies))):
                if not self.AllMovies[x].sentence.types.isdisjoint(self.advised_types):
                    return x     
            length = self.length
            r = random.randint(0,length)
            print(f"No disjoint movies left. Assignin random movie...")   
            return self.AllMovies[r]
    
    # EventHandler for plot information   
    def show_text(self,event,content):
        self.plotInfo.configure(text=content)
   
    # EventHandler for plot information  
    def hide_text(self,event):
        self.plotInfo.configure(text="")
   
    # Shows and Updates Poster 
    def showPoster(self,index,movie):
            frame = ttk.Frame(self.root,bg="black")
            frame.grid(row=1, column=index, sticky="nsew")
            
            label = ttk.Label(frame, image=self.API_Data(index,movie),justify="center",)
            label.grid(row=0, column=0, padx=5, pady=5)
            self.labels.append(label)
            
            label.bind("<Enter>", lambda event, content=self.plots[index]: self.show_text(event,content)) # After Mouse on Hover image, show_text() will execute
            label.bind("<Leave>", lambda event , content = "": self.hide_text(event))  # After Mouse Leave hide_text() will execute
            
            
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
            
    # Main widgets here
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
        
        # Setting previously advised types set. Its updating after everyy interaction
        self.advised_types = set()
        
        # Stores Only Current Shown Movies, It should update after every interaction, 
        self.currentMovies = self.assignRandomMovies(5)
        
        # Stores Only Current Shown Movies Pictures, It should update after every interaction
        self.images = ['poster1','poster2','poster3','poster4','poster5']
        
        # Stores Only Shown Movies Plots , It should update after every interaction
        self.plots = ['','','','','']
        
        
        # Stores Labels which holds current Images
        self.labels = []
        
        # Represents User is either Adult Or Not.        
        self.label = ttk.Label(self.root, text=f"Are You adult : {self.isAdult}",foreground="white", background="black")        
        self.label.grid(row=0, column=0, columnspan=len(self.images), pady=5)
        
        # Represent Plots after mousehover the movie poster
        plotFont = ('Helvetica',12)
        self.plotInfo =  ttk.Label(self.root, text="",foreground="green", background="black")  
        self.plotInfo.configure(font=plotFont)
        self.plotInfo.grid(row=0, column=0, columnspan=len(self.images), pady=5)  
        
        # Check input count. If reached expected, checkAdvice() will advice movie 
        self.count=0
        
        # Loop for each movie label 
        for index,movie in enumerate(self.currentMovies):
            self.showPoster(index,movie)
        ## ERR 
        #self.labels.grid(pady=5)
    
    # Checks total interest count for redirecting Advice Page
    def checkAdvice(self):
        if self.count >=5:
            # forget widgets 
            self.remove_widgets(self.root)
            # call another page for advice 
            Advice(self.root,self.Ai)

    # Removes all root widgets 
    def remove_widgets(self,root):
        for widget in root.winfo_children():
            widget.destroy()
            
class Advice():
    '''
    After Recommendation, Advice will called to show what is adviced based on choices.
    '''

    def __init__(self,root,Ai):
        self.root = root
        self.root.title("Movie Recommendation Results")
        self.Ai= Ai
        self.main()
    
    "simple bubble sort algortihm"
    def bubble_sort(self,arr):
        n = len(arr)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if len(arr[j]) < len(arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    "(0) shows previous selected movies in the window"
    def previousSelected(self):
        i_movies = self.previous_selected_interested_movies
        ni_movies = self.previous_selected_not_interested_movies
        string_info = "Interested movies\n"
        for m in i_movies:
            string_info += m.name+"\n"
        
        string_info+="\n"
        
        string_info += "Not Interested movies\n"
        for nm in ni_movies:
            string_info += nm.name+"\n"
            
        return string_info
        
    "(1) sorting Ai advice combinations using bubble sort algorithm"
    def calculation(self):
        before_sort = (list(self.Ai.advice_combinations))
        after_sort = self.bubble_sort(before_sort)
        for adv in after_sort:
            adv = sorted(adv)
        return after_sort

    "(2) returns letter's corresponding words "
    def create_advice_list(self):
        advices = self.advices
        advices_with_letter = []
        for advice in advices:
            "('I','Z','A')"
            adv = []
            for letter in advice:
                adv.append(returnSingleType(letter))
                
            advice_w_l = ",".join(adv)         
            advices_with_letter.append(advice_w_l)   
            
        return advices_with_letter
            
    "(3) using genres to make list " 
    def adviced_movies_list(self):
        advices = self.create_advice_list() 
        df = pd.read_csv(r'engine\Datasets\keywords.csv')
        key_ids = pd.read_csv(r'engine\Datasets\key_ids.csv')

        movies = []
        for advice in advices:
            types = advice
            if (types in df['genres'].values):
                print(f"Types : {types}")
                row = df[df['genres'] == types].iloc[0] # We can select other movies using iloc, not we will get first film as default.
                keys = key_ids[key_ids['tconst']==row['tconst']].iloc[0]
                advMovie = Movie(row['tconst'],row['originalTitle'],row['isAdult'],row['startYear'],row['genres'],row['averageRating'],row['numVotes'],keys['keyID'])
                movies.append(advMovie)
        self.movies = movies
    
    "(3) using keywords to make list" 
    def adviced_movies_list_using_keywords(self):
        local_movies = pd.read_csv(r'engine\Datasets\keywords.csv')
        key_ids = pd.read_csv(r'engine\Datasets\key_ids.csv')
        words = self.Ai.keywords_knowledge
        movieID = []
        
        all_keywords = set(words)
        for index,row in tqdm(key_ids.iterrows(),total=len(key_ids)):
            # OPTIMIZASYON SORUNU
            movie_word_ids =set(row['keyID'].split())

            common_words = movie_word_ids.intersection(all_keywords)
            
            # Ortak kelime varsa, movieID listesine ekleyin
            if common_words:
                movieID.append((row['tconst'], len(common_words)))
        
        # sort it using count 
        sorted_movies = sorted(movieID, key=lambda x: x[1],reverse=True)
        print(sorted_movies)
        
        movieList = []
        
        sorted_movies_set = [movieIDs[0] for movieIDs in sorted_movies[:10]] # Setting up advice film list range : 10
        
        for movieID in sorted_movies_set:
            if movieID in local_movies['tconst'].values:
                row = local_movies[local_movies['tconst'] == movieID].iloc[0]
                keys = key_ids[key_ids['tconst']== movieID].iloc[0]
                advMovie = Movie(row['tconst'],row['originalTitle'],row['isAdult'],row['startYear'],row['genres'],row['averageRating'],row['numVotes'],keys['keyID'])
                movieList.append(advMovie)
        self.movies = movieList
        print(f"MOVIES : {(self.movies)}")
    
    "(4) creating graph"
    def create_graphs(self):
        # [movies] = movies which will be advised in the next section
        # [Ai]     = movies which were be used to select advised movies past
        movies = self.movies
        X = [] # assign X 
        Y_keywords = []
        Y_categories = []
        Y_similarity_percentage = []
        
        for movie in movies:
            # movies names assigned to X 
            X.append(movie.name)
            # calculate how many categories joint with Ai knowledge, assigned to Y_categories
            joint_categories = list(movie.sentence.types.intersection(self.Ai.adviceTypes))
            Y_categories.append(len(joint_categories))
            # calculate how many keywords is joint with Ai knowledge, assigned to Y_keywords
            print(f"Keywords = {list(movie.keywords)}")
            print(f"Knowledge = {list(self.Ai.keywords_knowledge)}")
            joint_keywords = list(movie.keywords.intersection(self.Ai.keywords_knowledge))
            Y_keywords.append(len(joint_keywords))
            
        # Graph
        plt.plot(X,Y_keywords,label="Keyword Similarity",color='green',marker='o')
        plt.plot(X,Y_categories,label="Categories Similarity",color='red',linestyle='--')

        plt.xlabel('Advised Movies')
        plt.ylabel('Similarities')
        plt.title('Graph')
        
        plt.legend()
        plt.show(block=False)
        
        
    "(5) shows adviced movie in the window"
    def showAdvice(self):
        index = self.index
        movieID = self.movies[index].id
        self.label = ttk.Label(self.root, image=self.API_Data(movieID),justify="center",)
        self.label.place(anchor = "center", relx = .5, rely = .5)
        
        self.button_next = ttk.Button(self.root,text="Next",command=lambda:self.updateAdvice())
        self.button_next.place(anchor = "center", relx = .8, rely = .8)
    
    "(6) it will return image of specified movie, assign poster into allocated memory using self.images and returns itself"
    def API_Data(self,movieID):
        try:
            result = ask(movieID)
            url = result[0]
            Plot = result[1]
            response=requests.get(url)
            img_data = response.content
            # Resmi PIL ile aç
            image = Image.open(BytesIO(img_data))
            # Resmi PhotoImage olarak dönüştür
            photo = ImageTk.PhotoImage(image)
                
            self.image = photo  
            self.plot.configure(text=Plot)
            return self.image  
                
        except requests.exceptions.MissingSchema:
            print("Exception Occured")
  
    "(7) updates showAdvice to advice next movie"
    def updateAdvice(self):
        self.index += 1
        self.showAdvice()     
  
    "(main)"
    def main(self):
        self.previous_selected_interested_movies = self.Ai.InterestedMovies
        self.previous_selected_not_interested_movies = self.Ai.NotInterestedMovies

        self.previous_information = ttk.Label(text="You selected these films : ",foreground='yellow',background="black")
        self.selected_movies = self.previousSelected()
        self.previous_selected_movies_label = ttk.Label(text=self.selected_movies,foreground='green',background="black", wraplength=400)
        self.previous_selected_movies_label.place(anchor='center',relx=.8,rely=.1)
        
        self.advices = self.calculation()
        self.index = 0
        self.image = None
        
        plotFont = ('Helvetica', 16)
        self.plot = ttk.Label(text="this is plot",foreground='green',background="black", wraplength=500)
        self.plot.configure(font=plotFont)
        self.plot.place(anchor = "center", relx = .5, rely = .1)
        
        self.movies = []
        
        "OPTIONAL - YOU CAN DECIDE WHICH ALGORITHM WILL BE USED"
        if algorithm_type == 'keywords':
            self.adviced_movies_list_using_keywords()
        elif algorithm_type == 'genres':
            self.adviced_movies_list()
        
        # Now We have movies in self.movies. Lets create a graph of similarity percentage and matching keyword / mathching genres count based on films
        self.create_graphs()
        
        self.showAdvice()
        
        
        
    