import os
import requests
import json
import utils

config = utils.get_config("client.conf")
domain = config['AUTH']['domain']
token = config['AUTH']['token']
headers = {'Content-Type': 'application/json;', 'Authorization': token}
path = "/home/locvu/openvpn-ca"


def main():
    init = init_backup()
    if init.status_code == 200:
        json_data = json.loads(init.text)
        print(json_data)
        if json_data['status'] == "ok":
            print("available to backup")
            backup_id = json_data['backup_id']
            send_metadata(path, backup_id)

        elif json_data['status'] == "full_disk":
            print("ERROR: full disk")
        else:
            print("other")
    elif init.status_code == 401:
        print("ERROR authentication")
    else:
        print("fail")
        print(init.status_code)


def init_backup():
    url = "http://{}/rest/api/initialization".format(domain)
    response = requests.request("GET", url, headers=headers)
    return response


def send_metadata(path, backup_id):
    print(path)
    tree = utils.FileDir(path)
    url = "http://{}/rest/api/metadata".format(domain)
    payload = tree.get_metadata()
    payload["backup_id"] = backup_id
    data = str(payload).replace("'", '"')
    print(data)
    response = requests.request("POST", url, data=data, headers=headers)
    print(response.status_code)
    if os.path.isdir(path):
        for x in os.listdir(path):
            send_metadata(os.path.join(path, x), backup_id)
    return


def send_data(path, block_index):
    pass


if __name__ == "__main__":
    main()
