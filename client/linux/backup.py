import os
import requests
import json
import utils
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create a console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

# create a file handler
handler = logging.FileHandler('backup_log.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


def main(args):
    config = utils.get_config(args.config_file)
    domain = config['AUTH']['domain']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    path = args.repo_target

    # start a backup 
    init = init_backup(domain, headers) 

    if init.status_code == 200:
        json_data = json.loads(init.text)
        logger.debug(json_data)
        if json_data['status'] == "ok":
            logger.info("Ready to backup")
            backup_id = json_data['backup_id']
            send_metadata(config, headers, path, backup_id)
        else:
            logger.error("Fail in prepare to backup")
    elif init.status_code == 401:
        logger.error("Authentication: " + init.text)
    elif init.status_code == 507:
        logger.error("Insufficient Storage: " + init.text)
    else:
        logger.error("Unknown - " + str(init.status_code))


def init_backup(domain, headers):
    url = "http://{}/rest/api/initialization/".format(domain)
    response = requests.request("GET", url, headers=headers)
    return response


def send_metadata(config, headers, path, backup_id):
    file_or_dir = utils.FileDir(path, config)
    domain = config['AUTH']['domain']
    url = "http://{}/rest/api/metadata/".format(domain)
    payload = file_or_dir.get_metadata()
    payload["backup_id"] = backup_id
    data = str(payload).replace("'", '"')  # convert to json format 

    logger.debug(path)
    response = requests.request("POST", url, data=data, headers=headers)

    logger.debug(response.json())
    response_data = response.json()

    # Call send data function if response data have new block 
    if 'blocks' in response_data and response_data['blocks'] != []:
        send_data(domain, headers, path, response_data['blocks'], \
                response_data['file_object'], response_data['checksum'])

        logger.info("DONE: Send {} done".format(path))

    # Perform the same with files and subdirectories
    if os.path.isdir(path):
        for file_or_dir in os.listdir(path):
            send_metadata(config, headers, os.path.join(path, file_or_dir), backup_id)
    return


def send_data(config, headers, path, blocks, file_object, checksum):
    domain = config['AUTH']['domain']
    block_size = int(config['FILE']['block_size'])
    url = "http://{}/rest/api/upload/data/".format(domain)
    fin = open(path, 'rb')
    count = 0

    # Send each block one by one in the block_ids list
    for chunk, block_id in utils.read_in_blocks(fin, blocks, block_size):
        files = {'block_data': chunk}
        values = {'block_id' : block_id, 'file_object': file_object, 'checksum': checksum[count]}
        logger.debug("SENDING: {} - {}".format(block_id, checksum[count]))
        count += 1
        response = requests.post(url, files=files, data=values)
        logger.debug(response.text)
    return
