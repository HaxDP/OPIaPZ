def addUser(users, name, hobbies):
    users[name] = set(hobbies)

def commonHobbies(users):
    names = list(users.keys())
    common = users[names[0]].copy()
    i = 1
    while i < len(names):
        common = common & users[names[i]]
        i += 1
    return common

def allHobbies(users):
    all_set = set()
    for h in users.values():
        all_set = all_set | h
    return all_set

def hobbyStats(users):
    stats = {}
    for hset in users.values():
        for h in hset:
            if h in stats:
                stats[h] += 1
            else:
                stats[h] = 1
    return stats

users = {}
while True:
    name = input("name: ")
    if name == "":
        break
    hobbies = input("hobbies: ").split()
    addUser(users, name, hobbies)

print("all users:", users)
print("common hobbies:", commonHobbies(users))
print("all hobbies:", allHobbies(users))
print("hobby stats:", hobbyStats(users))