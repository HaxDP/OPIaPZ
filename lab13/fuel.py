def calculate_fuel_economy():
    print("Калькулятор витрати палива")
    distance = float(input("Введіть пройдену відстань (км): "))
    fuel_consumed = float(input("Введіть спожите пальне (л): "))
    fuel_price = float(input("Введіть ціну палива (грн/л): "))

    if distance <= 0 or fuel_consumed <= 0 or fuel_price <= 0:
        print("Помилка: всі значення повинні бути позитивними")
        return

    economy = distance / fuel_consumed
    cost = fuel_consumed * fuel_price

    print(f"\nВідстань: {distance} км")
    print(f"Спожите палне: {fuel_consumed} л")
    print(f"Витрата палива: {economy:.2f} км/л")
    print(f"Вартість палива: {cost:.2f} грн")

    cost_per_100km = (fuel_consumed / distance) * 100 * fuel_price
    print(f"Вартість на 100 км: {cost_per_100km:.2f} грн")

    if economy > 10:
        efficiency = "Відмінна"
    elif economy > 8:
        efficiency = "Добра"
    elif economy > 6:
        efficiency = "Задовільна"
    else:
        efficiency = "Погана"

    print(f"Оцінка ефективності: {efficiency}")

calculate_fuel_economy()