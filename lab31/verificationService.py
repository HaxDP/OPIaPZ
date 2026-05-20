from dataclasses import dataclass


@dataclass
class checkResult:
    name: str
    success: bool
    message: str


def calculateDiscount(price, percent):
    if price < 0:
        raise ValueError("ціна не може бути меншою за 0")
    if percent < 0 or percent > 100:
        raise ValueError("відсоток має бути від 0 до 100")

    discount = price * percent / 100
    return round(price - discount, 2)


def checkCodeStyle(codeText):
    results = []
    badCall = "ev" + "al("

    if badCall in codeText:
        results.append(checkResult("статичний аналіз", False, "знайдено небезпечний eval"))
    else:
        results.append(checkResult("статичний аналіз", True, "небезпечних викликів не знайдено"))

    if "\t" in codeText:
        results.append(checkResult("форматування", False, "у коді є табуляція"))
    else:
        results.append(checkResult("форматування", True, "табуляції немає"))

    return results


def runDynamicTests():
    tests = [
        ("знижка 10%", calculateDiscount(100, 10) == 90),
        ("знижка 0%", calculateDiscount(150, 0) == 150),
        ("знижка 100%", calculateDiscount(80, 100) == 0),
    ]

    results = []
    for name, success in tests:
        message = "тест пройдено" if success else "тест не пройдено"
        results.append(checkResult(name, success, message))
    return results


def buildReport(results):
    lines = ["звіт верифікації коду", "=" * 28]

    for result in results:
        status = "OK" if result.success else "ERROR"
        lines.append(f"{result.name}: {status} - {result.message}")

    successCount = sum(1 for result in results if result.success)
    lines.append(f"успішно: {successCount} з {len(results)}")
    return "\n".join(lines)