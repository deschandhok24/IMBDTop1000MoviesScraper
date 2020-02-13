import requests
from collections import defaultdict
import json
import flask

app = flask.Flask(__name__)

movie_search_dict = defaultdict(lambda: [])
with open('data.json') as json_file:
    movie_search_dict = json.load(json_file)

@app.route('/', methods=['GET'])
def home():
	queries = flask.request.args.getlist('query')
	queries_set = [set(movie_search_dict.get(query, [])) for query in queries]
	kep = set.intersection(*queries_set)
	return str(kep)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')