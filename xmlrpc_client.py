#!/usr/bin/env python3

import xmlrpc.client
import os, sys, shutil, json, subprocess, time, yara, hashlib, datetime, requests
from pathlib import Path
from pymongo import MongoClient

with open("tknk.conf", 'r') as f:
    tknk_conf = json.load(f)

VM_NAME=tknk_conf['vm_name']
VM_URL=tknk_conf['vm_url']

def change_state():
    state={"state":0}

    with open("state.json", 'w') as f:
        json.dump(state, f)

def download():
    proxy = xmlrpc.client.ServerProxy(VM_URL)
    with open("dump.zip", "wb") as handle:
        try:
            handle.write(proxy.download_file().data)
            return True

        except xmlrpc.client.Fault:
            print(sys.exc_info())
            return sys.exc_info()

            
def upload(filename):
    proxy = xmlrpc.client.ServerProxy(VM_URL)
    with open(filename, "rb") as handle:
        binary_data = xmlrpc.client.Binary(handle.read())
    if "/" in filename:
        filename = filename.rsplit("/", 1)[1]
    print("upload..." + filename)
    proxy.upload_file(binary_data, filename)

def dump():
    proxy = xmlrpc.client.ServerProxy(VM_URL)
    try:
        proxy.dump()
        return True
    except:
        return False

def vm_down():
    print(subprocess.call(['virsh', "destroy", VM_NAME]))

if __name__ == '__main__':
    args = sys.argv

    #db connect
    client = MongoClient('localhost', 27017)
    db = client.scan_database

    collection = db.scan_collection

    #read config
    with open('config.json', 'r') as f:
        config = json.load(f)

    uid=args[1]

    #make report format
    now = datetime.datetime.today()
    result = {"result":{"detail":"", "is_success":False},
              "run_time":config['time'], 
              "mode":config['mode'],
              "timestamp":str(now.isoformat()),
              "scans":[],
              "UUID":uid
             }

    file_sha256 = str(hashlib.sha256(open(config['path'],'rb').read()).hexdigest())

    rules = yara.compile('index.yar')
    matches = rules.match(config['path'])

    result['scans'].append({"sha256":file_sha256, "detect_rule":list(map(str,matches)), "file_name":config['target_file']})

    cmd=[("virsh snapshot-revert " + VM_NAME + " --current")]
    p = (subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True))
    output = p.stderr.read().decode('utf-8')
    print(output)

    if "busy" in output:
        print("failed to initialize KVM: Device or resource busy")
        result["result"]["is_success"] = False
        result["result"]["detail"] = "failed to initialize KVM: Device or resource busy"
        change_state()  
        collection.update({u'UUID':uid},result)
        exit()
        
    elif "Domain" in output:
        print("Domain snapshot not found: the domain does not have a current snapshot")
        result["result"]["is_success"] = False
        result["result"]["detail"] = "Domain snapshot not found: the domain does not have a current snapshot"
        change_state()  
        collection.update({u'UUID':uid},result)
        exit()

    c=0

    while(1):
        vm_state = subprocess.check_output(["virsh", "domstate", VM_NAME])
        time.sleep(1)
        c+=1
        #print (vm_state.decode('utf-8'))
        if "running" in str(vm_state.decode('utf-8')):
            break
        if c == 60:
            change_state()
            exit()

    upload("config.json")
    tools = ["tools/hollows_hunter.exe", "tools/pe-sieve.dll", "tools/procdump.exe", "tools/pssuspend.exe", "tools/mouse_emu.pyw"]

    for tool_name in tools:
        upload(tool_name)

    upload("target/" + config['target_file'])

    ret = dump()

    if ret == False:
        print("Connection error\n")
        is_success = False
        result["result"]["detail"] = "Connection error"  
    else:
        ret = download() 
     
        if ret == True:
            print("dump finish")
            is_success = True

        else:
            is_success = False
            if result["mode"] == "procdump":
                result["result"]["detail"] = "Process does not exist" 
            else:
                result["result"]["detail"] = "Dump file does not exist"  

    vm_down()

    if is_success == False:
        for scan in result["scans"]:
            if scan["detect_rule"] != []:
                result["result"]["is_success"] = True
                result["result"]["detail"] = "Detected with yara rule!"  
                break
        os.mkdir("result/" + str(uid))
        with open("result/"+ str(uid) + "/" +file_sha256+'.json', 'w') as outfile:
                json.dump(result, outfile, indent=4)

        print (json.dumps(result, indent=4))
        os.remove("config.json")
        collection.update({u'UUID':uid},result)
        change_state()  
        exit()

    elif is_success == True:
        p = Path("result/dump.zip")
        if p.exists():
            p.unlink()
            print("remove")
        shutil.move("dump.zip", "result/")
        subprocess.run(['unzip', "dump.zip"], cwd="result")   

        p = Path("result/dump/")

        for f in p.glob("**/*"):
            print(f.suffix)
            print(f.resolve())
            print(f.name)
            if (".exe" == f.suffix) or (".dll" == f.suffix) or (".dmp" == f.suffix):
	            sha256_hash = str(hashlib.sha256(open(str(f.resolve()),'rb').read()).hexdigest())
	            matches = rules.match(str(f.resolve()))
	            result['scans'].append({"sha256":sha256_hash, "detect_rule":list(map(str,matches)), "file_name":f.name})

    for scan in result["scans"]:
        if scan["detect_rule"] != []:
            result["result"]["is_success"] = True
            result["result"]["detail"] = "Detected with yara rule!" 
            break

    print (json.dumps(result, indent=4))

    with open("result/dump/"+file_sha256+'.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

    os.rename("result/dump/", "result/"+str(uid))
    os.remove("result/dump.zip")
    os.remove("config.json")

    collection.update({u'UUID':uid},result)
    change_state()

