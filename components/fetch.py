import json

def fetchToken():
    with open('data.json', 'r') as file:
        get = json.load(file)
    return get

# Develop fetch quotes for get() 
