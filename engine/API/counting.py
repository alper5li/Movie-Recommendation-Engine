def read():
    try:
        with open('engine/API/counter.txt', 'r') as file:
            content = file.read().strip()
            if content:
                return int(content)
            else:
                return 0
    except FileNotFoundError:
        # Dosya bulunamazsa veya ilk çalıştırıldığında dosya yoksa 0 döndür
        return 0

def update(value):
    with open('counter.txt', 'w') as file:
        file.write(str(value))

def API_inf():
    print("Sending API ...")
