"""import json

with open("./json_files/calcinfos.json", "r") as f:
    content = f.read().strip()
    content_decoded = json.loads(content)
    operationsHistory = []
    for i in content_decoded:
        operationsHistory.append(i['Operation'])
    print(operationsHistory)"""

a = lambda a,b: (f"{a} ** {b} = {a ** b}")
dict = {
    "+": "plus",
    "-": "subtraction"
}
operations = (" ".join([str(f',{i}') for i in dict]))
print(operations)
print(f"operation available is: {operations}")