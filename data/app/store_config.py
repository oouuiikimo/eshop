"""Flask config class."""
import os
import json
from collections import namedtuple
from json import JSONEncoder
import os
script_dir = os.path.dirname(os.path.realpath('__file__')) #<-- absolute dir the script is in
rel_path = "config/store.json"
abs_file_path = os.path.join(script_dir, rel_path)
#print(abs_file_path)
def customStoreDecoder(storeDict):
    return namedtuple('X', storeDict.keys())(*storeDict.values())

def store_config():
    data = None
    #Assume you received this JSON response
    with open(abs_file_path) as json_file:
        return json.load(json_file, object_hook=customStoreDecoder)
     
# Parse JSON into an object with attributes corresponding to dict keys.
#store = json.loads(data, object_hook=customStoreDecoder)

if __name__ == "__main__":
    data = store_config()
    print("After Converting JSON Data into Custom Python Object")
    print(data.NAME)
    data.NAME = 'FUCK'


    



