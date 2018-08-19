import requests
import logging
import json

import utils


utils.setup_logging()
logger = logging.getLogger(__name__)


def main(args, error=None):
    config = utils.get_config(args.config_file)
    domain = config['AUTH']['server_address']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    
    list_b = list_backup(domain, headers, args.pk, args.repo_target)
    if list_b.status_code == 200:
        print(json.dumps(list_b.json(), indent=4, sort_keys=True))
    else:
        logger.error(list_b.text)
    return


def list_backup(domain, headers, pk=None, target=None):
    query = {"path": target}
    if pk:
        url = "http://{}/rest/api/list/{}".format(domain, pk)
    else: 
        url = "http://{}/rest/api/list/".format(domain)
    response = requests.request("GET", url, headers=headers, params=query)
    return response
