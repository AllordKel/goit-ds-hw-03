import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

all_quotes_data = []
all_authors_data = []
url = "https://quotes.toscrape.com"

for page in range(1,11):
    page_url = f"{url}/page/{page}/"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    tags = soup.find_all("div", class_="tags")

    for i in range(len(quotes)):

        #gathering data for qoutes file.

        clean_quote_tags = []
        tagsforquotes = tags[i].find_all('a', class_='tag')
        for tagforquote in tagsforquotes:
            clean_quote_tags.append(tagforquote.text)

        quotes_data = {
        "tags": clean_quote_tags,
        "author": authors[i].text,
        "quote": quotes[i].text
        }

        all_quotes_data.append(quotes_data)
        
        # gathering data for authors file

        if any(authors[i].text == a["fullname"] for a in all_authors_data):
            continue # if author already exist in authors collection - skip further activities
        
        author_description_link = authors[i].find_next_sibling("a")
        author_description_url = url + author_description_link["href"]
        author_response = requests.get(author_description_url)
        author_soup = BeautifulSoup(author_response.text, "lxml")

        born_date = author_soup.find("span", attrs={"class": "author-born-date"})
        born_location = author_soup.find("span", attrs={"class": "author-born-location"})
        author_description = author_soup.find("div", attrs={"class": "author-description"})

        authors_data = {
        "fullname": authors[i].text,
        "born_date": born_date.text,
        "born_location": born_location.text,
        "description": author_description.text.replace("\n", "").strip()
        }

        all_authors_data.append(authors_data)
        
with open('qoutes.json', 'w', encoding='utf-8') as file:
    json.dump(all_quotes_data, file, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as file:
    json.dump(all_authors_data, file, ensure_ascii=False, indent=4)

#Uploading data from files to MongoDB

client = MongoClient(
    "mongodb+srv://<username>:<password>@allord.4d7ahvt.mongodb.net/?appName=Allord",
    #<username> and <password> should be replaced with yours.
    server_api=ServerApi('1')
)

db = client["goit-ds-hw-03"]
authors_collection = db["authors"]
qoutes_collection = db["qoutes"]

authors_collection.delete_many({})
qoutes_collection.delete_many({})

with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)
    authors_collection.insert_many(authors_data)

with open('qoutes.json', 'r', encoding='utf-8') as f:
    qoutes_data = json.load(f)
    qoutes_collection.insert_many(qoutes_data)