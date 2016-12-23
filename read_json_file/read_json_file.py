import json
f=''
with open('config.json','r') as fp:
	f=fp.read()
	print json.loads(f)
	for ca in json.loads(f):
		for cc in ca:
			print cc
