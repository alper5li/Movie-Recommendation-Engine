from Dictionary.classify import getType
from Dictionary.classify import returnType,returnSingleType
from Dictionary.classify import keywordIDs
from itertools import chain, combinations


class Movie():
    def __init__(self,id,name,adult,year,types,rating,vote):
        self.id = id
        self.name = name
        self.adult = adult
        self.year = year
        self.types = types
        self.rating = rating
        self.vote = vote
        self.sentence = Sentence(getType(types),len(types))
        self.keywords = set()
    
    # Sets keywords set using movie plot
    def setKeywords(self,plot):
        self.keywords = keywordIDs(plot)


# {A,B,C,D,F,G,H,J} 
class Sentence():
    """
    Logical statement about a Movie.
    A sentence consists of a set of movie types
    """
    
    '''
        A = action
        B = drama
        C = sciencefiction
        D = thriller
        E = crime
        F = adventure
        G = fantasy
        ...
    
    '''
    def __init__(self, types, count):
        self.types = set(types)     # {A,B,C,D,F,G,H,J}  
        self.count = count          #     8
    
    def remove(self):
        self.count -= 1
        return self.types.pop()
        
class MovieAi():
    '''
    Ai uses past knowledge and updates 
    its knowledge every single interaction.
    After all, it will generate a set of types
    for suggest movie. 
    '''    
    
    def __init__(self):
        
        # Track Movies
        self.Movies = set()
        
        # Track Interested Movies
        self.InterestedMovies = set()
        
        # Track Not Interested Movies 
        self.NotInterestedMovies = set()
        
        # Interested Movies Types
        self.Interested = set()
        
        # Not Interested Movies Types
        self.NotInterested = set()
        
        # Track types
        self.usedTypes = set()
        
        # Track Ai's next advice types for next question.
        self.adviceTypes = set()
        
        # Track adviceTypes's all possible combinations. 1 to 3
        self.advice_combinations = set()
        
        # Track only interested keywords based on movie's plot 
        self.interested_keywords = set()
        
        # Track only not intersested keywords based on movie's plot 
        self.not_interested_keywords = set()
        
        # Track interested keywords - not interested keywords
        self.keywords_knowledge = set()
        
        # Tracks interested knowledge based on genres
        self.knowledge =[]
    
    # adds movie types to Interested set   
    def mark_InterestedTypes(self,movie):
        for type in movie.sentence.types:
            self.Interested.add(type)
    
    # adds movie types to NotInterested set      
    def mark_notInterestedTypes(self,movie):
        for type in movie.sentence.types:
            self.NotInterested.add(type)
           
    # adds movie types to usedTypes set
    def mark_usedTypes(self,movie):
        for type in movie.sentence.types:
            self.usedTypes.add(type)
    
    def mark_interested_keywords(self,movie):
        self.interested_keywords.update(movie.keywords)
            
    def mark_not_interested_keywords(self,movie):
        self.not_interested_keywords.update(movie.keywords)

    
    # Updates knowledge whenever gets interaction with user.  
    def add_knowledge(self,movie,interest):
        '''
        This function should :
            1) mark a movie its been used 
            2) mark interest of that movie 
            3) mark keywords of that movie
            4) mark types its been used 
            5) update [knowledge] with this knowledge
            6) update advice types
            7) update advice_combinations based on advicetypes
            8) update keywords_knowledge based on interested_keywords and not_interested_keywords
        '''
        
        "(1)"
        self.Movies.add(movie)
        
        "(2)"
        if interest == 0:
            self.NotInterestedMovies.add(movie)
            self.mark_notInterestedTypes(movie)
            "(3)"
            self.mark_not_interested_keywords(movie)
        elif interest == 1:
            self.InterestedMovies.add(movie)
            self.mark_InterestedTypes(movie)
            "(3)"
            self.mark_interested_keywords(movie)
        
        "(4)"
        self.mark_usedTypes(movie)        
    
        "(5)"
        for typ in movie.sentence.types:
            if typ not in self.knowledge:                        
                self.knowledge.append(typ)

        "(6)"       
        if interest == 0:
            for _ in movie.sentence.types.copy():
                singleType = movie.sentence.remove()
                if singleType in self.adviceTypes:
                    self.adviceTypes.remove(singleType)
        elif interest == 1:
            for _ in movie.sentence.types.copy():
                singleType = movie.sentence.remove()
                if singleType not in self.adviceTypes:
                    self.adviceTypes.add(singleType)    
        for notint in self.NotInterested:
            if notint in self.adviceTypes:
                self.adviceTypes.remove(notint)
        "(7)"
        self.advice_combinations.clear()
        comb = set()
        
        for r in range(1, 4):
            comb.update(combinations(self.adviceTypes, r))
        for c in comb:
            if len(c) > 1:  
                self.advice_combinations.add(tuple(c))
            elif c:  
                self.advice_combinations.add(c[0])
        "(8)"
        self.keywords_knowledge = self.interested_keywords - self.not_interested_keywords
        
        
def example():
    '''
    EXAMPLE DEMO START

    '''
            
            
            
    Interested_Movies = [
        "Adult,Crime,Family",
        "Short,Sci-Fi,Romance",
        "Game-Show,Comedy,Crime",
        "History,Film-Noir,Drama",
        "News,Fantasy,Crime",
    ]


    NotInterested_Movies = [
        "Musical,Music,Family",
        "Talk-Show,Documentary,News",
        "Music,Reality-Tv,Romance",
        "Film-Noir,History,Drama",
        "Crime,Sport,Thriller",
    ]



    namelist = [
        "Godfather",
        "Narnia",
        "Game Of Thrones",
        "Lost",
        "Nemo"
    ]

    namelist2 = [
        "365 Day",
        "Harry Poter",
        "Star Wars",
        "Thor",
        "Cars"
    ]

    InterestedMovies = set()
    Not_InterestedMovies = set()


    # INTERESTED 
    for i in range(len(Interested_Movies)):
        makeMovie = Movie(i,namelist[i],1,2022,Interested_Movies[i],9,100)
        InterestedMovies.add(makeMovie)

    # NOT INTERESTED 
    for j in range(len(NotInterested_Movies)):
        makeMovie = Movie(i,namelist[j],0,2019,Interested_Movies[j],9,100)
        Not_InterestedMovies.add(makeMovie)

    Ai = MovieAi()

    for movie in InterestedMovies:
        Ai.add_knowledge(movie,1)  # 1 == interested
        
    for movie3 in Not_InterestedMovies:
        Ai.add_knowledge(movie3,0)  # 0 == Not interested  
        



    # Representation 
    for m in range(len(Ai.Movies)):
        movies_list = list(Ai.Movies)
        print(f"Movies = {movies_list[m].name}")
        
    print(f"Interested = {Ai.Interested}")
    print(f"Not Interested = {Ai.NotInterested}")
    print(f"used Types = {Ai.usedTypes}")
    print(f"Advice Types = {Ai.adviceTypes}")
    print(f"knowledge = {Ai.knowledge}")

    for k in Ai.knowledge:
        print(k)

    print(f"I ADVICE YOU {returnTypesList(Ai.adviceTypes)} TYPES FILMS.")

    '''
    EXAMPLE DEMO END

    '''