from classes.IMBDScraper import IMBDTopScraper

IMBDScraper = IMBDTopScraper(**{'offset':0, 'limit':1000, 'count_per_page':100})
IMBDScraper.run()
IMBDScraper.dump()