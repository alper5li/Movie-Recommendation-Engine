def read():
    try:
        with open('counter.txt', 'r') as file:
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

def count():
    # Önce dosyadan değeri oku
    counter = read()

    if counter > 0:
        # Sayacı azalt
        counter -= 1
        update(counter)
        print("Kalan API Hakki : ", counter)
    else:
        print("Dosya bulunamadi.")
