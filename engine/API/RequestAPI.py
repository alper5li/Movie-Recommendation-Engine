import requests
from Dictionary.printcolors import printCyan,printRed
from API.counting import API_inf
from API.personal_key import API_KEY

def ask(movieID):
    API_inf()
    url = f"http://www.omdbapi.com/?i={movieID}&apikey={API_KEY}&"
    Plot = ""
    posterURL = ""
    # GET request
    response = requests.get(url)
    if response.status_code == 200:
     
        data = response.json() 
        for key,value in data.items():
            if key == "Poster":
                posterURL = value
            if key == "Plot":
                Plot = value
            if value =="N/A":
                printRed(f"[{key}] : {value}")
            else:
                printCyan(f"[{key}] : {value}")
    else:
        printRed("İstek başarisiz oldu. Hata kodu:", response.status_code)
        
    return posterURL,Plot