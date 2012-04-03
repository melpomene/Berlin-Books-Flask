from flask import Flask, render_template, session, request
import facebook, http
import ConfigParser
import auth as oauth2
app = Flask(__name__)
app.secret_key = 'SESSKEY'
config = ConfigParser.RawConfigParser()
config.read('config.ini')
FACEBOOK_ID = config.get("FACEBOOK", "ID")
FACEBOOK_SECRET = config.get("FACEBOOK", "SECRET")
fb = oauth2.FacebookAuth(FACEBOOK_ID, FACEBOOK_SECRET, "http://127.0.0.1:5000/callback")

@app.route("/")
def index():
	try:
		session['access_token']
	except Exception, e:
		return render_template("/auth.html", auth_str = fb.auth_string)

	session['test'] = "HAILOL"
	return render_template("/index.html")

@app.route("/callback")
def callback():
	code = request.args.get('code')
	access_token = fb.request_access_token(code)
	response = urlparse.parse_qs(access_token)
	session['access_token'] 	= response['access_token'][0]
	session['expires'] 		= response['expires'][0]
	return session['test']

if __name__ == "__main__":
	app.debug = True
	app.run()