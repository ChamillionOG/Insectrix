import json
import os

save_file = "data.json"

def load_data():
    if not os.path.exists(save_file):
        print("Save File Not Found! Creating New Save!")
        return create_new_save()
    
    with open(save_file, "r") as file:
        return json.load(file)
    
def save_data(data):
    with open(save_file, "w") as file:
        json.dump(data, file, indent=4)

def create_new_save():
    data = {
        "bugs": 0,
        "max_bugs": 3,
        "bugnet": "basic",
        "enviroment": "forest",
        
        "container": {
            "type": "small_jar",
            "capacity": 10,
            "offset": 15,
            "bugs": []
        }
    }

    print("New Save File Created!")
    save_data(data)
    return data