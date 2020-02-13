import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from utils.request_helper import create_html_bs
import utils.scrape_helpers as scrape_helpers
from urllib.parse import urlencode

class IMBDTopScraper(object):

	def __init__(self, **kwargs):
		CONST_MAX_LIMIT = 1000

		self.offset = kwargs.get('offset', 0) + 1
		if(self.offset < 1):
			self.offset = 1

		self.limit = kwargs.get('limit',100) + 1
		if(self.limit > 1000):
			self.limit = CONST_MAX_LIMIT + 1

		self.count_per_page = kwargs.get('count_per_page', 100)
		if(self.count_per_page > 250):
			self.count_per_page = 250

		self.file_name = kwargs.get('file_name', 'data.json')
		if('.json' is not self.file_name[-4:]):
			self.file_nane = self.file_name + '.json'

		self.counter = 0
		self.current_dict = defaultdict(lambda: list())

	def get_movie_aspects(self, movie_bs, movie_url):
		return {
			'cast': scrape_helpers.get_movie_cast(movie_bs, movie_url),
			'rating': scrape_helpers.get_movie_rating(movie_bs),
			'full_date': scrape_helpers.get_movie_date(movie_bs),
			'discretion': scrape_helpers.get_movie_discretion(movie_bs),
			'languages': scrape_helpers.get_movie_languages(movie_bs),
			'production_company': scrape_helpers.get_movie_production_company(movie_bs),
			'length': scrape_helpers.get_movie_length(movie_bs),
			'genres': scrape_helpers.get_movie_genre(movie_bs),
			'locations': scrape_helpers.get_movie_locations(movie_bs, movie_url)
		}

	def update_dict(self, update_dict, movie_title):
		for key,value in update_dict.items():
			for key_element in value:
				self.current_dict[key_element].extend(movie_title)

	def scrape_movie(self, movie_bs):
		movie_url = 'https://www.imdb.com' + movie_bs.find('a', href=True)['href']
		movie_bs = create_html_bs(movie_url)
		movie_title = scrape_helpers.get_movie_title(movie_bs)
		self.counter = self.counter + 1
		movie_aspects_dict = self.get_movie_aspects(movie_bs, movie_url)
		self.update_dict(movie_aspects_dict, movie_title)

	def scrape_movies(self, movies_url):
		movies_bs = create_html_bs(movies_url)
		for movie_bs in movies_bs.find(class_='lister-list').find_all(class_='lister-item-header'):
			self.scrape_movie(movie_bs)

	def create_url(self):
		count_cur_page = self.count_per_page
		if(self.offset + self.counter + self.count_per_page > self.limit):
			count_cur_page = self.limit - (self.offset + self.counter)

		params = ({
			'groups':'top_1000', 
			'sort': 'user_rating', 
			'count': count_cur_page, 
			'start':self.offset+ self.counter,
			'ref_':'adv_prv'
		})

		return ('https://www.imdb.com/search/title/?' + urlencode(params))


	def run(self):
		while(self.counter + self.offset < self.limit):
			scrape_url = self.create_url()
			#self.counter = self.count_per_page + self.offset
			print (scrape_url)
			self.scrape_movies(scrape_url)

	def dump(self):
		with open(self.file_name, 'w') as fp:
			json.dump(self.current_dict, fp)
