from dataclasses import dataclass


@dataclass
class ticketPrice:
    passengerType: str
    distance: float
    price: float


def validateTicketData(distance, passengerType):
    if distance <= 0:
        raise ValueError("відстань має бути більшою за 0")

    if passengerType not in ("child", "student", "adult", "pensioner"):
        raise ValueError("невідомий тип пасажира")


def getPassengerDiscount(passengerType):
    if passengerType == "child":
        return 50

    if passengerType == "student":
        return 30

    if passengerType == "pensioner":
        return 40

    return 0


def calculateTicketPrice(distance, passengerType):
    validateTicketData(distance, passengerType)

    pricePerKilometer = 2.5
    minimumPrice = 20
    basePrice = distance * pricePerKilometer

    if basePrice < minimumPrice:
        basePrice = minimumPrice

    discount = getPassengerDiscount(passengerType)
    finalPrice = basePrice - basePrice * discount / 100

    return ticketPrice(passengerType, round(distance, 2), round(finalPrice, 2))


def validateProgramResults(testData):
    results = []

    for distance, passengerType, expectedPrice in testData:
        actualPrice = calculateTicketPrice(distance, passengerType).price
        results.append(actualPrice == expectedPrice)

    return all(results)