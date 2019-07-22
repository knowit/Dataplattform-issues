import urllib.request
import json
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
request = urllib.request.Request("https://knowitlabs.no/latest", headers=headers)
response = urllib.request.urlopen(request)
res = response.read().decode()

soup = BeautifulSoup(res, "html.parser")
scripts = soup.find_all("script")
script = scripts[8].text
starts_with = """// <![CDATA[
window["obvInit"]("""
ends_with = """)
// ]]>"""
if script.startswith(starts_with) and script.endswith(ends_with):
    script = script[len(starts_with):-len(ends_with):]
print(script)
json = json.loads(script)

print(json)