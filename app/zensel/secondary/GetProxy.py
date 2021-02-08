import requests
import json

class GetProxy:

    def get_list():

        url = 'https://proxybroker.craft-group.xyz/'
        response = requests.get(url)
        if response.status_code == 200:
            res = json.loads(response.text)

            return res
    
        return None