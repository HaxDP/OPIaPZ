def calculate_electricity_bill():
    print("Розрахунок квитанції за електроенергію")
    kwh_used = float(input("Введіть спожиту електроенергію (кВт·год): "))
    household_type = input("Тип господарства (residential/commercial/industrial): ").lower()

    if kwh_used < 0:
        print("Помилка: споживання не може бути негативним")
        return

    if household_type == "residential":
        if kwh_used <= 100:
            rate = 1.68
        elif kwh_used <= 200:
            rate = 2.50
        else:
            rate = 3.50
    elif household_type == "commercial":
        if kwh_used <= 500:
            rate = 2.20
        else:
            rate = 3.00
    elif household_type == "industrial":
        rate = 2.50
    else:
        print("Невідомий тип господарства")
        return

    base_cost = kwh_used * rate

    if household_type == "residential":
        tax = base_cost * 0.15
    elif household_type == "commercial":
        tax = base_cost * 0.20
    else:
        tax = base_cost * 0.10

    total_cost = base_cost + tax

    print(f"\nСпоживання: {kwh_used} кВт·год")
    print(f"Тариф: {rate} грн/кВт·год")
    print(f"Вартість електроенергії: {base_cost:.2f} грн")
    print(f"Податок: {tax:.2f} грн")
    print(f"Загальна вартість: {total_cost:.2f} грн")

calculate_electricity_bill()