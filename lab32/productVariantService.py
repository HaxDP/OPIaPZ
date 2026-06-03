from dataclasses import dataclass


@dataclass
class orderResult:
    variant: str
    basePrice: float
    discount: float
    delivery: float
    total: float


def validateOrder(price, quantity, variant):
    if price <= 0:
        raise ValueError("ціна має бути більшою за 0")

    if quantity <= 0:
        raise ValueError("кількість має бути більшою за 0")

    if variant not in ("basic", "standard", "premium"):
        raise ValueError("невідомий варіант продукту")


def getDiscountPercent(variant, quantity):
    if variant == "basic":
        if quantity >= 10:
            return 5
        return 0

    if variant == "standard":
        if quantity >= 10:
            return 10
        return 5

    if quantity >= 10:
        return 15
    return 10


def getDeliveryPrice(variant):
    if variant == "premium":
        return 0

    if variant == "standard":
        return 50

    return 80


def calculateOrder(price, quantity, variant):
    validateOrder(price, quantity, variant)

    basePrice = price * quantity
    discountPercent = getDiscountPercent(variant, quantity)
    discount = basePrice * discountPercent / 100
    delivery = getDeliveryPrice(variant)
    total = basePrice - discount + delivery

    return orderResult(
        variant,
        round(basePrice, 2),
        round(discount, 2),
        round(delivery, 2),
        round(total, 2),
    )


def compareVariants(price, quantity):
    variants = ["basic", "standard", "premium"]
    results = []

    for variant in variants:
        results.append(calculateOrder(price, quantity, variant))

    return sorted(results, key=lambda item: item.total)