import os
import requests
import json
import utils
from utils import FileDir
import urllib.request
import logging
import stat
import subprocess
from cryptography.fernet import Fernet
import win32con
import win32api

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
handler = logging.FileHandler('restore_log.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


def main(args, repo_target, bid):
    config = utils.get_config(args.config_file)
    server_address = config['AUTH']['server_address']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    path = repo_target
    pk = bid
    block_size = int(config['FILE']['block_size'])
    key = config['CRYPTO']['key']

    # start a restore
    logger.info("Start restore session")
    init = init_restore(server_address, headers, pk, path)
    if init.status_code == 200:
        # logger.debug(json.dumps(init.json(), indent=4))
        for value in init.json().values():
            wpath = utils.convert_linuxtowin_path(value['path'])

            logger.info("Restore: {}".format(wpath))
            if value['type'] == 'directory':
                # make directory recusive
                if not os.path.isdir(wpath):
                    os.makedirs(path, exist_ok=True)   
                    logger.debug("Directory {} created".format(wpath))

                # add attributes
                add_attribute(wpath, value['attr'])    
                logger.info("DONE: {} restore done".format(wpath))
            elif value['type'] == 'file':
                if not os.path.isfile(wpath):

                    # touch empty file 
                    basedir = os.path.dirname(wpath)
                    if not os.path.exists(basedir):
                        os.makedirs(basedir, exist_ok=True) 
                    print("wpath: ",wpath)
                    open(wpath, 'wb')
                    logger.debug("Empty file {} created".format(wpath))

                # compare checksum list 
                f = utils.FileDir(wpath, block_size)
                checksum_list = f.list_checksum()
                need_data = {"need": need_blocks(value['checksum'], checksum_list), \
                            "path": value['path']}
                need_data_json = str(need_data).replace("'", '"')  # convert to json format
                url = "http://{}/rest/api/download_data/{}/".format(server_address, pk)
                
                logger.debug("Get data {} - {}".format(wpath, value['checksum']))
                response = requests.request("GET", url, data=need_data_json, headers=headers)
                
                response_json = response.json()
                logger.debug("Download")
                logger.debug(response_json['url'])
                logger.debug("Existed")
                logger.debug(existed_blocks(value['checksum'], checksum_list))

                file_read = open(wpath, 'rb')
                print("checksum:", value['checksum'])
                data_existed = list(utils.read_in_blocks(file_read, \
                            list_block_id_existed(value['checksum'], checksum_list), block_size))
                print("data_existed: ", data_existed)
                data_need = list(get_data(server_address, response_json['url']))
                print("data_need: ", data_need)
                         
                data = data_existed + data_need  # list tuple [(data, block_id), (), ()]

                print("data: ", data)
                data_sorted = sorted(data, key=lambda x: x[1])

                attrs = win32api.GetFileAttributes(wpath)
                if (attrs & win32con.FILE_ATTRIBUTE_READONLY) != 0:
                    os.chmod(wpath, stat.S_IWRITE) # file read only 
                if (attrs & win32con.FILE_ATTRIBUTE_HIDDEN) != 0:
                    subprocess.check_call(["attrib","-H",wpath]) # file hidden

                if data_need != []:
                    # write to file 
                    join_file(wpath, data_sorted, key)

                    # add attributes
                    add_attribute(wpath, value['attr'])    
                    logger.info("DONE: {} restore done".format(wpath))
                else:
                    add_attribute(wpath, value['attr'])
                    logger.info("DONE: {} not change".format(wpath))

            elif value['type'] == 'symlink':
                logger.info("PASS: Restore link: {} pass".format(wpath))
    else:
        logger.warn("{} - {}".format(init.text, str(init.status_code)))

    result_restore = {"job_id": args.job_id, "status_code": init.status_code,
                      "backup_id": pk, "path": wpath}
    print(result_restore)

    # Send restore result to Controller
    ctl_address = config['CONTROLLER']['address']
    url_result = "http://{}/api/result-restore/".format(ctl_address)
    response = requests.request("POST", url_result, data=json.dumps(result_restore), headers=headers)
    logger.debug("Send result to Controller: " + str(response.status_code))
    #print(response.text)


def init_restore(server_address, headers, pk, path):
    url = "http://{}/rest/api/restore/{}".format(server_address, pk)
    lpath = utils.convert_wintolinux_path(path)
    query = {"path": lpath}
    response = requests.request("GET", url, headers=headers, params=query)
    return response


def add_attribute(path, attr):
    """
    - Addition permitions, owner, group, time
    - Set access list 
    """
    os.chmod(path, int(attr['mode']))
    #os.chown(path, int(attr['uid']), int(attr['gid'])) 
    subprocess.call(['icacls.exe', path, '/setowner', attr['uname']])
    os.utime(path,(float(attr['create_time']), float(attr['modify_time'])))
    #utils.set_acl(path, ast.literal_eval(attr['acl']))
    utils.set_acl(path, attr['acl'])

    attrs = win32api.GetFileAttributes(path)
    if (attrs & win32con.FILE_ATTRIBUTE_HIDDEN) != 0 and attr['hidden'] == 0:
        subprocess.check_call(["attrib","-H",path])
    if (attrs & win32con.FILE_ATTRIBUTE_HIDDEN) == 0 and attr['hidden'] != 0:    
        subprocess.check_call(["attrib","+H",path])

def list_block_id_existed(list_pre, list_now):
    addition_checksum = list(set(list_now) & set(list_pre))
    addition_pos = [list_now.index(i) for i in addition_checksum]
    return addition_pos


def need_blocks(list_pre, list_now):
    """
    The block is not available in the current pk
    return: dict  
    """
    addition_checksum = list(set(list_pre) - set(list_now))
    addition_pos = [str(list_pre.index(i)) for i in addition_checksum]
    addtion = dict(zip(addition_pos, addition_checksum))
    return addtion


def existed_blocks(list_pre, list_now):
    """
    The block existed in the current pk
    return: dict with position of previous verison  
    """
    existed_checksum = list(set(list_now) & set(list_pre))
    exitsed_pos = [str(list_pre.index(i)) for i in existed_checksum]
    existed = dict(zip(exitsed_pos, existed_checksum))
    return existed


def get_data(server_address, url_dict):
    base_url = "http://{}".format(server_address)
    for block_id, url in url_dict.items():
        response = urllib.request.urlopen(base_url + url)
        data = response.read()
        yield (data, int(block_id))


def join_file(path, data_chunks, key):
    os.chmod( path, stat.S_IWRITE) # file read only 
#    subprocess.check_call(["attrib","-H",path]) # file hidden

    cipher_suite = Fernet(key)

    file_write = open(path, 'wb')
    print('data_chunks: ', data_chunks)
    for chunk in data_chunks:
        file_write.write(cipher_suite.decrypt(chunk[0]))
    file_write.close()
