import requests
import json
import utils


def main():
    config = utils.get_config("client.conf")
    domain = config['AUTH']['domain']
    token = config['AUTH']['token']
    url = "http://{}/rest/api/initalization".format(domain)
    headers = {'Content-Type': 'application/json;', 'Authorization': token}
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    if json_data['status'] == "ok":
        print("available to backup")
    elif json_data['status'] == "full_disk":
        print("ERROR: full disk")
    else:
        print("other")


if __name__ == "__main__":
    main()
