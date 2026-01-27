def calculate_grade():
    print("Калькулятор оцінок студента")
    subject = input("Назва предмету: ")
    exam_score = float(input("Оцінка за іспит (0-100): "))
    homework_score = float(input("Оцінка за домашнє завдання (0-100): "))
    participation = float(input("Оцінка за участь (0-100): "))

    if exam_score < 0 or exam_score > 100 or homework_score < 0 or homework_score > 100:
        print("Помилка: оцінки повинні бути від 0 до 100")
        return

    final_score = (exam_score * 0.4) + (homework_score * 0.35) + (participation * 0.25)

    print(f"\n{subject}")
    print(f"Іспит: {exam_score}")
    print(f"Домашнє завдання: {homework_score}")
    print(f"Участь: {participation}")
    print(f"Фінальна оцінка: {final_score:.2f}")

    if final_score >= 90:
        grade = "A (Відмінно)"
    elif final_score >= 80:
        grade = "B (Добре)"
    elif final_score >= 70:
        grade = "C (Задовільно)"
    elif final_score >= 60:
        grade = "D (Прийнято)"
    else:
        grade = "F (Не прийнято)"

    print(f"Оцінка: {grade}")

calculate_grade()