# import requests
# from bs4 import BeautifulSoup
# from time import sleep

# jobKeyWords = ['DevOps', 'Azure devops', 'azure data']
# exampleElements = []

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# for jobKeyWord in jobKeyWords:
#     formatted_keyword = jobKeyWord.replace(' ', '%20')
#     url = f"https://www.dice.com/jobs?q={formatted_keyword}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=ONE&filters.employmentType=CONTRACTS&filters.easyApply=true&language=en"
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         exampleElements.extend(soup.select('div.card.search-card'))
#     else:
#         print(f"Failed to fetch {url}")

#     sleep(4)  # Adding a delay to be respectful to the website's servers

# # Now exampleElements contains all the job card elements from the scraped pages
# print(f"Total job cards scraped: {len(exampleElements)}")


print(len(""))