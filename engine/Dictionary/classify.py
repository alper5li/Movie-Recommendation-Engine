
dict = [
    {'A': 'Action'}, 
    {'B': 'Adult'}, 
    {'C': 'Adventure'}, 
    {'D': 'Animation'}, 
    {'E': 'Biography'}, 
    {'F': 'Comedy'}, 
    {'G': 'Crime'}, 
    {'H': 'Documentary'}, 
    {'I': 'Drama'}, 
    {'J': 'Family'}, 
    {'K': 'Fantasy'}, 
    {'L': 'Film-Noir'}, 
    {'M': 'Game-Show'}, 
    {'N': 'History'}, 
    {'O': 'Horror'}, 
    {'P': 'Music'}, 
    {'Q': 'Musical'}, 
    {'R': 'Mystery'}, 
    {'S': 'News'}, 
    {'T': 'Reality-TV'}, 
    {'U': 'Romance'}, 
    {'V': 'Sci-Fi'}, 
    {'W': 'Short'}, 
    {'X': 'Sport'}, 
    {'Y': 'Talk-Show'}, 
    {'Z': 'Thriller'}, 
    {'[': 'War'}, 
    {']': 'Western'}, 
    {'\\': '\\N'}
]

def getType(types):
    signs = set()
    for type in types:
        signs.add(findKey(type))
    return signs
        
        
# Eger classifylanmis bir kategori ise 0 dondurur.
def findKey(type):
    for d in dict:
        for key,val in d.items():
            if val == type:
                return key
    return "0"


def returnType(types):
    signs = set()
    for type in types:
        signs.add(findValue(type))
    return signs


def findValue(type):
    for d in dict:
        for key,val in d.items():
            if key == type:
                return val
    return "0"
