def check_exam_pass_fail():
    print("Визначення результату іспиту")
    student_name = input("Введіть ім'я студента: ")
    test1 = float(input("Оцінка за тест 1 (0-100): "))
    test2 = float(input("Оцінка за тест 2 (0-100): "))
    test3 = float(input("Оцінка за тест 3 (0-100): "))
    final_exam = float(input("Оцінка за фінальний іспит (0-100): "))

    all_scores = [test1, test2, test3, final_exam]

    if any(score < 0 or score > 100 for score in all_scores):
        print("Помилка: оцінки повинні бути від 0 до 100")
        return

    average = sum(all_scores) / len(all_scores)
    min_score = min(all_scores)
    max_score = max(all_scores)

    print(f"\nСтудент: {student_name}")
    print(f"Тест 1: {test1}")
    print(f"Тест 2: {test2}")
    print(f"Тест 3: {test3}")
    print(f"Фінальний іспит: {final_exam}")
    print(f"Середня оцінка: {average:.2f}")
    print(f"Мінімальна оцінка: {min_score}")
    print(f"Максимальна оцінка: {max_score}")

    if min_score < 50:
        status = "НЕ ПРОЙДЕНО (одна оцінка менша за 50)"
    elif average < 60:
        status = "НЕ ПРОЙДЕНО (середня менша за 60)"
    elif average < 70:
        status = "ПРОЙДЕНО (задовільно)"
    elif average < 85:
        status = "ПРОЙДЕНО (добре)"
    else:
        status = "ПРОЙДЕНО (відмінно)"

    print(f"Результат: {status}")

check_exam_pass_fail()