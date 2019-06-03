#!/usr/bin/env python3

import xmlrpc.client
import os, sys, shutil, json, subprocess, time, yara, hashlib, datetime, requests, magic, redis, socket, pefile
from pathlib import Path
from pymongo import MongoClient
from rq import get_current_job, Queue
from read_avclass_report import run_avclass
from redis import Redis

with open("tknk.conf", 'r') as f:
    tknk_conf = json.load(f)

VM_NAME=tknk_conf['vm_name']
VM_URL=tknk_conf['vm_url']

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

def dump(config):
    proxy = xmlrpc.client.ServerProxy(VM_URL)
    try:
        proxy.dump(config)
        return True
    except:
        return False

def vm_down():
    print(subprocess.call(['virsh', "destroy", VM_NAME]))

def current_job_init(r):
    q = Queue(connection=Redis())# Getting the number of jobs in the queue
    queued_job_ids = q.job_ids # Gets a list of job IDs from the queue

    if len(queued_job_ids) == 0:
        r.set('current_job_id', "")

    return

def size_fmt(num, suffix='B'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1000.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1000.0
        return "%.1f%s%s" % (num, 'Yi', suffix)


def suricata(output_path, tcpdump_pid):
    suricata_log=[]
    subprocess.run(['kill', str(tcpdump_pid)])

    if os.path.getsize("packet_dump.pcap") == 0:
        os.remove("packet_dump.pcap")
        return suricata_log

    cmd=["suricata", "-r", "packet_dump.pcap", "-l", "."]
    p = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    if os.path.getsize("eve.json") == 0:
        os.remove("eve.json")
        shutil.move("packet_dump.pcap", output_path)
        return suricata_log
        
    with open("eve.json") as f:
        line = f.readline()
        while line:
            print(line)
            suricata_log.append(json.loads(line))
            line = f.readline()

    shutil.move("packet_dump.pcap", output_path)
    os.remove("eve.json")
    return suricata_log

def analyze(uid):

    #db connect
    client = MongoClient('localhost', 27017)
    db = client.scan_database
    collection = db.scan_collection

    #redis connect
    pool =  redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    
    #update current_job
    job=get_current_job()
    r.set('current_job_id', job.id)

    #config read & write
    config = eval(r.get(uid).decode('utf-8'))
    pe =  pefile.PE(config['path'])
    config['entrypoint'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    
    #make report format
    result = {"result":{"detail":"", "is_success":False},
              "run_time":str(config['time']), 
              "mode":config['mode'],
              "timestamp":str(datetime.datetime.today().isoformat()),
              "scans":[],
              "UUID":uid,
              "magic":magic.from_file(config['path']),
              "virus_total":0,
              "avclass":{"flag":None, "data":[]}
             }
 
    with open(config['path'],'rb')as f:
        d = f.read()
        file_md5 = str(hashlib.md5(d).hexdigest())
        file_sha1 = str(hashlib.sha1(d).hexdigest())
        file_sha256 = str(hashlib.sha256(d).hexdigest())

    #avclass
    if tknk_conf['virus_total'] == 1:
        result['virus_total'] = 1
        result['avclass'] = run_avclass(tknk_conf['vt_key'], file_sha256)

    #Detect it easy
    cmd=["die/diec.sh", config['path']]
    p = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    result['die'] = p.stdout.decode("utf8").split("\n")
    if result['die'] != []:
        result['die'].pop()

    #read yara rules
    rules = yara.compile('index.yar')
    matches = rules.match(config['path'])

    result['target_scan']=({"md5":file_md5, "sha1":file_sha1, "sha256":file_sha256, "detect_rule":list(map(str,matches)), "file_name":config['target_file'], "size":size_fmt(os.path.getsize(config['path']))})

    if result['target_scan']['detect_rule']!=[]:
        result["result"]["is_success"] = True

    cmd=['virsh', 'snapshot-revert', VM_NAME, '--current']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.stderr.decode('utf-8')
    print(output)

    if "busy" in output:
        print("failed to initialize KVM: Device or resource busy")
        result["result"]["detail"] = "failed to initialize KVM: Device or resource busy"
        collection.update({u'UUID':uid},result)
        current_job_init(r)
        os._exit(0)
        
    elif "Domain" in output:
        print("Domain snapshot not found: the domain does not have a current snapshot")
        result["result"]["detail"] = "Domain snapshot not found: the domain does not have a current snapshot"
        collection.update({u'UUID':uid},result)
        current_job_init(r)
        os._exit(0)

    c=0

    while(1):
        vm_state = subprocess.check_output(["virsh", "domstate", VM_NAME])
        time.sleep(1)
        c+=1

        if "running" in str(vm_state.decode('utf-8')):
            break
        if c == 60:
            current_job_init(r)
            os._exit(0)
    if config['mode'] == "hollows_hunter":
        tools = ["tools/hollows_hunter.exe", "tools/pe-sieve.dll", "tools/mouse_emu.pyw"]
    elif config['mode'] == "procdump":
        tools = ["tools/procdump.exe", "tools/mouse_emu.pyw"]
    elif config['mode'] == "scylla":
        tools = ["tools/Scylla.dll", "tools/mouse_emu.pyw"]
    elif config['mode'] == "diff":
        tools = ["tools/procdump.exe", "tools/mouse_emu.pyw"]

    for tool_name in tools:
        upload(tool_name)

    upload("target/" + config['target_file'])

    tcpdump_pid = subprocess.Popen(['tcpdump', "-i", "virbr0", "-w", "packet_dump.pcap"]).pid

    ret = dump(config)

    if ret == False:
        print("Connection error\n")
        dump_success = False
        result["result"]["detail"] = "Connection error"
    else:
        ret = download() 
     
        if ret == True:
            print("dump finish")
            dump_success = True

        else:
            dump_success = False
            if result["mode"] == "procdump":
                result["result"]["detail"] = "Process does not exist" 
            else:
                result["result"]["detail"] = "Dump file does not exist"  

    vm_down()

    if dump_success == False:
        result['dump_success']=dump_success
        os.mkdir("result/" + str(uid))
        with open("result/"+ str(uid) + "/" +file_sha256+'.json', 'w') as outfile:
                json.dump(result, outfile, indent=4)
        shutil.copyfile(config['path'], "result/"+str(uid)+"/"+config['target_file'])

        suricata_log=suricata("result/"+str(uid), tcpdump_pid)
        result['suricata']=suricata_log
        collection.update({u'UUID':uid},result)

        print (json.dumps(result, indent=4))
        collection.update({u'UUID':uid},result)
        current_job_init(r)

        os.remove("dump.zip")
        
        os._exit(0)

    elif dump_success == True:
        result['dump_success']=dump_success
        p = Path("result/dump.zip")
        if p.exists():
            p.unlink()
            print("remove")
        shutil.move("dump.zip", "result/")
        subprocess.run(['unzip', "dump.zip"], cwd="result")   

        p = Path("result/dump/")

        for f in p.glob("**/*"):
            if (".exe" == f.suffix) or (".dll" == f.suffix) or (".dmp" == f.suffix):
                size = os.path.getsize(str(f))
                matches = rules.match(str(f.resolve()))
                result['scans'].append({"detect_rule":list(map(str,matches)), "file_name":f.name, "size":size_fmt(size)})

    for scan in result["scans"]:
        if scan["detect_rule"] != []:
            result["result"]["is_success"] = True
            result["result"]["detail"] = "Detected with yara rule!" 
            break

    shutil.copyfile(config['path'], "result/dump/"+config['target_file'])

    suricata_log=suricata("result/dump/", tcpdump_pid)
    result['suricata']=suricata_log

    with open("result/dump/"+file_sha256+'.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

    print (json.dumps(result, indent=4))
    collection.update({u'UUID':uid},result)
    current_job_init(r)

    os.rename("result/dump", "result/"+str(uid))
    os.remove("result/dump.zip")

    return

