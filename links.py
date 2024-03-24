import requests
from bs4 import BeautifulSoup
import re
import json

def get_html(endpoint):
    response = requests.get(endpoint, headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    })
    if response.status_code == 200:
        return response.text
    else:
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}

def get_page(page):

    SEARCH_URL = f"https://www.visualcapitalist.com/page/{page}/"
    pattern = r'https://www\.visualcapitalist\.com/[a-zA-Z0-9\-]+/'
    
    req = get_html(SEARCH_URL)

    linkset = set()
    if type(req) == str:
        soup = BeautifulSoup(req, features="html.parser")
        lis = soup.find_all('li', class_="mvp-blog-story-wrap")
        for li in lis:
            links = li.find_all('a')
            for link in links:
                if link.has_attr('href') and link['href'].count('/') == 4 and re.match(pattern, link['href']):
                    linkset.add(link['href'])
        return linkset
    else:
        return req

linkset = set()
for i in range(1, 100):
    page_links = get_page(i)
    for link in list(page_links):
        linkset.add(link)
    print(i, len(linkset))

with open("links.json", "w") as outfile:
    json_object = json.dumps(list(linkset))
    outfile.write(json_object)