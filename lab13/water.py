def calculate_water_bill():
    print("Розрахунок квитанції за водопостачання")
    cubic_meters = float(input("Введіть спожиту воду (м³): "))
    has_sewage = input("Чи є каналізація? (yes/no): ").lower()

    if cubic_meters < 0:
        print("Помилка: споживання не може бути негативним")
        return

    if cubic_meters <= 10:
        water_rate = 20
    elif cubic_meters <= 30:
        water_rate = 25
    else:
        water_rate = 30

    water_cost = cubic_meters * water_rate

    if has_sewage == "yes":
        sewage_cost = cubic_meters * 18
        maintenance = 100
    elif has_sewage == "no":
        sewage_cost = 0
        maintenance = 50
    else:
        print("Невірна відповідь")
        return

    subtotal = water_cost + sewage_cost + maintenance

    if subtotal > 1000:
        discount = subtotal * 0.05
    else:
        discount = 0

    total_cost = subtotal - discount

    print(f"\nСпоживання води: {cubic_meters} м³")
    print(f"Вартість води: {water_cost:.2f} грн")
    print(f"Вартість каналізації: {sewage_cost:.2f} грн")
    print(f"Обслуговування: {maintenance:.2f} грн")
    print(f"Знижка: {discount:.2f} грн")
    print(f"Загальна вартість: {total_cost:.2f} грн")

calculate_water_bill()