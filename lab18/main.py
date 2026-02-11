# - Напишіть програму, яка виконує обробку виключень у завданні, пов’язаному з обробкою
# користувацького вводу (наприклад, калькулятор).
# - Додайте власний клас виключення, який буде використовуватися у вашій програмі.
# - Підготуйте коротку презентацію про ваш підхід до обробки виключень, пояснюючи вибір
# використовуваних інструментів та підходів.

# 15. Напиши функцію, яка повертає None, якщо сталася помилка перетворення (ValueError).

class invalidOperationError(Exception):
    pass

def convertToFloat(value): # зробив для 15 варіанту тут функцію, яка повертає None, якщо сталася помилка перетворення
    try:
        return float(value)
    except ValueError:
        return None
    
# ++++++++ добавив багато класів для того щоб дотримувався SOLID (для тренеровки дла ООП) ++++++++++

class operation:
    def execute(self, numberOne, numberTwo):
        raise NotImplementedError 

class addition(operation):
    def execute(self, numberOne, numberTwo):
        return numberOne + numberTwo
    
class substraction(operation):
    def execute(self, numberOne, numberTwo):
        return numberOne - numberTwo

class multiplication(operation):
    def execute(self, numberOne, numberTwo):
        return numberOne * numberTwo
    
class division(operation):
    def execute(self, numberOne, numberTwo):
        if numberTwo == 0:
            raise ZeroDivisionError("ділення на 0")
        return numberOne / numberTwo
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# реєстр операцій
operations = {
    '+': addition(),
    '-': substraction(),
    '*': multiplication(),
    '/': division()
}

class calculator:
    def __init__(self, operations):
        self.operations = operations

    def calculate(self, numberOne, numberTwo, operator):
        if operator not in self.operations:
            raise invalidOperationError(f"операція '{operator}' не підтримується")
        return self.operations[operator].execute(numberOne, numberTwo)
    
if __name__ == "__main__":
    calc = calculator(operations)
    
    print("=" * 50)
    print("калькулятор з обробкою виключень")
    print("=" * 50)
    print("введіть 'exit' для виходу")
    print("=" * 50)
    
    while True:
        try:
            firstInput = input("\nвведіть перше число (або 'exit'): ")
            if firstInput.lower() == 'exit':
                print("вихід з програми")
                break
            
            numberOne = convertToFloat(firstInput)
            if numberOne is None:
                print("помилка, неправильний формат першого числа")
                continue
            
            operator = input("введіть операцію: ")
            if operator.lower() == 'exit':
                print("вихід з програми")
                break
            
            secondInput = input("введіть друге число (або 'exit'): ")
            if secondInput.lower() == 'exit':
                print("вихід з програми")
                break
            
            numberTwo = convertToFloat(secondInput)
            if numberTwo is None:
                print("помилка, неправильний формат другого числа")
                continue
            
            result = calc.calculate(numberOne, numberTwo, operator)
            print(f"\nрезультат: {numberOne} {operator} {numberTwo} = {result}")
            
        except ZeroDivisionError as error:
            print(f"помилка ділення: {error}")
        except invalidOperationError as error:
            print(f"помилка операції: {error}")
        except Exception as error:
            print(f"несподівана помилка: {error}")
    