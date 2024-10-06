from bs4 import BeautifulSoup
import requests
import re
import json


def check_category_page(link, processed_anecdotes, counter, global_url):
    category_response = requests.get(link)
    category_html = category_response.text
    category_soup = BeautifulSoup(category_html, 'html.parser')
    category_element = category_soup.find("ul", {"class": "list list_big"})
    category_links = category_element.find_all('a')
    for link_to_anecdote in category_links:
        anecdote_link = global_url+link_to_anecdote['href']
        anecdote_response = requests.get(anecdote_link)
        anecdote_html = anecdote_response.text
        anecdote_soup = BeautifulSoup(anecdote_html, 'html.parser')
        content = anecdote_soup.find("div", {"class": "content"})
        text = content.find('div', {'itemprop': 'articleBody'})
        paragraphs = text.find_all('p')
        clean_text = ""
        for paragraph in paragraphs:
            if "Sent by" in paragraph.text or "sent by" in paragraph.text:
                continue
            else:
                clean_text += paragraph.text + '\n'
        clean_text = re.sub(" +", " ", clean_text)
        processed_anecdotes.append({
            "id": counter,
            "text": clean_text
        })
        counter += 1
    category_next_page = category_soup.find("ul", {"role": "navigation"})
    if category_next_page is not None:
        next_button = category_next_page.find("li", {'class': 'pager__item pager__item_next'})
        if next_button is not None:
            next_link = next_button.find('a')
            if next_link is not None:
                processed_anecdotes, counter = check_category_page(global_url+next_link['href'], processed_anecdotes, counter, global_url)
    return processed_anecdotes, counter


url = 'https://www.native-english.ru/jokes'
global_url = 'https://www.native-english.ru'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
element = soup.find("div", {"class": "stack__secondary"})
links = element.find_all('a')
processed_anecdotes = []
counter = 0
for link in links:
    category_link = global_url+link['href']
    processed_anecdotes, counter = check_category_page(category_link, processed_anecdotes, counter, global_url)

with open("native-english.json", 'w') as file:
    json.dump(processed_anecdotes, file)
