import requests
from bs4 import BeautifulSoup
import json

def getJobDescription(jobID):
    url = f"https://www.dice.com/job-detail/{jobID}"
    response = requests.get(url)

    if response.status_code == 200:
        htmlContent = response.text
    else:
        print(f"Failed to retrieve the webpage. For: {url}, Status code: {response.status_code}")
        return 0

    soup = BeautifulSoup(htmlContent, 'html.parser')
    scriptTag = soup.select('script#__NEXT_DATA__')[0].text
    data = json.loads(scriptTag)

    jobDescription = data["props"]["pageProps"]["initialState"]["api"]["queries"][f'getJobById("{jobID}")']["data"]["description"]
    jobDescription = BeautifulSoup(jobDescription, 'html.parser').get_text()
    return jobDescription
