import os
import glob
import time

folders = glob.glob("./profiles/*")
for folder in folders:
	botName = folder[11:]
	print(f"Starting {botName}")
	cmd = f"screen -dm -S {botName} python3 starter.py {botName} &"
	os.system(cmd)
	time.sleep(10)
