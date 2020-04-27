#!/usr/bin/env python

import subprocess
from colorama import Fore, Back, Style
import optparse
import re


def data_parse():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC Address")
    parser.add_option("-m","--new_mac",dest="new_mac",help="New MAC Address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify the interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] please specify the new MAC Address, use --help for more info")
    else:
        return options
    

def mac_changer(interface,new_mac):
    subprocess.call(["ifconfig",interface,"down"])
    print(Fore.BLUE+"[+]"+Style.RESET_ALL+" Changed "+interface+" status to DOWN")
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    print("[+] setting New MAC Address to "+interface)
    subprocess.call(["ifconfig",interface,"up"])
    print("[+] changed "+interface+" status to UP")
    
    
def current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    check = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)
    if check:
        return check.group(0)
    else:
        print("[-] Could Not Read MAC Address")

options = data_parse()
current_macs = current_mac(options.interface)
print("[+] Current Mac is "+ str(current_macs))
mac_changer(options.interface,options.new_mac)

current_mac = current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] New Mac Address For "+options.interface+" is "+Fore.GREEN +options.new_mac+Style.RESET_ALL)
else:
    print("[-] Error While Changing MAC Address.")


exit()