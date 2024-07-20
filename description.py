import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# Load the job data from the JSON file
with open('jobData.json', 'r', encoding='utf-8') as file:
    jobData = json.load(file)

# Iterate over the job data with tqdm progress bar
for jobID, jobDetails in tqdm(jobData.items(), desc="Processing Jobs"):
    if jobDetails.get("isParsed") == False:
        url = f"https://www.dice.com/job-detail/{jobID}"
        response = requests.get(url)

        if response.status_code == 200:
            htmlContent = response.text
        else:
            print(f"Failed to retrieve the webpage. For: {url}, Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(htmlContent, 'html.parser')
        scriptTag = soup.select('script#__NEXT_DATA__')[0].text
        data = json.loads(scriptTag)

        jobDescription = data["props"]["pageProps"]["initialState"]["api"]["queries"][f'getJobById("{jobID}")']["data"]["description"]
        jobDescription = "\n".join(jobDescription.split("<br />")).replace("<strong>",'').replace("</strong>",'')

        jobDetails["description"] = jobDescription
        jobDetails["isApplied"] = False
        jobDetails["isParsed"] = True

# Save the updated job data back to the JSON file
with open('jobData.json', 'w', encoding='utf-8') as file:
    json.dump(jobData, file, ensure_ascii=False, indent=4)

print("Job data updated successfully.")
