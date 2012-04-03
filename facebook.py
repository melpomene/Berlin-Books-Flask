import http, json, urllib

baseurl = 'https://graph.facebook.com/'
access_token_query = '?access_token='

def do_fql_request(token):
	queries = dict()
	friends_query = '"friends_q":"SELECT uid2 FROM friend WHERE uid1 = me()"'
	books_query = '"books_q":"SELECT uid,books FROM user WHERE uid IN (SELECT uid2 FROM #friends_q) AND books != \'\' "'
	req_url = baseurl + "fql?q=" + urllib.quote("{" + friends_query + "," + books_query + "}") + "&access_token=" + token
	#print req_url
	r = http.get(req_url)
	json_r = json.loads(r.content)
	#print json_r
	user_list = []
	for user in  json_r['data'][1]['fql_result_set']:
		# [{"name":"tom", "books":["bok1", "bok2", "bok3"]}, {"name":"eva", "books":["bok1", "bok4"] } ])
		book_list = map(lambda x: x.strip(), user["books"].split(", "))
		user_list.append({"name":str(user["uid"]), "books":book_list})
	return user_list

def get_user_book(token, friend_id="me"):
	query_url = baseurl +str(friend_id) + '/books' + access_token_query + token
	print query_url
	r = http.get(query_url)

	if r.status_code != 200:
		print "There was a problem connecting to facebook.\nStatus code: " + str(r.status_code)
	else:
		jr = json.loads(r.content)
		value = []
		for book in jr['data']:
			value.append(book['name'])
		return value

