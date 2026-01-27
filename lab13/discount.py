def calculate_discount():
    print("Калькулятор знижки")
    original_price = float(input("Введіть первісну ціну: "))
    quantity = int(input("Введіть кількість товару: "))
    customer_type = input("Тип покупця (regular/vip/student): ").lower()

    if original_price <= 0 or quantity <= 0:
        print("Помилка: ціна та кількість повинні бути позитивними")
        return

    base_discount = 0

    if customer_type == "vip":
        base_discount = 0.20
    elif customer_type == "student":
        base_discount = 0.15
    elif customer_type == "regular":
        base_discount = 0.05
    else:
        print("Невідомий тип покупця")
        return

    quantity_discount = 0
    if quantity > 100:
        quantity_discount = 0.10
    elif quantity > 50:
        quantity_discount = 0.05

    total_discount = min(base_discount + quantity_discount, 0.30)
    subtotal = original_price * quantity
    discount_amount = subtotal * total_discount
    final_price = subtotal - discount_amount

    print(f"\nПервісна ціна за одиницю: {original_price:.2f} грн")
    print(f"Кількість: {quantity}")
    print(f"Сума без знижки: {subtotal:.2f} грн")
    print(f"Знижка: {total_discount * 100:.1f}% ({discount_amount:.2f} грн)")
    print(f"Кінцева ціна: {final_price:.2f} грн")

calculate_discount()