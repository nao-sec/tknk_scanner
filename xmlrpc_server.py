#!/usr/bin/env python3

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from ctypes import *
from ctypes.wintypes import *
import sys, time, json, ctypes.wintypes, os, subprocess, shutil
from pathlib import Path

#Microsoft types to ctypes for clarity
BYTE      = c_ubyte
WORD      = c_ushort
DWORD     = c_ulong
LPBYTE    = POINTER(c_ubyte)
LPTSTR    = POINTER(c_char) 
HANDLE    = c_void_p
PVOID     = c_void_p
LPVOID    = c_void_p
UINT_PTR  = c_ulong
LONG      = c_long
DWORD64   = c_uint64
PWCHAR    = c_wchar_p
DWORD_PTR = c_uint64
BOOL      = c_bool

# Constants
DEBUG_PROCESS         = 0x00000001
CREATE_NEW_CONSOLE    = 0x00000010

# Thread constants for CreateToolhelp32Snapshot()
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS  = 0x00000002
TH32CS_SNAPTHREAD   = 0x00000004
TH32CS_SNAPMODULE   = 0x00000008
TH32CS_INHERIT      = 0x80000000
TH32CS_SNAPALL      = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)
THREAD_ALL_ACCESS   = 0x001F03FF

kernel32 = windll.kernel32
advapi32 = windll.advapi32

# Structures for CreateProcessW() function
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb",            DWORD),        
        ("lpReserved",    LPTSTR), 
        ("lpDesktop",     LPTSTR),  
        ("lpTitle",       LPTSTR),
        ("dwX",           DWORD),
        ("dwY",           DWORD),
        ("dwXSize",       DWORD),
        ("dwYSize",       DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute",DWORD),
        ("dwFlags",       DWORD),
        ("wShowWindow",   WORD),
        ("cbReserved2",   WORD),
        ("lpReserved2",   LPBYTE),
        ("hStdInput",     HANDLE),
        ("hStdOutput",    HANDLE),
        ("hStdError",     HANDLE),
        ]

class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess",    HANDLE),
        ("hThread",     HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId",  DWORD),
        ]

class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize',             DWORD),
        ('cntUsage',           DWORD),
        ('th32ThreadID',       DWORD),
        ('th32OwnerProcessID', DWORD),
        ('tpBasePri',          LONG),
        ('tpDeltaPri',         LONG),
        ('dwFlags',            DWORD),
]

THREAD_SUSPEND_RESUME = 0x0002

class MODULEENTRY32(Structure):
    _fields_ = [( 'dwSize' , DWORD ) , 
                ( 'th32ModuleID' , DWORD ),
                ( 'th32ProcessID' , DWORD ),
                ( 'GlblcntUsage' , DWORD ),
                ( 'ProccntUsage' , DWORD ) ,
                ( 'modBaseAddr' , DWORD_PTR ) ,
                ( 'modBaseSize' , DWORD ) , 
                ( 'hModule' , HMODULE ) ,
                ( 'szModule' , c_char * 256 ),
                ( 'szExePath' , c_char * 260 ) ]

p = Path(sys.argv[0])
work_dir = p.parents[0]

################################################

def scylla_dump(pid, copy_file, entrypoint):
    hSnapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid)

    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)

    kernel32.Module32First(hSnapshot, byref(me32))
    print("[*] me32.modBaseAddr: " + hex(me32.modBaseAddr))

    scylla = windll.scylla
    ScyllaDumpProcessW = scylla.ScyllaDumpProcessW

    print("[*] AddressOfEntryPoint: " +  hex(entrypoint))
    out_file = str(work_dir.joinpath(str(pid)+"_dump.exe"))
    imagebase=me32.modBaseAddr

    # BOOL __stdcall ScyllaDumpProcessW(DWORD_PTR pid, const WCHAR * fileToDump, DWORD_PTR imagebase, DWORD_PTR entrypoint, const WCHAR * fileResult);
    ret = ScyllaDumpProcessW(
        DWORD_PTR(pid),
        PWCHAR(copy_file),
        DWORD_PTR(imagebase),
        DWORD_PTR(entrypoint),
        PWCHAR(out_file)
    )

    print(ret)

    if(ret != 1):
        print("Process does not exist.")
        return

    kernel32.TerminateProcess(pid)
    
    shutil.move(out_file, "dump/")
   
    return


