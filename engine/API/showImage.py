import requests
from PIL import Image
import matplotlib.pyplot as plt
import io

def show(url):
    img_url = requests.get(url)
    if img_url.status_code == 200:
        img = Image.open(io.BytesIO(img_url.content))
        # Resmi gösterme
        plt.imshow(img)
        plt.axis('off')  # Eksenleri kapatma
        plt.show()        