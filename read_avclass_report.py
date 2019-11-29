import json, sys, re, subprocess, os
import requests

def run_avclass (vt_key, sha256):
    #Download VT report
    params = {'apikey': vt_key, 'resource':sha256}

    headers = {
      "Accept-Encoding": "gzip, deflate",
      "User-Agent" : "Retrieving file scan reports"
      }

    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)

    json_response = response.json()
    file_name = params['resource']+".json"

    if json_response['response_code']==0:
        return ({"flag":False, "data":"It does not exist in VirusTotal"})

    with open (file_name, 'w') as f:
        json.dump(json_response, f)

    vt_url = "https://www.virustotal.com/#/file/" + sha256 + "/detection"

    #run AVClass
    cmd = ["python3 ./avclassplusplus/avclass_labeler.py", "-vt", file_name, "-v"]
    subprocess.call(cmd)

    #read AVClass results
    with open(sha256 +".verbose", 'r') as f:
        read_data = f.read()

    r = re.compile('(%s.*%s)' % ("\[", "\]"))
    m = r.search(read_data)

    if m != None:
        fam = m.group(0)
        fam= (eval(fam))
        fam_json=[]

        for column in fam:
            fam_json.append({"family_name":column[0], "count":column[1]})
    
    else:
        fam_json=[]

    os.remove(sha256+".json")
    os.remove(sha256+".verbose")
    return ({"flag":True, "data":fam_json})



