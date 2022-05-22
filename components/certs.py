from datetime import datetime
import json 
#
from components.dump import pretty_dump

def cert_check(new_cert, gen):
    with open('data/certs.json') as file:
        data = json.load(file)
    
    if new_cert in data[gen]['certs']:
        return True
    else:
        return False

def cert_adder(new_cert, gen):
    with open('data/certs.json') as file:
        data = json.load(file)
    
    data[gen]['certs'].append(new_cert)
    pretty_dump(data)
    return True

def cert_remover(chosen_cert, gen):
    with open('data/certs.json') as file:
        data = json.load(file)
    
    for cert in data[gen]['certs']:
        fcert = f"[{cert['type']}] {cert['name']} {cert['date']}"
        if fcert == chosen_cert:
            data[gen]['certs'].remove(cert)
            break

    pretty_dump(data)

    return True

def getSubjects(gen):
    with open('data/certs.json') as file:
        data = json.load(file)
    
    subjects = [subject for subject in data[gen]['subjects']]
    return subjects

def getCerts(update, gen):
    with open('data/certs.json') as file:
        data = json.load(file)
    
    certs = [cert for cert in data[gen]['certs']]
    return certs

def getRemainingDays(subject):
    currentDate = datetime.now().strftime("%Y-%m-%d")
    subjectDate = subject['date']
    remainingDays = (datetime.strptime(subjectDate, "%Y-%m-%d") - datetime.strptime(currentDate, "%Y-%m-%d")).days

    return remainingDays
