import requests
import utils
import argparse
import logging
import utils 


utils.setup_logging()
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description="Run the list backups")
parser.add_argument('--config-file', dest='config_file', default='conf.d/client.conf',
                    help='Path of config file')
parser.add_argument('--pk', dest='pk', help='Index of backup')             
args = parser.parse_args()


def main(args):
    config = utils.get_config(args.config_file)
    domain = config['AUTH']['server_address']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    list_b = list_backup(domain, headers, args.pk)
    if list_b.status_code == 200:
        logger.info(list_b.text)
    else:
        logger.error(list_b.text)
    return


def list_backup(domain, headers, pk=None):
    if pk:
        url = "http://{}/rest/api/list/{}".format(domain, pk)
    else: 
        url = "http://{}/rest/api/list/".format(domain)
    response = requests.request("GET", url, headers=headers)
    return response


if __name__ == '__main__':
    main(args)
