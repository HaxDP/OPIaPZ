def calculate_salary():
    print("Калькулятор заробітної плати")
    gross_salary = float(input("Введіть валову заробітну плату: "))
    years_experience = int(input("Введіть кількість років досвіду: "))

    tax_rate = 0.18
    military_tax = 1.5

    if years_experience >= 10:
        bonus = gross_salary * 0.20
    elif years_experience >= 5:
        bonus = gross_salary * 0.10
    else:
        bonus = 0

    salary_with_bonus = gross_salary + bonus
    tax_amount = salary_with_bonus * (tax_rate + military_tax / 100)
    net_salary = salary_with_bonus - tax_amount

    print(f"\nВалова заробітна плата: {gross_salary:.2f} грн")
    print(f"Бонус: {bonus:.2f} грн")
    print(f"Податки: {tax_amount:.2f} грн")
    print(f"Чиста заробітна плата: {net_salary:.2f} грн")

    if net_salary > 50000:
        print("Високий дохід")
    elif net_salary > 20000:
        print("Середній дохід")
    else:
        print("Низький дохід")

calculate_salary()