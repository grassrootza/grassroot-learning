import psutil
import time
import os


while True:
    time.sleep(600)
    keep = []
    all_proc = psutil.net_connections()
    for i in all_proc:
        keep.append(i[3])
    if ('127.0.0.1', 5000) not in keep:
        os.system('bash activate_me.sh')
    else:
    	print("All's well.")
