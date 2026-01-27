def calculate_shipping_cost():
    print("Калькулятор вартості доставки")
    weight = float(input("Введіть вагу посилки (кг): "))
    distance = float(input("Введіть відстань доставки (км): "))
    delivery_type = input("Тип доставки (standard/express/overnight): ").lower()

    if weight <= 0 or distance <= 0:
        print("Помилка: вага та відстань повинні бути позитивними")
        return

    base_rate = 50
    weight_cost = weight * 10
    distance_cost = distance * 0.5

    if delivery_type == "standard":
        multiplier = 1.0
    elif delivery_type == "express":
        multiplier = 1.5
    elif delivery_type == "overnight":
        multiplier = 2.0
    else:
        print("Невідомий тип доставки")
        return

    subtotal = (base_rate + weight_cost + distance_cost) * multiplier

    if subtotal > 1000:
        discount = subtotal * 0.10
    elif subtotal > 500:
        discount = subtotal * 0.05
    else:
        discount = 0

    total_cost = subtotal - discount

    print(f"\nВага: {weight} кг")
    print(f"Відстань: {distance} км")
    print(f"Тип доставки: {delivery_type}")
    print(f"Базова вартість: {base_rate:.2f} грн")
    print(f"Вартість за вагою: {weight_cost:.2f} грн")
    print(f"Вартість за відстанню: {distance_cost:.2f} грн")
    print(f"Знижка: {discount:.2f} грн")
    print(f"Загальна вартість: {total_cost:.2f} грн")

calculate_shipping_cost()