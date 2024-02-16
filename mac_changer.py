#!/usr/bin/env python
import random
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for which to change the MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    parser.add_option("-r", "--rmac", action="store_true", dest="should_generate_random_mac", help="Assign a random MAC address to the interface.")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not (options.new_mac or options.should_generate_random_mac):
        parser.error("[-] Please specify a new MAC address or use the randomize option, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode("utf-8")

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read the MAC address of the interface " + interface)


def generate_random_mac_address():
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0xff),
           random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ':'.join(map(lambda hexadecimal_digit: "%02x" % hexadecimal_digit, mac))

options = get_arguments()

new_mac = options.new_mac

if options.should_generate_random_mac:
    new_mac = generate_random_mac_address()
    print("Random MAC address = " + new_mac)

current_mac = get_current_mac(options.interface)

change_mac(options.interface, new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not change.")
