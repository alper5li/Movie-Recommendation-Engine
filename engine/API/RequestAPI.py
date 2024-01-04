import requests
from API.counting import API_inf
from API.personal_key import API_KEY

def ask(movieID):
    count()
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
            print(f"[{key}] : {value}")
    else:
        print("İstek başarisiz oldu. Hata kodu:", response.status_code)
        
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