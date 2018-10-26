#!/usr/bin/python3
import threading
import argparse
import requests
import os
import json
import logging

from cryptography.fernet import Fernet

import utils


utils.setup_logging()
logger = logging.getLogger(__name__)


def parse():
    parser = argparse.ArgumentParser(description="Run the Backup CLI")
    parser.add_argument('--config-file', dest='config_file', default='conf.d/client.conf',
                        help='Path of config file')
    args = parser.parse_args()

    if os.path.exists(args.config_file):
        return args
    else:
        print("File config does not exist ")
        exit(1)


def get_job():
    '''
    Get backup and restore job from controller node
    '''
    threading.Timer(5, get_job).start()
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
        if job['job_type'] == "backup":
            os.system("./backcli -t " + '"' + job['path'] + '"' + \
                    " -s " + job['server'] + \
                    " -c " + args.config_file + \
                    " -j " + str(job['job_id']))
        elif job['job_type'] == "restore":
            os.system("./restorecli -t " + '"' + job['path'] + '"' + \
                    " -c " + args.config_file + \
                    " -p " + str(job['backup_id']) + \
                    " -j " + str(job['job_id']))


def info_agent():
    # threading.Timer(60, info_agent).start()
    logger.info("Send information agent")
    args = parse()
    config = utils.get_config(args.config_file)
    address = config['CONTROLLER']['address']
    token = config['AUTH']['token']
    url = "http://{}/api/info-agent/".format(address)
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    data = utils.get_info_agent()
    requests.request("POST", url, data=json.dumps(data), headers=headers)


def main():
    get_job()
    info_agent()


if __name__ == '__main__':
    main()
