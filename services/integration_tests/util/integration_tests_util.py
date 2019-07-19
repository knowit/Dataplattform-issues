import json
import urllib.request


def read_serverless_output(service):
    f = open(f"{service}.serverless_outputs.json")
    data = json.loads(f.read())
    f.close()
    return data


def get_from_api(url, apikey=None) -> (int, str):
    return post_to_api(None, url, apikey)


def post_to_api(body, url, apikey=None) -> (int, str):
    data = None if body is None else body.encode("ascii")
    headers = {"x-api-key": apikey} if apikey else {}
    try:
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        return response.getcode(), json.loads(response.read().decode())
    except urllib.request.HTTPError:
        return 500, None
