import json

def write_json(jsonfile, score_dict):
	with open(jsonfile, 'w+', encoding = 'utf-8') as f:
		f.write(json.dumps(score_dict, ensure_ascii = False, indent = 2))


s_dict = {1:1000, 2:2000}

write_json('test.json', s_dict)