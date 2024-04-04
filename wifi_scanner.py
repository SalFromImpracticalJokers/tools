## call function which then creates new thread of itself when os command is onde. this no longer requires thread handling and checking for activity

import os
import time
import sys
import threading
import keyboard

try:
        specified_ssids = False
        specified_fr = "."
        arguments = [i.strip().lower() for i in sys.argv]
        if "-s" in arguments: specified_ssids = arguments[arguments.index("-s")+1:]
        if "-f" in arguments: specified_fr = arguments[arguments.index("-f")+1].strip()
        if "-h" in arguments or "--help" in arguments:
                print("""\nHELP INFO FOR NETWORK SIGNAL SCANNER:

USE THIS TOOL TO MONITER THE STRENGTH AND FREQUENCIES OF WIFI IN THE LOCAL AREA
REPLACE 'wlo1' WITH THE CORRECT WIRELESS INTERFACE CHIP ON YOUR SYSTEM
USE 'ctrl + c' TO EXIT PROGRAM
PRESS 'space' TO PAUSE DISPLAY REQUIRES KEYBOARD AS SUDO

FLAGS:
RUN WITH NO FLAGS TO SCAN FOR ANY NETWORK SSID AT ANY FREQUENCY
USE '-f' FOLLOWED BY A SINGULAR FREQUENCY TO SEARCH FOR THAT SPECIFIC FREQUENCY
USE '-s' FOLLOWED BY ANY NUMBER OF SSIDS SEPERATED BY SPACES TO SEARCH FOR THOSE SSIDS
USE '-h' OR '--help' TO DISPLAY THIS HELP MESSAGE

NOTE - SSIDS ARE LISTED FROM HIGHEST SIGNAL STRENGTH TO LOWEST
""")
                exit()
except Exception as e:
        print(e)
        exit()

ssid_longest = 0
fr_longest = 0
sorted_wifi_info = {}
pause = False

def run():
        time.sleep(0.2)
        global ssid_longest
        global fr_longest
        global sorted_wifi_info
        global pause
        try:
                result = os.popen("""sudo iwlist wlo1 scanning | grep -E 'ESSID|Frequency|Signal level|Quality'""").read()
                thread_new = threading.Thread(target=run)
                thread_new.start()
                if not pause:
                        result = ("#~#".join([i.strip() for i in result.split("\n")])).split("Frequency")
                        result.pop(0)
                        returns = []
                        for i in result:
                                net = ("Frequency" + i).split("#~#")[:len(("Frequency" + i).split("#~#"))-1]
                                double = net[1]
                                double = double.split(" ")
                                net.pop(1)
                                net.insert(1, double[0])
                                net.insert(2, " ".join(double[2:]))
                                add = False
                                if specified_ssids:
                                        for ssid in specified_ssids:
                                                if (ssid.lower().strip() == net[-1].lower().strip().split(":")[-1] or ssid.lower() == net[-1].lower().strip().split(":")[-1][1:][:-1]) and specified_fr in net[0].split(":")[1].split(" ")[0].strip():
                                                        add = True
                                                        break
                                else:
                                        if specified_fr in net[0].split(":")[1].split(" ")[0].strip(): add = True
                                if add: returns.append(net)
                        networks = {}
                        for i in returns:
                                frequency = i[0].split(":")[1].strip()
                                quality = i[1].split("=")[1].strip()
                                signal = i[2].split("=")[1].strip()
                                ssid = i[3].split(":")[1].strip()
                                if '\\x00' in ssid or ssid == '""': ssid = "Unknown"
                                if ssid not in networks.keys(): networks[ssid] = [signal, frequency, quality]
                                else:
                                        count = 0
                                        for j in networks.keys():
                                                if ssid in j: count += 1
                                        new_ssid = ssid + " (" + str(count+1) + ")"
                                        networks[new_ssid] = [signal, frequency, quality]
                                
                        sorted_wifi_info = sorted(networks.items(), key=lambda x: int(x[1][0].split()[0]), reverse=True)
                        for ssid, info in sorted_wifi_info:
                                if len(ssid) > ssid_longest: ssid_longest = len(ssid)
                                if len(info[1]) > fr_longest: fr_longest = len(info[1])
        except:
                print("")
                os._exit(1)

def pause_func():
        try:
                global pause
                while True:
                        time.sleep(0.1)
                        keyboard.wait("space")
                        pause = not pause
        except:
                pass

thread_one = threading.Thread(target=run)
thread_one.start()

pause_thread = threading.Thread(target=pause_func)
pause_thread.start()

while 1:
        try:
                os.system("clear")
                print(f"\n| WIFI SSID:".ljust(ssid_longest+12) + f"| SIGNAL STRENGTH:".ljust(31) + f"| FREQUENCY:".ljust(fr_longest+18) + f"| QUALITY:")
                print("".join(["-" for i in range(len(f"| WIFI SSID:".ljust(ssid_longest+11) + f"| SIGNAL STRENGTH:".ljust(31) + f"| FREQUENCY:".ljust(fr_longest+18) + f"| QUALITY:")+6)]))
                statement = ""
                for ssid, info in sorted_wifi_info:
                        signal_strength, frequency, quality = info
                        statement = statement + (f"| SSID= {ssid}".ljust(ssid_longest+11) + f"| Signal strength= {signal_strength}".ljust(31) + f"| Frequency= {frequency}".ljust(fr_longest+18) + f"| Quality= {quality}") + "\n"
                print(statement)
                if pause: print("\n | PAUSED | \n")
                time.sleep(0.2)
        except:
                print("")
                os._exit(1)
