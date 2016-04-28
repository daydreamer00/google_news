import json
with open('temp.json', 'r') as f:
	for l in f:
		data = json.loads(l)
		if ("titleName" in l):
			print json.dumps(data,sort_keys=True,indent=3,separators=(',',': '))
