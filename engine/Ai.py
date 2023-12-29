from Dictionary.classify import getType
from Dictionary.classify import returnType
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
        # Other additional informations like rating, views etc.
        

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
        
        # Interested Movies
        self.Interested = set()
        
        # Not Interested Movies
        self.NotInterested = set()
        
        # Track types
        self.usedTypes = set()
        
        # Track Ai's next advice types for next question.
        self.adviceTypes = set()
        
        # Tracks interested knowledge
        self.knowledge =[]
    
    # adds movie types to Interested set   
    def mark_InterestedTypes(self,movie):
        for type in movie.sentence.types:
            self.Interested.add(type)
    
    # adds movie types to NotInterested set      
    def mark_notInterestedTypes(self,movie):
        for type in movie.sentence.types:
            self.NotInterested.add(type)
            
    def mark_usedTypes(self,movie):
        for type in movie.sentence.types:
            self.usedTypes.add(type)
    
    # Updates knowledge whenever gets interaction with user.  
    def add_knowledge(self,movie,interest):
        '''
        This function should :
            1) mark a movie its been used 
            2) mark interest of that movie 
            3) mark types its been used 
            4) update [knowledge] with this knowledge
            5) update advice types
        
        '''
        
        "(1)"
        self.Movies.add(movie)
        
        "(2)"
        if interest == 0:
            self.mark_notInterestedTypes(movie)
        elif interest == 1:
            self.mark_InterestedTypes(movie)
        
        "(3)"
        self.mark_usedTypes(movie)        
    
        "(4)"
        all_subsets = list(chain.from_iterable(combinations(movie.sentence.types, r) for r in range(len(movie.sentence.types) + 1)))
        for subset in all_subsets:
            if subset not in self.knowledge:
                self.knowledge.append(subset)
        "(5)"       
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

        all_subsets_in_advice = set()
        for r in range(2, 4):  # 2 ile 3 elemanlı kombinasyonları almak için
            subsets = combinations(self.adviceTypes, r)
            all_subsets_in_advice.update(subsets)

        for subset in all_subsets_in_advice:
            self.adviceTypes.add(subset)
        

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

    print(f"I ADVICE YOU {returnType(Ai.adviceTypes)} TYPES FILMS.")

    '''
    EXAMPLE DEMO END

    '''