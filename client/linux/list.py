import requests
import utils
import argparse


parser = argparse.ArgumentParser(description="Run the list backups")
parser.add_argument('--config-file', dest='config_file', default='client.conf',
                    help='Path of config file')
parser.add_argument('--pk', dest='pk', help='Index of backup')             
args = parser.parse_args()


def main(args):
    config = utils.get_config(args.config_file)
    domain = config['AUTH']['domain']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    list_b = list_backup(domain, headers, args.pk)
    # print(list_b.status_code)
    print(list_b.text)

def list_backup(domain, headers, pk=None):
    if pk:
        url = "http://{}/rest/api/list/{}".format(domain, pk)
    else: 
        url = "http://{}/rest/api/list/".format(domain)
    response = requests.request("GET", url, headers=headers)
    return response

if __name__ == '__main__':
    main(args)