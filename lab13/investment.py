def calculate_investment_return():
    print("Калькулятор прибутку від інвестицій")
    principal = float(input("Введіть первісну суму (грн): "))
    annual_rate = float(input("Введіть річну процентну ставку (%): "))
    years = int(input("Введіть період інвестування (років): "))
    compounding = input("Тип нарахування (simple/compound/monthly): ").lower()

    if principal <= 0 or annual_rate < 0 or years <= 0:
        print("Помилка: невірні вхідні дані")
        return

    rate_decimal = annual_rate / 100

    if compounding == "simple":
        final_amount = principal * (1 + rate_decimal * years)
    elif compounding == "compound":
        final_amount = principal * (1 + rate_decimal) ** years
    elif compounding == "monthly":
        final_amount = principal * (1 + rate_decimal / 12) ** (years * 12)
    else:
        print("Невідомий тип нарахування")
        return

    profit = final_amount - principal
    profit_percentage = (profit / principal) * 100

    print(f"\nПервісна сума: {principal:.2f} грн")
    print(f"Річна ставка: {annual_rate}%")
    print(f"Період: {years} років")
    print(f"Тип нарахування: {compounding}")
    print(f"Кінцева сума: {final_amount:.2f} грн")
    print(f"Прибуток: {profit:.2f} грн")
    print(f"Відсоток прибутку: {profit_percentage:.2f}%")

    if profit_percentage > 100:
        print("Очікується значний прибуток!")
    elif profit_percentage > 50:
        print("Хороший прибуток")

calculate_investment_return()