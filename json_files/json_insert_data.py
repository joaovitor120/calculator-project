import json

def AddToJson(data, file):
    array1 = []
    with open(file, "r") as f:
        content = f.read().strip()
    if content:
        content_decoded = json.loads(content) #json  str format into python object
        for i in content_decoded:
            array1.append(i)
        array1.append(data)
        json_data = json.dumps(array1, indent=4)
        with open(file, "w") as f:
            f.write(json_data)
    else:
        array1.append(data)
        json_data = json.dumps(array1, indent=4)
        with open(file, "w") as f:
            f.write(json_data)