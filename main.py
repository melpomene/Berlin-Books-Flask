from flask import Flask, render_template, session, request
import facebook
import auth as oauth2
app = Flask(__name__)

app.secret_key = 'SESSKEY'

@app.route("/")
def index():
	session['test'] = "HAILOL"
	return render_template("/index.html")

@app.route("/callback")
def callback():
	code = request.args.get('code')
	fb = oauth2.FacebookAuth(FACEBOOK_ID, FACEBOOK_SECRET, "http://0.0.0.0:8080/callback")
	access_token = fb.request_access_token(code)
	response = urlparse.parse_qs(access_token)
	session['access_token'] 	= response['access_token'][0]
	session['expires'] 		= response['expires'][0]
	return session['test']

if __name__ == "__main__":
	app.debug = True
	app.run()