#!/usr/bin/env python3

import json, subprocess, requests, time, shutil, magic, os, uuid
from pathlib import Path
from pymongo import MongoClient
from flask import Flask, jsonify, request, url_for, abort, Response, make_response

with open("tknk.conf", 'r') as f:
    tknk_conf = json.load(f)

VM_NAME=tknk_conf['vm_name']
UPLOAD_FOLDER="target/" 

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def start_analyze():
    if 'application/json' not in request.headers['Content-Type']:
        print(request.headers['Content-Type'])
        return jsonify(status_code=2, message="Content-Type Error.")

    with open("state.json", 'r') as f:
        state = json.load(f)

    if state['state'] == 1:
        return make_response(jsonify(status_code=1, message="It is processing now. Wait for analysis."), 406)
    elif state['state'] == 0:
        state['state'] = 1
        with open("state.json", 'w') as f:
            json.dump(state, f)

    json_data = request.json

    uid = str(uuid.uuid4())
    post = {"UUID":uid}

    collection.insert_one(post)

    json_data['target_file']=json_data['path'].split("/")[1]
    print(json.dumps(json_data, indent=4))
    with open('config.json', 'w') as outfile:
        json.dump(json_data, outfile)

    cmd=[("virsh snapshot-revert " + VM_NAME + " --current")]

    p = (subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True))
    output = p.stderr.read().decode('utf-8')
    print(output)

    if "busy" in output:
        state={"state":0}
        with open("state.json", 'w') as f:
            json.dump(state, f)
        return make_response(jsonify(status_code=2, message="failed to initialize KVM: Device or resource busy"), 500)
        
    elif "Domain" in output:
        state={"state":0}
        with open("state.json", 'w') as f:
            json.dump(state, f)
        return make_response(jsonify(status_code=2, message="Domain snapshot not found: the domain does not have a current snapshot"), 500)

    cmd = [("./xmlrpc_client.py "+ uid)]
    subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    return jsonify(status_code=0, UUID=uid, message="Submission Success!")

@app.route('/upload', methods=['POST'])
def file_upload():
    f = request.files['file']
    filename = (f.filename)
    f.save(os.path.join(UPLOAD_FOLDER, filename))

    file_type = magic.from_file("target/"+filename)
    print(file_type)

    if ("DLL" in file_type) or (("PE32" or"PE32+") not in file_type):
            print("Invalid File Format!! Only PE Format File(none dll).")
            return make_response(jsonify(status_code=2, message="Invalid File Format!! Only PE Format File(none dll)."), 400)

    if (("PE32" or "PE32+") in file_type):
        path = Path("target/"+filename)
        if path.suffix != "exe":
            os.rename("target/"+path.name, "target/"+path.stem+".exe")
            filename=path.stem+".exe"

    return jsonify(status_code=0, path=UPLOAD_FOLDER+filename)

@app.route('/results/<uuid>')
def show_result(uuid=None):
    print(uuid)

    result = list(collection.find({u"UUID":uuid}))[0]
    result.pop('_id')
    
    if "scans" in result:
        return jsonify(status_code=0, result=result)
    else:
        return make_response(jsonify(status_code=1, message='Analysing.'), 206)
        
    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(status_code=2, message='Not found.'), 404)

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.scan_database
    collection = db.scan_collection

    state={"state":0}
    with open("state.json", 'w') as f:
        json.dump(state, f)

    app.run(host='0.0.0.0', port=8000)
    

