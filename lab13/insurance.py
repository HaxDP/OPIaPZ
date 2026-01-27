def calculate_insurance_premium():
    print("Калькулятор страхового внеску")
    coverage_amount = float(input("Введіть суму страховки: "))
    age = int(input("Введіть вік: "))
    health_status = input("Стан здоров'я (excellent/good/fair/poor): ").lower()
    smoker = input("Чи ви курите? (yes/no): ").lower()

    if coverage_amount <= 0 or age <= 0:
        print("Помилка: невірні вхідні дані")
        return

    base_rate = coverage_amount * 0.01

    if age < 25:
        age_multiplier = 1.3
    elif age < 40:
        age_multiplier = 1.0
    elif age < 60:
        age_multiplier = 1.2
    else:
        age_multiplier = 1.5

    if health_status == "excellent":
        health_multiplier = 0.8
    elif health_status == "good":
        health_multiplier = 1.0
    elif health_status == "fair":
        health_multiplier = 1.3
    elif health_status == "poor":
        health_multiplier = 1.6
    else:
        print("Невідомий стан здоров'я")
        return

    smoking_multiplier = 1.5 if smoker == "yes" else 1.0

    annual_premium = base_rate * age_multiplier * health_multiplier * smoking_multiplier

    print(f"\nСума страховки: {coverage_amount:.2f} грн")
    print(f"Вік: {age}")
    print(f"Стан здоров'я: {health_status}")
    print(f"Курець: {smoker}")
    print(f"Базова ставка: {base_rate:.2f} грн")
    print(f"Річний внесок: {annual_premium:.2f} грн")
    print(f"Місячний внесок: {annual_premium / 12:.2f} грн")

    if annual_premium > coverage_amount * 0.05:
        print("Внесок досить високий")

calculate_insurance_premium()