def calculate_loan_payment():
    print("Калькулятор кредиту")
    loan_amount = float(input("Сума кредиту: "))
    annual_rate = float(input("Річна процентна ставка (%): "))
    term_years = int(input("Термін кредиту (років): "))

    monthly_rate = annual_rate / 100 / 12
    months = term_years * 12

    if monthly_rate == 0:
        monthly_payment = loan_amount / months
    else:
        monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

    total_payment = monthly_payment * months
    overpayment = total_payment - loan_amount

    print(f"\nЩомісячний платіж: {monthly_payment:.2f} грн")
    print(f"Загальна сума виплат: {total_payment:.2f} грн")
    print(f"Переплата: {overpayment:.2f} грн")

    if overpayment > loan_amount:
        print("Переплата більша за тіло кредиту")
    elif overpayment > loan_amount * 0.5:
        print("Переплата значна")
    else:
        print("Умови кредиту прийнятні")

calculate_loan_payment()