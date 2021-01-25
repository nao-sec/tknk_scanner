#!/usr/bin/env python3
from rq import Queue
import json
import subprocess
import requests
import time
import shutil
import magic
import os
import uuid
import math
import redis
import datetime
import re
import sys
from pathlib import Path
from pymongo import MongoClient
from flask import Flask, jsonify, request, url_for, abort, Response, make_response, send_file, abort
from redis import Redis
from xmlrpc_client import analyze

UPLOAD_FOLDER="target/" 

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def start_analyze():
    if 'application/json' not in request.headers['Content-Type']:
        return jsonify(status_code=2, message="Content-Type Error.")

    requet_data = request.json
    p = Path(requet_data['path'])
    requet_data['target_file']=p.name

    path = "target/"
    if os.path.exists(path+requet_data['target_file']) != True:
        return abort(404)

    uid = str(uuid.uuid4())
    post = {
        "meta": {
            "UUID":uid
        }
    }

    collection.insert_one(post)

    r.set(uid, str(requet_data))

    job = q.enqueue(analyze, uid,  job_id=uid, timeout=requet_data['time']+500)

    return jsonify(status_code=0, UUID=uid, message="Submission Success!")

@app.route('/upload', methods=['POST'])
def file_upload():
    f = request.files['file']
    filename = (f.filename)
    base= Path(UPLOAD_FOLDER)
    f.save(str(base/filename))

    file_type = magic.from_file("target/"+filename)

    if ("PE32" or"PE32+") not in file_type:
            return make_response(jsonify(status_code=2, message= str(file_type)+ " Invalid File Format!! Only PE Format File."  ), 400)

    if (("PE32" or "PE32+") in file_type):
        path = Path("target/"+filename)
        if path.suffix != "exe":
            os.rename("target/"+path.name, "target/"+path.stem+".exe")
            filename=path.stem+".exe"

    return jsonify(status_code=0, path=UPLOAD_FOLDER+filename)

@app.route('/result/<uuid>')
def show_result(uuid=None):

    report = collection.find_one({u"meta.UUID":uuid})
    if report == None:
        return abort(404)
    report.pop('_id')

    if 1 < len(report['meta']):
        return jsonify(status_code=0, report=report)
    else:
        return make_response(jsonify(status_code=1, message='Analysing...'), 206)
        
@app.route('/yara/<rule_name>')
def get_yara_file(rule_name=None):

    pool =  redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)

    rule_name_check = rule_name.replace("_", "")
    if rule_name_check.isalnum() == False:
        return make_response(jsonify(status_code=2, message="Invalid rule_name"), 400)

    db = json.loads(r.get("yara_db").decode('utf-8').replace("\'", "\""))    

    try:
        with open(db[rule_name], 'r') as f:
            yara_file=f.read()
    except:
         return make_response(jsonify(status_code=2, message="File not found"), 404)

    return jsonify(status_code=0, rule=yara_file)

@app.route('/page/<page_num>')
def page(page_num=None):
    reports=[]
    page_num = int(page_num)
    line_num = 30.0
    page_size= math.ceil(len(list(collection.find()))/line_num)
    page_item = collection.find().sort('timestamp',-1).limit(int(line_num)).skip((page_num-1)*int(line_num))
    for p in page_item:
        detect_rules = p['result']['uploaded_file_scan']['detect_rules']
        for dumped_file in p['result']['dumped_file_scan']:
            detect_rules.extend(dumped_file['detect_rules'])
        detect_rules = list(set(detect_rules))
        new_page_item = {
            "meta":p['meta'],
            "detect_rules_summary":detect_rules
        }
        reports.append(new_page_item)
    return jsonify(status_code=0, reports=page, page_size=page_size)

@app.route('/jobs')
def job_ids():
    q = Queue(connection=Redis())# Getting the number of jobs in the queue
    queued_job_ids = q.job_ids # Gets a list of job IDs from the queue
    queued_jobs=[]
    if r.get('current_job_id') != b'':
        current_job_id=r.get('current_job_id')
        config = eval(r.get(current_job_id).decode('utf-8'))
        del config['path']
        current_job={"id":current_job_id, "config":config}
    else:
        current_job=None
    
    for queued_job_id in queued_job_ids:
        config = eval(r.get(queued_job_id).decode('utf-8'))
        del config['path']
        queued_jobs.append({"id":queued_job_id, "config":config})

    return jsonify(status_code=0, queued_jobs=queued_jobs, current_job=current_job)

@app.route('/download/<uuid>')
def download(uuid=None):
    uuid = os.path.basename(uuid)
    path = "result/"

    if os.path.exists(path+uuid) != True:
        return abort(404)

    zipname = uuid+".zip"
    cmd=['zip', '-r', '-P', 'infected', path+zipname, path+uuid]
    subprocess.run(cmd, stdout=subprocess.PIPE)

    return send_file(path+zipname, as_attachment=True, attachment_filename=zipname)

@app.route('/search/<search_type>/<value>')    
def search(search_type=None, value=None):
    if search_type != "md5" and search_type != "sha1" and search_type != "sha256":
        return abort(404)
    search_results=[]

    report = collection.find({"result.uploaded_file_scan."+search_type:value})

    results = list(report)

    for r in results:
        detect_rules = r['result']['uploaded_file_scan']['detect_rules']
        for dumped_file in r['result']['dumped_file_scan']:
            detect_rules.extend(dumped_file['detect_rules'])
        detect_rules = list(set(detect_rules))
        new_page_item = {
            "meta":r['meta'],
            "detect_rules_summary":detect_rules
        }
        search_results.append(new_page_item)

    if len(search_results) == 0:
        abort(404)
    
    return jsonify(status_code=0, results=search_results)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(status_code=2, message='Not found.'), 404)

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.scan_database
    collection = db.scan_collection

    pool =  redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.set('current_job_id', "")
   
    with open("index.yar", 'r') as f:
        index = f.readlines()

    yara_db={}
    re_search = re.compile('(%s.*%s)' % ('\"', '\"'))
    rule_regexp = re.compile('%s\s([\w\d_:]+)(\s:?\s?[\w\s]*)?[\s\n]*%s' % ('rule', '{'))

    l = len(index)

    for i in range(l):
        sys.stdout.write("\r[*] Loading yara rules %d/%d" % (i+1,l))
        sys.stdout.flush()
        m = re_search.search(index[i])
        path = m.group(0).strip('\"')

        with open(path, 'r') as f:
            rule_file = f.read()
            rules_list = rule_regexp.findall(rule_file)
            if rules_list != []:
                for rule in rules_list:
                    yara_db.update({rule[0].strip().strip(":"):path})
            else:
                pass
    
    r.set('yara_db', str(yara_db))

    # Tell RQ what Redis connection to use
    redis_conn = Redis(host='localhost', port=6379)
    q = Queue(connection=redis_conn)  # no args implies the default queue

    app.run(host='0.0.0.0', port=8000)
