def calculate_car_loan():
    print("Калькулятор автокредиту")
    car_price = float(input("Введіть ціну автомобіля: "))
    down_payment = float(input("Введіть первинний внесок: "))
    annual_rate = float(input("Введіть річну процентну ставку (%): "))
    loan_term = int(input("Введіть термін кредиту (років): "))

    if car_price <= 0 or down_payment < 0 or annual_rate < 0 or loan_term <= 0:
        print("Помилка: невірні вхідні дані")
        return

    if down_payment > car_price:
        print("Помилка: первинний внесок не може перевищувати ціну автомобіля")
        return

    loan_amount = car_price - down_payment
    monthly_rate = annual_rate / 100 / 12
    months = loan_term * 12

    if monthly_rate == 0:
        monthly_payment = loan_amount / months
    else:
        monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

    total_paid = monthly_payment * months
    total_interest = total_paid - loan_amount

    print(f"\nЦіна автомобіля: {car_price:.2f} грн")
    print(f"Первинний внесок: {down_payment:.2f} грн")
    print(f"Сума кредиту: {loan_amount:.2f} грн")
    print(f"Щомісячний платіж: {monthly_payment:.2f} грн")
    print(f"Загальна сума виплат: {total_paid:.2f} грн")
    print(f"Загальні відсотки: {total_interest:.2f} грн")

    if total_interest > loan_amount * 0.5:
        print("Вартість кредиту висока")
    else:
        print("Вартість кредиту прийнятна")

calculate_car_loan()