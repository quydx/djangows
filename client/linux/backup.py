import os
import requests
import json
import logging

from cryptography.fernet import Fernet

import utils


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
    server_address = args.server_address or config['AUTH']['server_address']
    token = config['AUTH']['token']
    key = config['CRYPTO']['key']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    block_size = int(config['FILE']['block_size'])
    path = args.repo_target

    # start a backup 
    init = init_backup(server_address, headers) 

    if init.status_code == 200:
        json_data = json.loads(init.text)
        logger.debug(json_data)
        if json_data['status'] == "ok":
            logger.info("Ready to backup")
            backup_id = json_data['backup_id']
            send_metadata(server_address, block_size, token, path, backup_id, key)
        else:
            logger.error("Fail in prepare to backup")
    elif init.status_code == 401:
        logger.error("Authentication: " + init.text)
    elif init.status_code == 507:
        logger.error("Insufficient Storage: " + init.text)
    else:
        logger.error("Unknown - " + str(init.status_code))


def init_backup(server_address, headers):
    url = "http://{}/rest/api/initialization/".format(server_address)
    response = requests.request("GET", url, headers=headers)
    return response


def send_metadata(server_address, block_size, token, path, backup_id, key):
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    file_or_dir = utils.FileDir(path, block_size)
    url = "http://{}/rest/api/metadata/".format(server_address)
    payload = file_or_dir.get_metadata()
    payload["backup_id"] = backup_id

    # encrypt
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(json.dumps(payload).encode())
    
    logger.debug(path)
    response = requests.request("POST", url, data=cipher_text, headers=headers)

    # decrypt
    plain_data = cipher_suite.decrypt(response.text.encode())
    response_data = json.loads(plain_data.decode())
    logger.debug(response_data)

    # Call send data function if response data have new block 
    if 'blocks' in response_data and response_data['blocks'] != []:
        send_data(server_address, block_size, token, path, response_data['blocks'], \
                response_data['file_object'], response_data['checksum'], key)

        logger.info("DONE: Send {} done".format(path))

    # Perform the same with files and subdirectories
    if os.path.isdir(path):
        for file_or_dir in os.listdir(path):
            send_metadata(server_address, block_size, token, os.path.join(path, file_or_dir), backup_id, key)
    return


def send_data(server_address, block_size, token, path, blocks, file_object, checksum, key):
    headers = {'Authorization': token}
    url = "http://{}/rest/api/upload/data/".format(server_address)
    fin = open(path, 'rb')
    count = 0

    # Send each block one by one in the block_ids list
    for chunk, block_id in utils.read_in_blocks(fin, blocks, block_size):
        # encrypt
        cipher_suite = Fernet(key)
        files = {'block_data': cipher_suite.encrypt(chunk)}
        values = {'block_id' : block_id, 'file_object': file_object, 'checksum': checksum[count]}
        # logger.debug(files)
        # cipher_file = cipher_suite.encrypt(json.dumps(files).encode())
        # logger.debug(cipher_file)
        cipher_text = cipher_suite.encrypt(json.dumps(values).encode())
        logger.debug(cipher_text)

        logger.debug("SENDING: {} - {}".format(block_id, checksum[count]))
        count += 1
        response = requests.post(url, files=files, data=values, headers=headers)
        
        logger.debug(response.text)
    return
