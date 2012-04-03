import http, urllib, json, ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.ini')
GOOGLE_KEY = config.get("BOOKS", "KEY")


base_url = "https://www.googleapis.com/books/v1/volumes?key=" + str(GOOGLE_KEY)

def get(name):
	query_url = base_url + "&q=" + urllib.quote(name.encode("utf-8"))
	print query_url
	r = http.get(query_url)
	json_r = json.loads(r.content)
	if 'items' in json_r:
		try:
			item = json_r['items'][0]
			return_item = dict()
			if 'title' in item['volumeInfo']:       return_item['title'] = item['volumeInfo']['title']
			if 'authors' in item['volumeInfo']:     return_item['authors'] = item['volumeInfo']['authors']
			if 'description' in item['volumeInfo']: return_item['description'] = item['volumeInfo']['description'][:140] + " [...]"
			#if 'description' in item['volumeInfo']: return_item['description'] = item['volumeInfo']['subtitle']
			if 'imageLinks' in item['volumeInfo']:  return_item['images'] = item['volumeInfo']['imageLinks']
			if 'infoLink' in item['volumeInfo']:  return_item['infoLink'] = item['volumeInfo']['infoLink']
			return return_item
		except KeyError:
			pass
	else:
		print("no data found")