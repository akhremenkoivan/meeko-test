from collections import OrderedDict
from csv import DictWriter
from time import sleep

from bs4 import BeautifulSoup
import requests


API_KEY = "488d52c6"

movies = list()
with open("imdb_most_popular_movies_dump.html") as html:
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.select("tbody")[0]
    tr_list = tbody.select("tr")
    for tr in tr_list:
        link = tr.find("a")["href"]
        imdb_id = link.split("/")[2]
        td_list = tr.select("td")
        l = list()
        for td in td_list:
            l.append(td.get_text())
        title, year, rank, *_ = td_list[1].get_text().strip().splitlines()
        year = year.strip("()")
        rating = td_list[2].get_text().strip()
        rating = rating if rating else None
        imdb_parsed_data = {"imdbID": imdb_id, "Title": title, "Year": year, "imdbRating": rating}
        imdb_api_data = requests.get(f'https://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}').json()
        sleep(0.8)
        imdb_data = {**imdb_parsed_data, **imdb_api_data}
        movies.append(imdb_data)

with open('movies.csv', 'w', encoding="utf-8", newline='') as csvfile:
    fieldnames = movies[0].keys()
    writer = DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(movies)

