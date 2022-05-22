from datetime import datetime
import json

def save_record(gen, action, params, usr_name, usr_id):
	with open('data/history.json', 'r') as file:
		data = json.load(file)
	history = data[gen]
	history.append(
		{
			'date': datetime.now().strftime('%Y-%m-%d'), 
			'name': usr_name, 
			'action': action,
			'params': params,
			'user': { 'id': usr_id, 'name': usr_name }
		}
	)

	with open('data/history.json', 'w') as output:
		json.dump(data, output, indent=2)
	
def get_history(gen):
	with open('data/history.json', 'r') as file:
		data = json.load(file)
	
	history = data[gen]
	history = history[-7:]
	
	output = []
	for record in history:
		output.append(
			f"{record['action']} << {record['user']['name']}"
		)
	
	return output
