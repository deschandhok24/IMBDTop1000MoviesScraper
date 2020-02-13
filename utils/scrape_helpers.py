import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from utils.request_helper import create_html_bs


def bs_find (bs_query, movie_aspect, should_print = True):
	try:
		return bs_query()
	except Exception as e:
		if(should_print):
			print ('Could not find ' + movie_aspect + ' ' + str(e))

#only returns if full first name, full middle name, full last name (no suffix)
def extract_name(actor_name):
	part_name  = [part_name for part_name in actor_name.strip().split(' ') if '.' not in part_name]
	return  [part_name[0], part_name[-1], part_name[0]+part_name[-1]] if len(part_name) else []


def get_actors(crew_bs):
	movie_actors = set()
	actor_func = lambda: crew_bs.find(class_='cast_list').findAll(True, {'class':['odd', 'even']})
	actors = bs_find(actor_func, 'actor') or []
	for actor in actors:
		actor_name_func = lambda: actor.find_all('td')[1].find('a').getText().lower()
		actor_name = bs_find(actor_name_func, 'actor name')
		movie_actors.update(extract_name(actor_name)) if actor_name else None
	return movie_actors

def get_cast(crew_bs):
	movie_cast = set()
	for casts in crew_bs.find_all(class_='simpleCreditsTable'):
		for cast in casts.find_all(class_='name'):
			movie_cast.update(extract_name(cast.getText().lower()))
	return movie_cast

def get_movie_cast(movie_bs, movie_url):
	crew_url_func = lambda: movie_bs.find(id='titleCast').find(class_='see-more').find('a', href=True)['href']
	crew_url = bs_find(crew_url_func, 'crew url')
	if(crew_url):
		full_crew_url = movie_url + crew_url
		crew_bs = create_html_bs(full_crew_url)
		return list(get_actors(crew_bs) | get_cast(crew_bs))
	return []

def get_movie_rating(movie_bs):
	rating_func = lambda: movie_bs.find("span", itemprop="ratingValue").getText()
	return bs_find(rating_func, 'movie rating') or []

def get_movie_date(movie_bs):
	date_func = lambda: (movie_bs.find('a', title='See more release dates').getText()
		.split(' (')[0].lower().split())
	return bs_find(date_func, 'movie date') or []

def get_movie_discretion(movie_bs):
	discretion_func = lambda: ([movie_bs.find(class_='title_wrapper').find(class_='subtext')
		.getText().split('|')[0].strip().lower()])
	return bs_find(discretion_func, 'movie discretion') or []

def get_movie_languages(movie_bs):
	languages_func = (lambda: movie_bs.find(id= 'titleDetails').find(text= 'Language:')
		.find_parent(class_='txt-block').find_all('a'))
	languages_bs = bs_find(languages_func, 'movie languages') or []
	return [language_bs.getText().strip().lower() for language_bs in languages_bs]

def get_movie_production_company(movie_bs):
	company_func = (lambda: [movie_bs.find(id= 'titleDetails').find(text= 'Production Co:')
		.find_parent(class_='txt-block').find('a').getText().strip().lower()])
	return bs_find(company_func, 'movie production company') or []


def get_movie_length(movie_bs):
	length_func = lambda: [movie_bs.select_one('.title_wrapper time').getText().strip().lower()]
	return bs_find(length_func, 'movie length') or []

def get_movie_genre(movie_bs):
	genres_func = (lambda: movie_bs.find(id= 'titleStoryLine').find(text= 'Genres:')
		.find_parent(class_='see-more').find_all('a'))
	genres_bs = bs_find(genres_func, 'movie genres') or []
	return [genre_bs.getText().strip().lower() for genre_bs in genres_bs]

def get_movie_title(movie_bs):
	title_func = (lambda: [movie_bs.find(class_='title_wrapper').find('h1').getText()
		.split('(')[0].strip()])
	return bs_find(title_func, 'movie title') or []

def get_movie_locations(movie_bs, movie_url):
	locations_url_func = (lambda: movie_bs.find(text='Filming Locations:')
		.find_parent(class_='txt-block').find(class_='see-more').find('a')['href'])
	locations_url = bs_find(locations_url_func, 'many locations url', False)

	if(locations_url):
		movie_locations = set()
		full_locations_url = movie_url + locations_url
		locations_bs = create_html_bs(full_locations_url)

		for location_bs in locations_bs.select('#filming_locations .sodavote a[itemprop="url"]'):
			movie_locations.update([split_loc.strip().lower() for split_loc in location_bs.getText().split(',')])
		return list(movie_locations)

	else:
		one_location_url_func = (lambda: movie_bs.find(text='Filming Locations:')
		.find_parent(class_='txt-block').find('a').getText().lower().split(','))
		return bs_find(one_location_url_func, 'any locations url', True) or []
	return []