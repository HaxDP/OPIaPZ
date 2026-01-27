def convert_temperature():
    print("Конвертер температури")
    temperature = float(input("Введіть температуру: "))
    scale = input("Введіть шкалу (C/F/K): ").upper()

    if scale == "C":
        fahrenheit = (temperature * 9/5) + 32
        kelvin = temperature + 273.15
        print(f"\n{temperature}°C = {fahrenheit:.2f}°F")
        print(f"{temperature}°C = {kelvin:.2f}K")
        
        if temperature < 0:
            print("Дуже холодно!")
        elif temperature < 15:
            print("Холодно")
        elif temperature < 25:
            print("Комфортно")
        else:
            print("Гарячо")
            
    elif scale == "F":
        celsius = (temperature - 32) * 5/9
        kelvin = celsius + 273.15
        print(f"\n{temperature}°F = {celsius:.2f}°C")
        print(f"{temperature}°F = {kelvin:.2f}K")
        
    elif scale == "K":
        celsius = temperature - 273.15
        fahrenheit = (celsius * 9/5) + 32
        print(f"\n{temperature}K = {celsius:.2f}°C")
        print(f"{temperature}K = {fahrenheit:.2f}°F")
    else:
        print("Невідома шкала температури")

convert_temperature()