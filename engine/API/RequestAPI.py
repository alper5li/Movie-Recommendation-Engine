import requests
from Dictionary.printcolors import printCyan,printRed
from API.counting import API_inf
from API.personal_key import API_KEY

def ask(movieID):
    API_inf()
    url = f"http://www.omdbapi.com/?i={movieID}&apikey={API_KEY}&"
    Plot = ""
    posterURL = ""
    # GET isteği gönderme
    response = requests.get(url)
    if response.status_code == 200:
        # İstek başarılıysa, veriyi alabiliriz
        data = response.json()  # API'den gelen veriyi JSON olarak alır
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

def getPlot(movieID):
    url = f"http://www.omdbapi.com/?i={movieID}&apikey={API_KEY}&"
    Plot = ""
    # GET isteği gönderme
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # API'den gelen veriyi JSON olarak alır
        for key,value in data.items():
            if key == "Plot":
                Plot = value
                return Plot