def SuspendProcess(pid):
    hSnapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)

    te = THREADENTRY32()
    te.dwSize = sizeof(THREADENTRY32)
    ret = kernel32.Thread32First(hSnapshot,  byref(te))
    if ret == 0 :
        print ("[*] SuspendProcess Fail")
        kernel32.CloseHandle(hSnapshot)

    while ret :
        if te.th32OwnerProcessID == pid : 
            print ("[*] th32ThreadID=%d"% te.th32ThreadID )
            print ("[*] th32OwnerProcessID=%d"% te.th32OwnerProcessID)
            print("[*] --------------------------------")
            hThread = kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, te.th32ThreadID)
            r = kernel32.SuspendThread(hThread)
        ret = kernel32.Thread32Next( hSnapshot, byref(te) )
    
    return

def download_file():
     with open(str(work_dir.joinpath("dump.zip")), "rb") as handle:
        return xmlrpc.client.Binary(handle.read())


def upload_file(arg, filename):
    print ("upload... " + filename)
    
    with open(str(work_dir.joinpath(filename)), "wb") as handle:
        handle.write(arg.data)
        return True

def dump(config):
    subprocess.call(["powershell", "Get-ChildItem -File", "|", "Set-ItemProperty", "-name", "isReadOnly", "-Value", "$true"])
    os.mkdir(str(work_dir.joinpath("dump/")))
    print(config)

    subprocess.call(['cmd.exe', "/c", "start", "pythonw", "mouse_emu.pyw"])

    if config["mode"] == "diff":
        Psapi = ctypes.WinDLL('Psapi.dll')
        EnumProcesses = Psapi.EnumProcesses
        EnumProcesses.restype = ctypes.wintypes.BOOL

        ProcessIds = (ctypes.wintypes.DWORD*512)()
        cb = ctypes.sizeof(ProcessIds)
        BytesReturned = ctypes.wintypes.DWORD()

        EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned))
        src_set = set(ProcessIds)

    creation_flags = CREATE_NEW_CONSOLE 
    startupinfo         = STARTUPINFO()
    process_information = PROCESS_INFORMATION()
    startupinfo.dwFlags     = 0x1
    startupinfo.wShowWindow = 0x0
    startupinfo.cb = sizeof(startupinfo)
    
    if kernel32.CreateProcessW(str(work_dir.joinpath(config['target_file'])),
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):

        print ("[*] Launched the process!")
        print ("[*] The Process ID is: %d" % process_information.dwProcessId)
        PID = process_information.dwProcessId

        if config["mode"] == "procdump":
            cmd=["cmd", "/c", "start", "powershell", "-windowstyle", "hidden","Start-Sleep", str(config["time"]), ";", "taskkill", "/F", "/PID", str(PID), ";"]

            subprocess.call(cmd)
            subprocess.call(["procdump.exe", "-t", "-ma", str(PID), "/AcceptEula"],cwd=str(work_dir.joinpath("dump/")))

    else:    
        print ("[*] Error with error code %d." % kernel32.GetLastError())
        return

    if config["mode"] != "procdump": 
        print(("[*] wait for dump %d seconds\n") % config["time"])   
        time.sleep(config["time"])

    print("[*] Dumping\n")

    if config["mode"] == "hollows_hunter":
        SuspendProcess(PID)
        subprocess.call(["hollows_hunter.exe"], cwd=str(work_dir.joinpath("dump/")))

    elif config["mode"] == "diff":
        EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned))
        tag_set = set(ProcessIds)

        diff_ProcessIds = list(src_set ^ tag_set)

        new_ProcessIds = []

        for pid in diff_ProcessIds:
            SuspendProcess(pid)
        for pid in new_ProcessIds:
            subprocess.call(["procdump.exe", "-ma", str(pid), "/AcceptEula"], cwd=str(work_dir.joinpath("dump/")))
   
    print("[*] Get network connection info\n")
    subprocess.call(['powershell', 'Get-NetTCPConnection', '|', 'Select-Object', '-Property', 'RemoteAddress, RemotePort, State, OwningProcess, { (Get-Process -Id $_.OwningProcess).Name}, {(Get-Process -Id $_.OwningProcess) | Select-Object -ExpandProperty Path}', '|', 'Export-Csv', '-path', 'netscan.csv'], cwd=str(work_dir.joinpath("dump/")))
    
    print("[*] Make zip\n")
    subprocess.call(["powershell", "compress-archive", "-Force", str(work_dir.joinpath("dump/")) , str(work_dir.joinpath("dump.zip"))])

################################################

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', 8000), allow_none=True)
    print ("Listening on port 8000...")
    server.register_function(download_file, 'download_file')
    server.register_function(upload_file, 'upload_file')
    server.register_function(dump, 'dump')
    server.serve_forever()
