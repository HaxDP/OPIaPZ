year = int(input("Введіть рік: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print("Високосний рік")
else:
    print("Не високосний рік")