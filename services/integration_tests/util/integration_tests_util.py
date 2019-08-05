import json
import os
import urllib.request

import pymysql


def read_serverless_output(service, stage="dev"):
    if os.getenv("TRAVIS"):
        stage = "test"
    f = open(f"{service}.serverless_outputs_{stage}.json")
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


class IntegrationTestUtil:
    MYSQL_CONFIG = read_serverless_output("structured_mysql")
    __connection = None

    @staticmethod
    def get_mysql_cursor():
        if not IntegrationTestUtil.__connection:
            IntegrationTestUtil.__connection = pymysql.connect(
                host=IntegrationTestUtil.MYSQL_CONFIG["auroraClusterROEndpoint"],
                port=int(IntegrationTestUtil.MYSQL_CONFIG["auroraDBPort"]),
                user=IntegrationTestUtil.MYSQL_CONFIG["auroraDBUser"],
                password=IntegrationTestUtil.MYSQL_CONFIG["auroraDBPassword"],
                db=IntegrationTestUtil.MYSQL_CONFIG["auroraDBName"],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
        return IntegrationTestUtil.__connection
