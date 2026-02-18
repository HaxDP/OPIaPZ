from singletonService import PhysicsService # тут сам імпорт з стореного мною файлика зі всіма функціями, щоб чистіше виглядав основний файл

def main():
    first_client = PhysicsService()
    second_client = PhysicsService()

    print("один об'єкт:", first_client is second_client) # тут виводиться чи це один і той же об'єкт
    print("прискорення вільного падіння:", first_client.get_gravity())

    mass = 10
    print("сила тяжіння для 10 кг:", first_client.weight_force(mass), "Н")

    time_seconds = 3
    print("відстань вільного падіння за 3 с:", second_client.free_fall_distance(time_seconds), "м")

    second_client.set_gravity(1.62)
    print("прискорення змінено на:", first_client.get_gravity())
    print("сила тяжіння для 10 кг на Місяці:", first_client.weight_force(mass), "Н")

    print("загальна кількість обчислень:", first_client.get_calculation_count())


if __name__ == "__main__":
    main()