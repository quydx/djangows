import os
import stat
import requests
import json
import utils
import urllib.request
import ast 
import logging

from cryptography.fernet import Fernet


utils.setup_logging()
logger = logging.getLogger(__name__)


def main(args, error=None):
    config = utils.get_config(args.config_file)
    domain = args.server_address or config['AUTH']['server_address']
    token = config['AUTH']['token']
    key_decrypt = config['CRYPTO']['key']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    path = args.repo_target
    backup_id = args.backup_id
    block_size = int(config['FILE']['block_size'])

    # start a restore
    logger.info("Start restore session")
    init = init_restore(domain, headers, backup_id, path)
    data = {}

    if init.status_code == 200:
        # logger.debug(json.dumps(init.json(), indent=4))
        for value in init.json().values():
            logger.info("Restore: {}".format(value['path']))
            if value['type'] == 'directory':

                # make directory recusive 
                if not os.path.isdir(value['path']):
                    os.makedirs(value['path'], exist_ok=True)
                    logger.debug("Directory {} created".format(value['path']))

                # add attributes
                add_attribute(value['path'], value['attr'])
                logger.info("DONE: {} restore done".format(value['path']))
            elif value['type'] == 'file':
                if not os.path.isfile(value['path']):

                    # touch empty file 
                    basedir = os.path.dirname(value['path'])
                    if not os.path.exists(basedir):
                        os.makedirs(basedir, exist_ok=True)
                    os.mknod(value['path'])
                    logger.debug("Empty file {} created".format(value['path']))

                # compare checksum list 
                f = utils.FileDir(value['path'], block_size)
                checksum_list = f.list_checksum()
                need_data = {"need": need_blocks(value['checksum'], checksum_list), \
                            "path": value['path']}
                need_data_json = str(need_data).replace("'", '"')  # convert to json format
                url = "http://{}/rest/api/download_data/{}/".format(domain, backup_id)

                logger.debug("Get data {} - {}".format(value['path'], value['checksum']))
                response = requests.request("GET", url, data=need_data_json, headers=headers)

                response_json = response.json()
                logger.debug("Download: ")
                logger.debug(response_json['url'])
                logger.debug("Existed:")
                logger.debug(existed_blocks(value['checksum'], checksum_list))

                file_read = open(value['path'], 'rb')
                
                data_existed = list(utils.read_in_blocks(file_read, \
                            list_block_id_existed(value['checksum'], checksum_list), block_size))
                data_need = list(get_data(response_json['server_storage'], response_json['url'], key_decrypt))
           
                data = data_existed + data_need  # list tuple [(data, block_id), (), ()]
                data_sorted = sorted(data, key=lambda x: x[1])

                # write to file
                join_file(value['path'], data_sorted)

                # add attributes
                add_attribute(value['path'], value['attr'])    
                logger.info("DONE: {} restore done".format(value['path']))
            elif value['type'] == 'symlink':
                logger.info("PASS: Restore link: {} pass".format(value['path']))
    else:
        logger.error("{} - {}".format(init.text, str(init.status_code)))

    result_restore = {"job_id": args.job_id, "status_code": init.status_code,
                      "backup_id": args.backup_id, "path": path}

    # Send restore result to Controller
    ctl_address = config['CONTROLLER']['address']
    url_result = "http://{}/api/result-restore/".format(ctl_address)
    response = requests.request("POST", url_result, data=json.dumps(result_restore), headers=headers)
    logger.debug("Send result to Controller: " + str(response.status_code))


def init_restore(domain, headers, backup_id, path):
    url = "http://{}/rest/api/restore/{}".format(domain, backup_id)
    query = {"path": path}
    response = requests.request("GET", url, headers=headers, params=query)
    return response


def add_attribute(path, attr):
    """
    - Addition permitions, owner, group, time
    - Set access list 
    """
    os.chown(path, int(attr['uid']), int(attr['gid']))
    os.chmod(path, int(attr['mode']))
    os.utime(path,(float(attr['create_time']), float(attr['modify_time'])))
    utils.set_acl(path, ast.literal_eval(attr['acl']))


def list_block_id_existed(list_pre, list_now):
    addition_checksum = list(set(list_now) & set(list_pre))
    addition_pos = [list_now.index(i) for i in addition_checksum]
    return addition_pos


def need_blocks(list_pre, list_now):
    """
    The block is not available in the current version
    return: dict  
    """
    addition_checksum = list(set(list_pre) - set(list_now))
    addition_pos = [str(list_pre.index(i)) for i in addition_checksum]
    addtion = dict(zip(addition_pos, addition_checksum))
    return addtion


def existed_blocks(list_pre, list_now):
    """
    The block existed in the current version
    return: dict with position of previous verison  
    """
    existed_checksum = list(set(list_now) & set(list_pre))
    exitsed_pos = [str(list_pre.index(i)) for i in existed_checksum]
    existed = dict(zip(exitsed_pos, existed_checksum))
    return existed


def get_data(domain, url_dict, key):
    '''Download data from domain'''
    base_url = "http://{}".format(domain)
    cipher_suite = Fernet(key)
    
    for block_id, url in url_dict.items():
        response = urllib.request.urlopen(base_url + url)
        data_cypher = response.read()
        data_plain = cipher_suite.decrypt(data_cypher)
        yield (data_plain, int(block_id))


def join_file(path, data_chunks):
    if os.path.exists(path) and not os.access(path, os.W_OK):  # file read only
        os.chmod(path, stat.S_IWRITE)  # Write by owner

    file_write = open(path, 'wb')
    for chunk in data_chunks:
        file_write.write(chunk[0])
    file_write.close()
