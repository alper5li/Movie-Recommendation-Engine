import requests
from engine.API.showImage import show
from engine.API.counting import count
from engine.API.personal_key import API_KEY

movieName = input("Movie Title : ")
count()
url = f"http://www.omdbapi.com/?t={movieName}&apikey={API_KEY}&"

# GET isteği gönderme
response = requests.get(url)

if response.status_code == 200:
    # İstek başarılıysa, veriyi alabiliriz
    data = response.json()  # API'den gelen veriyi JSON olarak alır
    for key,value in data.items():
        if key == "Poster":
            show(value)
        print(f"[{key}] : {value}")
else:
    print("İstek başarisiz oldu. Hata kodu:", response.status_code)


