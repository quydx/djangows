import os
import requests
import json
import utils
import logging
from cryptography.fernet import Fernet

print("Start backup.py")
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


def main(args, repo_target, error=None):
    config = utils.get_config(args.config_file)
    ctl_address = config['CONTROLLER']['address']
    url_result = "http://{}/api/result-backup/".format(ctl_address)
    server_address = args.server_address or config['AUTH']['server_address']
    token = config['AUTH']['token']
    key = config['CRYPTO']['key']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}

    if error:
        data = {"job_id": args.job_id, "status_code": 404, "msg": error, 
                "path": repo_target, "server": server_address}
    else:
        block_size = int(config['FILE']['block_size'])
        path = repo_target # Path of directory need to backup
        data = {}

        # start a backup 
        init = init_backup(server_address, headers)
        #print("init.status", init.status_code)
        
        if init.status_code == 200:
            json_data = json.loads(init.text)
            logger.debug(json_data)
            if json_data['status'] == "ok":
                logger.info("Ready to backup")
                backup_id = json_data['backup_id']
                send_metadata(server_address, block_size, token, path, backup_id, key)

                # Notify send last message
                url_last_msg = "http://{}/rest/api/result_backup/{}".format(server_address, backup_id)
                last_msg = requests.request("GET", url_last_msg, headers=headers)
                print(last_msg)
                data.update(last_msg.json())

                msg = "Successfull"
            else:
                msg = "Fail in prepare to backup"
                logger.error(msg)

        elif init.status_code == 401:
            msg = "Authentication: " + init.text
            logger.error(msg)
        elif init.status_code == 507:
            msg = "Insufficient Storage: " + init.text
            logger.error(msg)
        else:
            msg = "Unknown - " + str(init.status_code)
            logger.error(msg)

        data.update({"job_id": args.job_id, "status_code": init.status_code, "msg": msg,
                     "server":server_address, "path": path})
    
    # Send backup result to Controller  
    response = requests.request("POST", url_result, data=json.dumps(data), headers=headers)
    print(response.status_code)


def init_backup(server_address, headers):
    url = "http://{}/rest/api/initialization/".format(server_address)
    response = requests.request("GET", url, headers=headers)
    print(response)
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
        print("\nSend data:")
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
