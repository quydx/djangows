import os
import requests
import json
import utils
import urllib.request
import ast 


def main(args):
    config = utils.get_config(args.config_file)
    domain = config['AUTH']['domain']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    path = args.repo_target
    version = args.version

    init = init_restore(domain, headers, version, path)

    if init.status_code == 200:
        print(json.dumps(init.json(), indent=4))
        for key, value in init.json().items():
            if value['type'] == 'directory':
                if not os.path.isdir(value['path']):
                    os.makedirs(path, exist_ok=True)    # make directory recusive 

                # add attributes
                add_attribute(value['path'], value['attr'])    

            elif value['type'] == 'file':
                if not os.path.isfile(value['path']):
                    basedir = os.path.dirname(value['path'])
                    if not os.path.exists(basedir):
                        os.makedirs(basedir, exist_ok=True) 
                    os.mknod(value['path'])     # touch empty file 

                # compare checksum list 
                f = utils.FileDir(value['path'])
                checksum_list = f.list_checksum()
                need_data = {"need": need_blocks(value['checksum'], checksum_list), "path": value['path']}
                need_data_json = str(need_data).replace("'", '"')
                url = "http://{}/rest/api/download_data/{}/".format(domain, version)
                response = requests.request("GET", url, data=need_data_json, headers=headers)
                print(response.status_code)
                
                response_json = response.json()
                print("Need : ")
                print(response_json['url'])
                print("Existed :")
                print(existed_blocks(value['checksum'], checksum_list))

                file_read = open(value['path'], 'rb')
                print(list_block_id_existed(value['checksum'], checksum_list))
                data_existed = list(utils.read_in_blocks(file_read, list_block_id_existed(value['checksum'], checksum_list)))
                
                # print(data_existed)
                data_need = list(get_data(domain, response_json['url']))
                # print(data_need)
                
                data = data_existed + data_need  # list tuple [(data, block_id), (), ()]
                data_sorted = sorted(data, key=lambda x: x[1])

                # write to file 
                join_file(value['path'], data_sorted)

                # add attributes
                add_attribute(value['path'], value['attr'])    
                print("Done : {}".format(value['path']))
            elif value['type'] == 'symlink':
                pass
    else:
        print("{} - {}".format(init.text, str(init.status_code)))


def init_restore(domain, headers, version, path):
    url = "http://{}/rest/api/restore/{}".format(domain, version)
    query = {"path": path}
    response = requests.request("GET", url, headers=headers, params=query)
    return response

# {'access_time': 1526784106.4107292, 'mode': 33279, 
# 'create_time': 1525974482.3170633, 'modify_time': 1525974482.3130634, 'uid': 1000, 'gid': 1000}

def add_attribute(path, attr):
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
    # diff_list = {}
    addition_checksum = list(set(list_pre) - set(list_now))
    addition_pos = [str(list_pre.index(i)) for i in addition_checksum]
    addtion = dict(zip(addition_pos, addition_checksum))
    # diff_list = {"addition": addtion, "existed": existed}
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


def download_data(domain, path, url_list):
    base_url = "http://{}".format(domain)
    for url in url_list:
        urllib.request.urlretrieve(base_url + url,  '/' + url.split('/', 3)[3])


def get_data(domain, url_dict):
    base_url = "http://{}".format(domain)
    for block_id, url in url_dict.items():
        response = urllib.request.urlopen(base_url + url)
        data = response.read()
        yield (data, int(block_id))


def join_file(path, data_chunks):
    file_write = open(path, 'wb')
    for chunk in data_chunks:
        file_write.write(chunk[0])
    file_write.close()