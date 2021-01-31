import json


#
file = open("names.txt", "r")
persons = file.readlines()
for i in range(len(persons)):
    persons[i] = persons[i].strip("\n")
    print(persons[i])
file.close()

data = {}


def make():
    with open("names.json", "w") as f:
        data['names'] = persons
        json.dump(data, f, indent=4)
        for i in persons:
            print("added {0} to names".format(i))


def edit():
    with open("names.json", "r") as f:
        data = json.load(f)
    with open("names.json", "w") as f:
        for i in data['names']:
            i.replace("\\n", "")
        json.dump(data, f, indent=4)

make()
