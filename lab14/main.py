import struct

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            print(line.strip())

def write_file(filename):
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    with open(filename, "w", encoding="utf-8") as f:
        for l in lines:
            f.write(l + "\n")

def append_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def count_stats(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    line_count = len(lines)
    word_count = 0
    char_count = 0
    for l in lines:
        word_count += len(l.split())
        char_count += len(l)
    return line_count, word_count, char_count

def copy_file(src, dst):
    with open(src, "r", encoding="utf-8") as f1:
        data = f1.read()
    with open(dst, "w", encoding="utf-8") as f2:
        f2.write(data)

def search_replace(src, dst, old, new):
    with open(src, "r", encoding="utf-8") as f:
        data = f.read()
    data = data.replace(old, new)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(data)

def binary_numbers(filename, numbers):
    with open(filename, "wb") as f:
        for n in numbers:
            f.write(struct.pack("i", n))
    total = 0
    with open(filename, "rb") as f:
        while True:
            bytes_data = f.read(4)
            if not bytes_data:
                break
            total += struct.unpack("i", bytes_data)[0]
    return total

def filter_lines(src, dst, keyword):
    with open(src, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(dst, "w", encoding="utf-8") as f:
        for l in lines:
            if keyword in l:
                f.write(l)

def create_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File '{filename}' created successfully!")

while True:
    print("1 read file")
    print("2 write file")
    print("3 append file")
    print("4 count stats")
    print("5 copy file")
    print("6 search replace")
    print("7 binary numbers")
    print("8 filter lines")
    print("9 create file")
    print("10 exit")
    choice = input("choice: ")

    if choice == "1":
        read_file(input("filename: "))
    elif choice == "2":
        write_file(input("filename: "))
    elif choice == "3":
        append_file(input("filename: "), input("text: "))
    elif choice == "4":
        l, w, c = count_stats(input("filename: "))
        print("lines:", l)
        print("words:", w)
        print("chars:", c)
    elif choice == "5":
        copy_file(input("source: "), input("destination: "))
    elif choice == "6":
        search_replace(input("source: "), input("destination: "), input("old: "), input("new: "))
    elif choice == "7":
        nums = list(map(int, input("numbers: ").split()))
        total = binary_numbers(input("filename: "), nums)
        print("sum:", total)
    elif choice == "8":
        filter_lines(input("source: "), input("destination: "), input("keyword: "))
    elif choice == "9":
        create_file(input("filename: "), input("content: "))
    elif choice == "10":
        break