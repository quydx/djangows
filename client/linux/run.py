import os
import requests
import json
import utils

# config = utils.get_config("client.conf")

def main(args):
    config = utils.get_config(args.config_file)
    domain = config['AUTH']['domain']
    token = config['AUTH']['token']
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    # path = "/home/locvu/openvpn-ca"
    path = args.repo_target
    init = init_backup(domain, headers)

    if init.status_code == 200:
        json_data = json.loads(init.text)
        print(json_data)
        if json_data['status'] == "ok":
            print("available to backup")
            backup_id = json_data['backup_id']
            send_metadata(domain, headers, path, backup_id)

        elif json_data['status'] == "full_disk":
            print("ERROR: full disk")
        else:
            print("other")
    elif init.status_code == 401:
        print("ERROR authentication")
    else:
        print("fail")
        print(init.status_code)


def init_backup(domain, headers):
    url = "http://{}/rest/api/initialization/".format(domain)
    response = requests.request("GET", url, headers=headers)
    return response


def send_metadata(domain, headers, path, backup_id):
    tree = utils.FileDir(path)
    url = "http://{}/rest/api/metadata/".format(domain)
    payload = tree.get_metadata()
    payload["backup_id"] = backup_id
    data = str(payload).replace("'", '"')
    print('SEND METADATA: ')
    print(data)
    response = requests.request("POST", url, data=data, headers=headers)
    print('RECEIVED: ')
    print(response.json())
    response_data = response.json()
    if 'blocks' in response_data:
        send_data(domain, headers, path, response_data['blocks'], response_data['file_object'], response_data['checksum'])

    if os.path.isdir(path):
        for x in os.listdir(path):
            send_metadata(domain, headers, os.path.join(path, x), backup_id)
    return


def send_data(domain, headers, path, blocks, file_object, checksum):
    url = "http://{}/rest/api/upload/data/".format(domain)
    fin = open(path, 'rb')
    count = 0
    for chunk, block_id in utils.read_in_blocks(fin, utils.block_size, blocks):
        files = {'block_data': chunk}
        values = {'block_id' : block_id, 'file_object': file_object, 'checksum': checksum[count]}
        print("-- SEND DATA:")
        print(checksum[count])
        count += 1
        response = requests.post(url, files=files, data=values)
        print('-- RESPONSE: ')
        print(response.text)

# if __name__ == "__main__":
#     main(args)



