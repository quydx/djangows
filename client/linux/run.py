import os
import requests
import json
import utils

config = utils.get_config("client.conf")
domain = config['AUTH']['domain']
token = config['AUTH']['token']
headers = {'Content-Type': 'application/json;', 'Authorization': token}
path = "/home/locvu"


def main():
    init = init_backup()
    if init.status_code == 200:
        json_data = json.loads(init.text)
        print(json_data)
        if json_data['status'] == "ok":
            print("available to backup")
            send_metadata(path)

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


def send_metadata(path):
    tree = utils.FileDir(path)
    url = "http://{}/rest/api/metadata".format(domain)
    payload = tree.get_metadata()
    print(payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)
    if os.path.isdir(path):
        send_metadata((os.path.join(path, x)) for x in os.listdir(path))
    return


if __name__ == "__main__":
    main()
