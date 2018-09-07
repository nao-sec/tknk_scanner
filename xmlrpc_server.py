#!/usr/bin/env python3

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from ctypes import *
import sys, time, json, ctypes.wintypes, os, subprocess
from pathlib import Path

def download_file():
     with open("dump.zip", "rb") as handle:
        return xmlrpc.client.Binary(handle.read())


def upload_file(arg, filename):
    print ("upload... " + filename)
    with open(filename, "wb") as handle:
        handle.write(arg.data)
        return True

def dump():
    os.mkdir("dump")

    with open('config.json', 'r') as outfile:
        config = json.load(outfile)

    if config["mode"] == "diff":
        Psapi = ctypes.WinDLL('Psapi.dll')
        EnumProcesses = Psapi.EnumProcesses
        EnumProcesses.restype = ctypes.wintypes.BOOL

        ProcessIds = (ctypes.wintypes.DWORD*512)()
        cb = ctypes.sizeof(ProcessIds)
        BytesReturned = ctypes.wintypes.DWORD()

        EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned))
        src_set = set(ProcessIds)

    subprocess.call(['cmd.exe', "/c", "start", config['target_file']])
    subprocess.call(['cmd.exe', "/c", "start", 'mouse_emu.exe'])

    print(("wait for unpack %d seconds\n") % config["time"])
        
    time.sleep(config["time"])

    print("dumping\n")

    if config["mode"] == "procdump":
        subprocess.call(["pssuspend.exe", config["target_file"], "/AcceptEula"])
        subprocess.call(["procdump.exe", "-ma", config["target_file"], "/AcceptEula"],cwd="dump")

    elif config["mode"] == "hollows_hunter":
        subprocess.call(["pssuspend.exe", config["target_file"], "/AcceptEula"])
        subprocess.call(["hollows_hunter.exe"],cwd="dump")

    elif config["mode"] == "diff":
        EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned))
        tag_set = set(ProcessIds)

        diff_ProcessIds = list(src_set ^ tag_set)

        new_ProcessIds = []

        for pid in diff_ProcessIds:
            try:
                proc_state = subprocess.check_output(["pssuspend.exe", str(pid), "/AcceptEula"])
                if "suspended." in str(proc_state):
                    new_ProcessIds.append(pid)
            except subprocess.CalledProcessError:
                pass
        for pid in new_ProcessIds:
            subprocess.call(["procdump.exe", "-ma", str(pid), "/AcceptEula"],cwd="dump")

    print("make zip\n")
    subprocess.call(['powershell', "compress-archive", "-Force", "dump", "dump.zip"])

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', 8000), allow_none=True)
    print ("Listening on port 8000...")
    server.register_function(download_file, 'download_file')
    server.register_function(upload_file, 'upload_file')
    server.register_function(dump, 'dump')
    server.serve_forever()
