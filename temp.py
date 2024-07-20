import requests
from bs4 import BeautifulSoup
import json

def print_keys_tree(data, indent=0):
    indent_str = '  ' * indent
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indent_str}{key}")
            print_keys_tree(value, indent + 1)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{indent_str}[{i}]")
            print_keys_tree(item, indent + 1)

url = "https://www.dice.com/job-detail/e1322a6c-4ac4-4e69-8b1a-f3a7c4c6b1e7"
response = requests.get(url)

if response.status_code == 200:
    htmlContent = response.text
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
    htmlContent = ""

soup = BeautifulSoup(htmlContent, 'html.parser')
scriptTag = soup.select('script#__NEXT_DATA__')[0].text
data = json.loads(scriptTag)


print(data["props"]["pageProps"]["initialState"]["api"]["queries"]['getJobById("e1322a6c-4ac4-4e69-8b1a-f3a7c4c6b1e7")']["data"]["description"])
# print_keys_tree(data["props"]["pageProps"]["initialState"]["api"]["queries"]['getJobById("e1322a6c-4ac4-4e69-8b1a-f3a7c4c6b1e7")']['data']['description'])
