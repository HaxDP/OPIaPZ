def add_student(students, name, grades):
    students.append((name, grades))

def student_average(grades):
    total = 0
    for g in grades:
        total += g
    return total / len(grades)

def group_average(students):
    total = 0
    for s in students:
        total += student_average(s[1])
    return total / len(students)

def best_student(students):
    best = students[0]
    i = 1
    while i < len(students):
        if student_average(students[i][1]) > student_average(best[1]):
            best = students[i]
        i += 1
    return best

students = []
num_students = int(input("how many students? "))
for i in range(num_students):
    name = input("name: ")
    grades = list(map(int, input("grades: ").split()))
    add_student(students, name, grades)

print("students:", students)

for s in students:
    print(s[0], "average:", student_average(s[1]))

print("group average:", group_average(students))

bs = best_student(students)
print("best student:", bs[0], "with average:", student_average(bs[1]))