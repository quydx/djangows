import requests
from pprint import pprint
import json
if __name__ == '__main__':
    url = 'http://localhost:8000/rest/api/metadata'
    data = {'token': 'e214b58b483930a872da916fefcb8898d9546521', 'type': 'folder', 'path': '/etc/nginx'}
    header = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=header)
    res_json = response.json()
    obs = eval(str(res_json))
    pprint(obs)