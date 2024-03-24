import json
import os
import re
from bs4 import BeautifulSoup
import requests
from weasyprint import HTML
from concurrent.futures import ThreadPoolExecutor

def get_html(endpoint):
    response = requests.get(endpoint, headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    })
    if response.status_code == 200:
        return response.text
    else:
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}


def get_and_store_page(link):
    pattern = r'https://www\.visualcapitalist\.com/([a-zA-Z0-9\-]+)/'
    match = re.match(pattern, link)
    if match:
        filename =  './pdfs/'+match.group(1)+'.pdf'

        html_content = get_html(link)
        soup = BeautifulSoup(html_content, features="html.parser")
        target_html1 = ''
        for p in soup.find('span', class_='mvp-post-excerpt').find_all('p'):
            img = p.find('img')
            if img and img.get('src'):
                img_link = img['src']
                if "e-icon-black.png" not in img_link and "voronoi-icon-transparent.png" not in img_link:
                    target_html1 = "<img src=\""+img_link+"\" style=\"width:100%\"/>"
                    break

        target_html2 = str(soup.find('div', id='mvp-content-body-top'))

        pdf_file_path = os.path.join(os.getcwd(), filename)
        HTML(string=target_html1+target_html2).write_pdf(pdf_file_path)
    print('done', link)


with open('links.json', 'r') as openfile:
    link_list = json.load(openfile)

with ThreadPoolExecutor(max_workers=10) as exe:
    for ind, link in enumerate(link_list):
        exe.submit(get_and_store_page, link)