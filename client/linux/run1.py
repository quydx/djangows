import requests
import json
import utils


def main():
    config = utils.get_config("client1.conf")
    domain = config['AUTH']['domain']
    token = config['AUTH']['token']
    url = "http://{}/rest/api/initalization".format(domain)
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        print(json_data)
        if json_data['status'] == "ok":
            print("available to backup")
        elif json_data['status'] == "full_disk":
            print("ERROR: full disk")
        else:
            print("other")
    elif response.status_code == 401:
        print("ERROR authentication")
    else:
        print(response.status_code)


if __name__ == "__main__":
    main()
