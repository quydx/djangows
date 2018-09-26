#!C:\env\env\Scripts\python.exe
import threading
import argparse
import requests
import os
import json
from cryptography.fernet import Fernet

import utils

parent = "E:\\Huyen Trang\\project\\djangows\\client\\windows\\"
clientConf = parent + "client.conf"

def parse():
    parser = argparse.ArgumentParser(description="Run the Backup CLI")
    parser.add_argument('-c', '--config-file', dest='config_file', default=clientConf,
                        help='Path of config file')
    args = parser.parse_args()

    if os.path.exists(args.config_file):
        return args
    else:
        print("File config does not exist ")
        exit(1)

def get_job():
    threading.Timer(5, get_job).start() # repeat function every 5s
    args = parse()
    config = utils.get_config(args.config_file)
    address = config['CONTROLLER']['address']
    token = config['AUTH']['token']
    url = "http://{}/api/get-job/".format(address)
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)

    # decrypt
    key = config['CRYPTO']['key']
    cipher_suite = Fernet(key)
    plain_data = cipher_suite.decrypt(response.text.encode())
    response_data = json.loads(plain_data.decode())
    print(response_data)

    backupConf = parent + "backcli.py"
    restoreConf = parent + "restorecli.py"
    for job in response_data['jobs']:
        if job['job_type'] == "backup":
            os.system("python \""+ backupConf + "\" -t " + job['path'] + \
                    " -s " + job['server'] + \
                    " -c " + args.config_file + \
                    " -j " + str(job['job_id']))
        elif job['job_type'] == "restore":
            path = utils.convert_linuxtowin_path(job['path'])
            os.system("python "+ restoreConf + " -t " + path + \
                    " -c " + args.config_file + \
                    " -p " + str(job['backup_id']) + \
                    " -j " + str(job['job_id']))


def info_agent():
    #threading.Timer(60, info_agent).start()
    print("Send information agent")
    args = parse()
    config = utils.get_config(args.config_file)
    address = config['CONTROLLER']['address']
    token = config['AUTH']['token']
    url = "http://{}/api/info-agent/".format(address)
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    data = utils.get_info_agent()
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    print(response.status_code)


def main():
    info_agent()
    get_job()
            
            
if __name__ == '__main__':
    main()
