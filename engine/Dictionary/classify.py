import json 

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

key_dict = {}

with open(r"engine\Dictionary\unique_keylist.json", 'r') as file:
        key_dict = json.load(file)


def getType(types):
    signs = set()
    typelist = types.split(',')
    for type in typelist:
        signs.add(findKey(type))
    return signs
        
# Eger classifylanmamis bir kategori ise 0 dondurur.
def findKey(type):
    for d in dict:
        for key,val in d.items():
            if val == type:
                return key
    return None

def returnType(types):
    list = []
    for type in types:
        if findValue(type) != None:
            list.append(findValue(type))
    return list

def returnSingleType(letter):
    if findValue(letter) != None:
        return findValue(letter)

def findValue(type):
    for d in dict:
        for key,val in d.items():
            if key == type:
                return val
    return "0"

# returns keyID set using plot input
def keywordIDs(plot):
    keywords = plot.split()
    # Eşleşen anahtarları bulmak için set comprehension kullanabiliriz
    keyIDs = {key for plot_word in keywords for key, word in key_dict.items() if plot_word == word}
    return keyIDs