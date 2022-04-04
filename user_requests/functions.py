import re
import datetime

import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent": "Mozilla/5.0", 'Accept-Language': 'en-US, en;q=0.5'}


class IMDBMovieData:
    def __init__(self, imdb_id):
        self.url = "https://www.imdb.com/title/" + str(imdb_id) + "/fullcredits"
        self.r = requests.get(self.url, headers=HEADERS)
        self.soup = BeautifulSoup(self.r.text, "html.parser")

    @property
    def imdb_get_title(self):
        title = self.soup.find("h3", {"itemprop": "name"})
        title = title.find("a")
        title = title.text.strip() if title else None
        return title

    @property
    def imdb_get_directors(self):
        directors = self.soup.find("h4", {"id": "director"}).next_sibling.next_sibling
        directors = directors.findAll("a")
        directors_list = []
        for director in directors:
            director_url = director.get("href")
            director_imdb_id = re.search(r"nm[.]*[^(?:/|?)]+", director_url)[0]
            directors_list.append(director_imdb_id)
        directors_set = set()
        directors_set_add = directors_set.add
        directors_list = \
            [director for director in directors_list if not (director in directors_set or directors_set_add(director))]
        return directors_list

    @property
    def imdb_get_actors(self):
        actors = self.soup.find("h4", {"id": "cast"}).next_sibling.next_sibling
        actors = actors.findAll("a")
        actors_list = []
        for actor in actors:
            actor_url = actor.get("href")
            actor_imdb_id = re.search(r"nm[.]*[^(?:/|?)]+", actor_url)[0]
            actors_list.append(actor_imdb_id)
        actors_set = set()
        actors_set_add = actors_set.add
        actors_list = [actor for actor in actors_list if
                       not (actor in actors_set or actors_set_add(actor))]
        return actors_list

    @property
    def imdb_get_release_year(self):
        release_year = self.soup.find("h3", {"itemprop": "name"})
        release_year = release_year.find("span").text.strip()[1:-1]
        return release_year


class IMDBPeopleData:
    def __init__(self, imdb_id):
        self.url = "https://www.imdb.com/name/" + str(imdb_id) + "/bio"
        self.r = requests.get(self.url, headers=HEADERS)
        self.soup = BeautifulSoup(self.r.text, "html.parser")

    @property
    def imdb_get_first_name(self):
        first_name = self.soup.find("h3")
        first_name = first_name.text.split()[0] if first_name else ""
        return first_name

    @property
    def imdb_get_last_name(self):
        last_name = self.soup.find("h3")
        last_name = last_name.text.split()[1:] if last_name else ""
        last_name = " ".join(last_name)
        return last_name

    @property
    def imdb_get_birth_date(self):
        birth_date = self.soup.find("time")
        birth_date = birth_date.get("datetime")
        birth_date = datetime.datetime.strptime(birth_date,
                                                "%Y-%m-%d").date() if birth_date else None
        return birth_date

    @property
    def imdb_get_death_date(self):
        dates = self.soup.findAll("td", {"class": "label"})
        for date in dates:
            if date.text == "Died":
                death_date = date.next_sibling.next_sibling.find("time")
                death_date = death_date.get("datetime") if death_date else ""
                death_date = datetime.datetime.strptime(death_date,
                                                        "%Y-%m-%d").date() if death_date else None
                return death_date
        death_date = None
        return death_date
