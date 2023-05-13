import sys
from bombcryptobot import *

if len(sys.argv) < 2:
	print("ERROR, no profile name sent, usage: python3 start.py PROFILE_NAME")
	exit()

details_dict = None
try:
	with open('./config.json') as json_file:
		tmp = json.load(json_file)
	
	if sys.argv[1] not in tmp['profiles']:
		print(f"The profile '{sys.argv[1]}' is not configured.")
		exit()

	details_dict = {
		"lang": tmp["lang"],
		"key": tmp["key"],
		"wait_loading": tmp["wait_loading"],
		"debug": tmp["debug"],
		"showDisplay": tmp["showDisplay"],
		"instance_name": sys.argv[1]
	}

	for key, val in tmp['profiles'][sys.argv[1]].items():
		details_dict[key] = val
except:
	print("Configuration file load error. Check your config.cfg")
	exit()

BombCryptoBot(details_dict)