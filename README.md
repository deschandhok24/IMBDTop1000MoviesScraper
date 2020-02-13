## IMBDTOP1000 Movie Scraper

Scrapes top 1000 imbd movies. 
Exposes simple API that returns movie name, given search terms

## Getting Started

### Prerequisites

Either:
Docker
OR 
Python3, Flask, Requests, and BeautifulSoup


### Running Search Service

With docker

1)sudo docker build -t name .

2)sudo docker run -d -p port:port_mapping name


```
sudo docker build -t des:latest .
sudo docker run -d -p 5000:5000 des

Runs on port 5000 on local host
```

Without docker

python3 app.py (will show up on localhost:5000 by default)


### Querying Search Service
Movie aspects:
Actor/cast
Location
Rating
Date of Release
Production Company
Discretion (rated r, pg-13, etc)
Genres
Languages
Movie Length- (example would be 2h 22min)

Everything is in lowercase


```
http://localhost:port/?query=brad&query=hanks - will return all movies the name brad and hanks are from the movie aspects scraped.

http://localhost:port/?query=2h 22min - will return all movies that are 2h and 22minutes long

http://localhost:port/?query=october - will return all movies that were released in October.

http://localhost:port/?query=tomhanks - will return all movies that were released by Tom Hanks.
```
### Running Scraper

The data.json file, which holds all the scraped data, has already been generated.
In order to re-scrape the data from IMDTop1000 movies and generate a new data.json file use the directions below.


With docker

Bash into docker using:

1)docker exec -it <container name> /bin/bash

2)python3 scrape.py   (will run the scraping of all 1000 movies)


Without docker

python3 scrape.py


## Other Info

Answer to questions given in prompt are in file questions.txt

