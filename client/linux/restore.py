import os
import requests
import json
import utils


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
                checksum_diff = compare_checksum(value['checksum'], checksum_list)
                print(checksum_list)
                print(value['checksum'])
                print(checksum_diff)
                data = str(checksum_diff).replace("'", '"')
                url = "http://{}/rest/api/download_data/{}/".format(domain, version)
                response = requests.request("POST", url, data=data, headers=headers)
                print(response.status_code)

                # add attributes
                add_attribute(value['path'], value['attr'])    

            elif value['type'] == 'symlink':
                pass


    else:
        print("{} - {}".format(init.text, str(init.status_code)))

def init_restore(domain, headers, version, path):
    url = "http://{}/rest/api/restore/{}".format(domain, version)
    query = {"path": path}
    response = requests.request("GET", url, headers=headers, params=query)
    return response

# {'access_time': 1526784106.4107292, 'nlink': 1, 'inode': 6031529, 'device': 2050, 'mode': 33279, 
# 'create_time': 1525974482.3170633, 'size': 8416, 'modify_time': 1525974482.3130634, 'uid': 1000, 'gid': 1000}

def add_attribute(path, attr):
    os.chown(path, int(attr['uid']), int(attr['gid']))
    os.chmod(path, int(attr['mode']))
    os.utime(path,(float(attr['create_time']), float(attr['modify_time'])))


def compare_checksum(list_old, list_new):
    diff_list = {}
    addition_checksum = list(set(list_old) - set(list_new))
    addition_pos = [str(list_old.index(i)) for i in addition_checksum]
    addtion = dict(zip(addition_pos, addition_checksum))
    # addtion = sorted(list(zip(addition_checksum, addition_pos)), key=lambda x: x[1])

    deletion_checksum = list(set(list_new) - set(list_old))
    deletion_pos = [str(list_new.index(i)) for i in deletion_checksum] 
    deletion = dict(zip(deletion_pos, deletion_checksum))
    # deletion = sorted(list(zip(deletion_checksum, deletion_pos)), key=lambda x: x[1])
    diff_list = {"addition": addtion, "deletion": deletion}
    
    return diff_list
