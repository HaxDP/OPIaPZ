def calculate_bmi():
    print("Калькулятор індексу маси тіла (IMT)")
    weight = float(input("Введіть вагу (кг): "))
    height = float(input("Введіть ріст (м): "))

    if height <= 0 or weight <= 0:
        print("Помилка: вага та ріст повинні бути позитивними значеннями")
        return

    bmi = weight / (height ** 2)

    print(f"\nВаша вага: {weight} кг")
    print(f"Ваш ріст: {height} м")
    print(f"Індекс маси тіла: {bmi:.2f}")

    if bmi < 18.5:
        category = "Недостатня вага"
    elif bmi < 25:
        category = "Нормальна вага"
    elif bmi < 30:
        category = "Надлишкова вага"
    else:
        category = "Ожиріння"

    print(f"Категорія: {category}")

calculate_bmi()