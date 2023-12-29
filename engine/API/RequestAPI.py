import requests
from API.counting import count
from API.personal_key import API_KEY

def ask(movieID):
    count()
    url = f"http://www.omdbapi.com/?i={movieID}&apikey={API_KEY}&"

    # GET isteği gönderme
    response = requests.get(url)
    if response.status_code == 200:
        # İstek başarılıysa, veriyi alabiliriz
        data = response.json()  # API'den gelen veriyi JSON olarak alır
        for key,value in data.items():
            if key == "Poster":
                return value
            print(f"[{key}] : {value}")
    else:
        print("İstek başarisiz oldu. Hata kodu:", response.status_code)

