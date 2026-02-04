def add_task(tasks, name, hours):
    tasks.append((name, hours))

def total_hours(tasks):
    total = 0
    for t in tasks:
        total += t[1]
    return total

def average_hours(tasks):
    if len(tasks) == 0:
        return 0
    return total_hours(tasks) / len(tasks)

def longest_task(tasks):
    if len(tasks) == 0:
        return None
    longest = tasks[0]
    i = 1
    while i < len(tasks):
        if tasks[i][1] > longest[1]:
            longest = tasks[i]
        i += 1
    return longest

def menu():
    tasks = []
    while True:
        print("1 add task")
        print("2 show all")
        print("3 statistics")
        print("4 exit")
        choice = input("choice: ")

        if choice == "1":
            name = input("task name: ")
            hours = float(input("hours: "))
            add_task(tasks, name, hours)
        elif choice == "2":
            for t in tasks:
                print(t[0], "-", t[1], "hours")
        elif choice == "3":
            print("total hours:", total_hours(tasks))
            print("average hours:", average_hours(tasks))
            lt = longest_task(tasks)
            if lt != None:
                print("longest task:", lt[0], lt[1])
        elif choice == "4":
            break

menu()