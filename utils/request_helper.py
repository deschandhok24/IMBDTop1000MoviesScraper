import requests
from bs4 import BeautifulSoup

def create_html_bs(url):
	try:
		page = requests.get(url)
		return BeautifulSoup(page.text, 'html.parser')
	except requests.exceptions.RequestException as e:
		print ('invalid url ' + e)