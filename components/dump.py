import json
from components.fetch import *

def pretty_dump(data):
    with open('data/certs.json', 'w') as file:
        file.write("{\n")
        for gen in data.keys():
            file.write(f"\t\"{str(gen)}\":" + " {\n")

            file.write("\t\t\"subjects\": [\n")
            for subject in data[gen]['subjects']:
                if subject == data[gen]['subjects'][-1]:
                    file.write(f'\t\t\t"{subject}"\n')
                else:
                    file.write(f'\t\t\t"{subject}",\n')

            file.write("\t\t],\n")

            file.write("\t\t\"certs\": [\n")
            for cert in data[gen]['certs']:
                if cert != data[gen]['certs'][-1]:
                    cert = json.dumps(cert, ensure_ascii=False)
                    file.write(f"\t\t\t{cert},\n")
                else:
                    cert = json.dumps(cert, ensure_ascii=False)
                    file.write(f"\t\t\t{cert}\n")

            file.write("\t\t]\n")
            if gen == "testing": file.write("\t}\n")
            else: file.write("\t},\n")
        file.write("}")
