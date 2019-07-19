import json
import urllib.request


def read_serverless_output(service):
    f = open(f"{service}.serverless_outputs.json")
    data = json.loads(f.read())
    f.close()
    return data


def post_to_api(body, url, apikey=None) -> (int, str):
    data = body.encode("ascii")
    headers = {"x-api-key": apikey} if apikey else {}
    try:
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        return response.getcode(), response.read().decode()
    except urllib.request.HTTPError:
        return 500, None
