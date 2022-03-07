import json

def fetch_token():
    with open('sensitive.json', 'r') as file:
        get = json.load(file)
    return get['token']

def fetch_groups_IDs():
    with open('sensitive.json', 'r') as file:
        data = json.load(file)
    return data['groupsIDs']

def id_in_groups_IDs(chat_id):
    chat_id = str(chat_id)
    data = fetch_groups_IDs()
    for i in range(len(data)):
        if chat_id == data[i][1]:
            return True
    return False

def get_generation(chat_id):
    data = fetch_groups_IDs()
    chat_id = str(chat_id)
    for i in range(len(data)):
        if chat_id == data[i][1]:
            return data[i][0]
    return None

def get_certs_data():
    with open('data/certs.json', 'r') as file:
        data = json.load(file)
    return data

# Develop fetch quotes for get() 
