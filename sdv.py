import requests
from bs4 import BeautifulSoup

# Fetch the webpage
url = "https://www.dice.com/jobs?q=DevOps&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&language=en&jobSavedSearchId=a35866ec-a689-44de-8b57-29d44ca98f74"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)


# Save the parsed content to a text file
with open('pageContent.txt', 'w', encoding='utf-8') as file:
    file.write(str(soup))
# Example of extracting data
exampleElements = soup.select('div.card.search-card')

# Print the text of each element found
for exampleElement in exampleElements:
    print(exampleElement.text)