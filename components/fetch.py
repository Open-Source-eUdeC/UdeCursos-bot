import json

def fetchToken():
    with open('token.json', 'r') as file:
        get = json.load(file)
    return get

# Develop fetch quotes for get() 
