import pycurl
import cStringIO

def get(url):
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	print(url)
	c.setopt(c.URL, str(url))
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.perform()
	response_object = Response(buf.getvalue(), c.getinfo(pycurl.HTTP_CODE))
	buf.close()
	return response_object

def post(url, data):
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, repr(url))
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.perform()
	response_object = Response(buf.getvalue(), c.getinfo(pycurl.HTTP_CODE))
	buf.close()
	return response_object

class Response:

	def __init__(self, content, status_code):
		self.content = content
		self.status_code = status_code