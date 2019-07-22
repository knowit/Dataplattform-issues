import urllib.request
import json
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    html = get_html_from_blog()
    medium_data = get_medium_data_dict(html)
    docs = create_docs(medium_data)
    print(json.dumps(docs))
    return True


def create_docs(data):
    docs = []
    for post in data["posts"]:
        doc = {
            "title": post["title"],
            "subtitle": post["virtuals"]["subtitle"],
            "created": post["createdAt"]
        }
        creator_id = post["creatorId"]

        # TODO: Figure out if this is inefficient.
        doc["author"] = data["references"]["User"][creator_id]["name"]
        docs.append(doc)

    return docs


def get_html_from_blog():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }
    request = urllib.request.Request("https://knowitlabs.no/latest", headers=headers)
    response = urllib.request.urlopen(request)

    return response.read().decode()


def get_medium_data_dict(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")
    script = scripts[8].text

    starts_with = """// <![CDATA[\nwindow["obvInit"]("""

    ends_with = """)\n// ]]>"""

    if script.startswith(starts_with) and script.endswith(ends_with):
        script = script[len(starts_with):-len(ends_with):]
    return json.loads(script)


lambda_handler(None, None)
