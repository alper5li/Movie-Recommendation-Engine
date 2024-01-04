import requests
import time

def checkNetwork(url="www.ombdapi.com"):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        if response.status_code == 200:
            ping_time = (end_time - start_time) * 1000  # in milliseconds
            return ((f"Ping to {url} is {ping_time:.2f} ms"),True)
        else:
            return ((f"Failed to connect server : {url}"),False)
    except requests.RequestException as e:
        return ((f"Failed to ping : {url}"),False)