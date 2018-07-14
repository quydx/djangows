#!/home/locvu/backup_server/env/bin/python

import threading
import argparse
import requests
import os

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
    

def main():
    threading.Timer(60.0, get_job).start()


if __name__ == '__main__':
    main()