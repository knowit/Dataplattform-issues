import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
from poller_util import PollerUtil

KNOWITLABS_TYPE = "KnowitlabsType"


def poll():
    """
    This method gets run every day and should fetch data from the website and compare it to a
    database in order to avoid duplicates.
    :return: True if everything was successful.
    """
    # Should actually be called most_recent here in blog_poller.
    last_inserted_doc = PollerUtil.fetch_last_inserted_doc(KNOWITLABS_TYPE)

    html = get_html_from_blog()
    medium_data = get_medium_data_dict(html)
    docs = create_docs(medium_data)

    most_recent = docs[0]["id"]
    for doc in docs:
        if should_upload_ingest(doc, last_inserted_doc):
            PollerUtil.post_to_ingest_api(doc, KNOWITLABS_TYPE)
        else:
            break
    if last_inserted_doc != most_recent:
        PollerUtil.upload_last_inserted_doc(most_recent, KNOWITLABS_TYPE)
    return True


def should_upload_ingest(doc, last_inserted_doc):
    """
    :param doc: The current document.
    :param last_inserted_doc: The document to compare to.
    :return: True if the id for the current document is not the same as the last_inserted_doc.
    """
    return not doc["id"] == last_inserted_doc


def create_docs(data):
    """
    :param data: The data from a medium website.
    :return: A list containing some information about each post on the website.
    """

    docs = []
    for post in data["posts"]:
        doc = {
            "id": post["id"],
            "title": post["title"],
            "subtitle": post["virtuals"]["subtitle"],
            # Created is a timestamp with milliseconds accuracy, which is a bit redundant for our
            # use.
            "created": int(post["createdAt"] / 1000)
        }
        creator_id = post["creatorId"]

        doc["author"] = data["references"]["User"][creator_id]["name"]
        docs.append(doc)

    return docs


def get_html_from_blog():
    """
    This method requests the knowitlabs website and returns the data.
    :return: The raw html data fetched from knowitlabs.
    """
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.142 Safari/537.36"
    }
    request = urllib.request.Request("https://knowitlabs.no/latest", headers=headers)
    response = urllib.request.urlopen(request).read().decode()
    return urllib.parse.unquote(response)


def get_medium_data_dict(html):
    """
    This method takes in raw html data and finds the hidden dictionary in the javascript of the
    website.
    :param html: The raw html data.
    :return: medium_data formatted as a nice dictionary.
    """
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")

    starts_with = """// <![CDATA[\nwindow["obvInit"]("""

    ends_with = """)\n// ]]>"""

    for script in scripts:
        if script.startswith(starts_with) and script.endswith(ends_with):
            script = script[len(starts_with):-len(ends_with):]
            return json.loads(script)
    return None
