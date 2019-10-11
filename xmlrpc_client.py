#!/usr/bin/env python3

import xmlrpc.client
import os
import sys
import shutil
import json
import subprocess
import time
import yara
import hashlib
import datetime
import requests
import magic
import redis
import socket
import csv
import re
from pathlib import Path
from pymongo import MongoClient
from rq import get_current_job, Queue
from read_avclass_report import run_avclass
from redis import Redis
import configparser

conf = configparser.ConfigParser()
conf.read('tknk.conf', 'UTF-8')

VM_NAME=conf.get('settings','vm_name')
VM_URL=conf.get('settings','vm_url')
AVCLASS=conf.getboolean('plugin','avclass')
DIE=conf.getboolean('plugin','die')
SURICATA=conf.getboolean('plugin','suricata')
VT_KEY=conf.get('plugin','vt_key')

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
            suricata_log.append(json.loads(line))
            line = f.readline()

    shutil.move("packet_dump.pcap", output_path)
    os.remove("eve.json")
    return suricata_log

def private_ip(ip):
    regex = r"(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^::1$)|(^[fF][cCdD])"
    pattern = re.compile(regex)
    match = pattern.match(ip)

    if match == None:
       return 0

    return 1



def get_connections():
    connections=[]
    with open("result/dump/netscan.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        header = next(reader)

        for row in reader:
            if row[0] != "::" and row[0] != "0.0.0.0" and row[2] != "Listen" and row[2] != "Bound" and row[2] != "Idle" and row[3] != "0" and private_ip(row[0]) == 0: 
                connections.append({
                    "remote_address":row[0],
                    "remote_port":int(row[1]),
                    "state":row[2],
                    "pid":int(row[3]),
                    "process_name":row[4],
                    "path":row[5]
                })
    
    return connections

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
    
    #make report format
    report = {
        "meta": {
            "UUID":uid,
            "timestamp":str(datetime.datetime.utcnow().isoformat()),
            "settings": {
                "mode":config['mode'],
                "run_time":config['time']
            },    
            "is_dumped":False,
            "is_matched":False,
            "detail":"",
            "plugins":{
                "avclass":AVCLASS,
                "die":DIE,
                "suricata":SURICATA
            }
        },
        "results": {
            "dump_files_scan":[],
            "upload_file_scan": {},
            "plugins":{
                "avclass":[],
                "die": [],
                "suricata":[]
            }
        }
    }

    #avclass
    if AVCLASS:
        report['results']['plugins']['avclass'] = run_avclass(VT_KEY, file_sha256)

    #Detect it easy
    if DIE:
        cmd=["die/diec.sh", config['path'], "-deepscan:yes", "-showentropy:yes"]
        p = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        report['results']['plugins']['die'] = p.stdout.decode("utf8").split("\n")
        if report['results']['plugins']['die'] != []:
            report['results']['plugins']['die'].pop()

    #load yara rules
    rules = yara.compile('index.yar')

    #make upload scan report
    matches = rules.match(config['path'])

    with open(config['path'],'rb')as f:
        d = f.read()
        file_md5 = str(hashlib.md5(d).hexdigest())
        file_sha1 = str(hashlib.sha1(d).hexdigest())
        file_sha256 = str(hashlib.sha256(d).hexdigest())
        
    report['results']['upload_file_scan']={
        "md5":file_md5, 
        "sha1":file_sha1, 
        "sha256":file_sha256, 
        "detect_rule":list(map(str,matches)), 
        "file_name":config['target_file'], 
        "size":os.path.getsize(config['path']),
        "magic":magic.from_file(config['path'])
        }
  
    if report['results']['upload_file_scan']['detect_rule']!=[]:
        report["meta"]["is_matched"] = True
   
    if "DLL" in report['results']['upload_file_scan']['magic']:
        report["meta"]["detail"] = "In the case of a DLL, only uploaded files is scanned."
        collection.update({u'UUID':uid},report)
        current_job_init(r)
        os._exit(0)

    #revert VM
    cmd=['virsh', 'snapshot-revert', VM_NAME, '--current']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.stderr.decode('utf-8')
    print(output)

    #error check
    if "busy" in output:
        print("failed to initialize KVM: Device or resource busy")
        report['meta']['detail'] = "failed to initialize KVM: Device or resource busy"
        collection.update({u'UUID':uid},report)
        current_job_init(r)
        os._exit(0)
        
    elif "Domain" in output:
        print("Domain snapshot not found: the domain does not have a current snapshot")
        report['meta']['detail'] = "Domain snapshot not found: the domain does not have a current snapshot"
        collection.update({u'UUID':uid},report)
        current_job_init(r)
        os._exit(0)

    #run vm
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

    #upload tools
    if config['mode'] == "hollows_hunter":
        tools = ["tools/hollows_hunter.exe", "tools/pe-sieve.dll", "tools/mouse_emu.pyw"]
    elif config['mode'] == "procdump":
        tools = ["tools/procdump.exe", "tools/mouse_emu.pyw"]
    elif config['mode'] == "diff":
        tools = ["tools/procdump.exe", "tools/mouse_emu.pyw"]
    for tool_name in tools:
        upload(tool_name)
    upload("target/" + config['target_file'])

    if SURICATA:
        tcpdump_pid = subprocess.Popen(['tcpdump', "-i", "virbr0", "-w", "packet_dump.pcap"]).pid

    #start dump in server 
    ret = dump(config)

    #check dump result
    if ret == False:
        print("Connection error\n")
        dump_success = False
        report['meta']['detail'] = "Connection error"
    else:
        ret = download() 
        if ret == True:
            print("dump finish")
            dump_success = True
        else:
            dump_success = False
            if report['meta']['settings']['mode'] == "procdump":
                report['meta']['detail'] = "Process does not exist" 
            else:
                report['meta']['detail'] = "Dump file does not exist" 

    #down vm
    vm_down()

    #dump is fail 
    if dump_success == False:
        report['meta']['is_dumped']=dump_success
        os.mkdir("result/" + str(uid))
        with open("result/"+ str(uid) + "/" +file_sha256+'.json', 'w') as outfile:
            json.dump(report, outfile, indent=4)
        shutil.copyfile(config['path'], "result/"+str(uid)+"/"+config['target_file'])

        #netscan
        report['results']['plugins']['connections'] = get_connections()


        if SURICATA:
            suricata_log=suricata("result/"+str(uid), tcpdump_pid)
            report['results']['plugins']['suricata']=suricata_log
        
        collection.update({u'UUID':uid},report)
        print (json.dumps(report, indent=4))
        collection.update({u'UUID':uid},report)
        current_job_init(r)

        os.remove("dump.zip")
        os._exit(0)

    elif dump_success == True:
        report['meta']['is_dumped']=dump_success
        p = Path("result/dump.zip")
        if p.exists():
            p.unlink()
            print("remove")
        shutil.move("dump.zip", "result/")
        subprocess.run(['unzip', "dump.zip"], cwd="result") 

        p = Path("result/dump/")

        for f in p.glob("**/*"):
            if (".exe" == f.suffix) or (".dll" == f.suffix) or (".shc" == f.suffix) or (".dmp" == f.suffix):
                size = os.path.getsize(str(f))
                matches = rules.match(str(f.resolve()))
                report['results']['dump_files_scan'].append({"detect_rule":list(map(str,matches)), "file_name":f.name, "size":size})

    for scan in  report['results']['dump_files_scan']:
        if scan["detect_rule"] != []:
            report["meta"]["is_matched"] = True
            report['meta']['detail'] = "Detected with yara rule!" 
            break

    shutil.copyfile(config['path'], "result/dump/"+config['target_file'])

    #netscan
    report['results']['plugins']['connections']  = get_connections()  

    if SURICATA:
        suricata_log=suricata("result/dump/", tcpdump_pid)
        report['results']['plugins']['suricata']=suricata_log

    with open("result/dump/"+file_sha256+'.json', 'w') as outfile:
        json.dump(report, outfile, indent=4)
    print (json.dumps(report, indent=4))
    collection.update({u'UUID':uid},report)
    current_job_init(r)

    os.rename("result/dump", "result/"+str(uid))
    os.remove("result/dump.zip")

    return

