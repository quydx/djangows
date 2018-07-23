#!/home/locvu/backup_server/env/bin/python

import threading
import argparse
import requests
import os
import json
import logging

from cryptography.fernet import Fernet

import utils


def parse():
    parser = argparse.ArgumentParser(description="Run the Backup CLI")
    parser.add_argument('--config-file', dest='config_file', default='client.conf',
                        help='Path of config file')
    args = parser.parse_args()

    if os.path.exists(args.config_file):
        return args
    else:
        print("File config does not exist ")
        exit(1)

def get_job():
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
    for job in response_data['jobs']:
        os.system("./backcli -t " + job['path'] + \
                  " -s " + job['server'] + \
                  " --config-file " + args.config_file + \
                  " -j " + str(job['job_id']))


def main(f_stop):
    get_job()
    if not f_stop.is_set():
        threading.Timer(5, main, [f_stop]).start()


if __name__ == '__main__':
    f_stop = threading.Event()
    main(f_stop)