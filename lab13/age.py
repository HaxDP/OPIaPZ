def determine_age_category():
    print("Визначення вікової категорії")
    birth_year = int(input("Введіть рік народження: "))
    current_year = 2026

    age = current_year - birth_year

    if age < 0:
        print("Помилка: рік народження не може бути в майбутньому")
        return

    print(f"\nВік: {age} років")

    if age < 1:
        category = "Новонароджена дитина"
    elif age < 3:
        category = "Малюк"
    elif age < 7:
        category = "Дошкільник"
    elif age < 13:
        category = "Молодша школа"
    elif age < 18:
        category = "Підліток"
    elif age < 30:
        category = "Молодий дорослий"
    elif age < 60:
        category = "Дорослий"
    elif age < 75:
        category = "Пенсіонер"
    else:
        category = "Літня людина"

    print(f"Категорія: {category}")

determine_age_category()