def read():
    try:
        unique_elements = set()  # Using a set to store unique elements
        with open('genres.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                elements = line.split(",")
                for el in elements:
                    unique_elements.add(el.strip())  # Adding each element to the set

        with open('categories.txt', 'a') as file:
            for el in unique_elements:
                file.write(el + "\n")  # Writing unique elements to the file

    except FileNotFoundError:
        print(0)

    
    
def sirala():
    try:
        with open('categories.txt', 'r') as file:
            lines = file.readlines()
            lines.sort()  # Satırları alfabetik olarak sırala

        with open('categories_sorted.txt', 'w') as sorted_file:
            for line in lines:
                sorted_file.write(line)  # Sıralanmış satırları yeni dosyaya yaz

    except FileNotFoundError:
        return 0

sirala()