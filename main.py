from flask import Flask, render_template, session, request
import facebook, http, recommend, bookinfo, os
import ConfigParser, urlparse
import auth as oauth2
app = Flask(__name__)
app.secret_key = 'SESSKEY'
app.debug = False
config = ConfigParser.RawConfigParser()
config.read('config.ini')
FACEBOOK_ID = config.get("FACEBOOK", "ID")
FACEBOOK_SECRET = config.get("FACEBOOK", "SECRET")
fb = oauth2.FacebookAuth(FACEBOOK_ID, FACEBOOK_SECRET, "http://berlinbooks.herokuapp.com/callback")

@app.route("/")
def index():
	try:
		user_list = facebook.do_fql_request(session['access_token'])
		you = facebook.get_user_book(session['access_token'])

		r = recommend.Recommend()
		r.build_dict(user_list, you)
		recommendations = r.compare()
		recommended = []
		for book in recommendations:
			b =  bookinfo.get(book)
			if b is not None: 
				recommended.append(b)
		return render_template("/index.html", recommended = recommended)
	except KeyError:
		return render_template("/auth.html", auth_str = fb.auth_string)

@app.route("/callback")
def callback():
	code = request.args.get('code')
	access_token = fb.request_access_token(code)
	response = urlparse.parse_qs(access_token)
	session['access_token'] 	= response['access_token'][0]
	session['expires'] 		= response['expires'][0]
	return render_template("/callback.html")

if __name__ == "__main__":
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
