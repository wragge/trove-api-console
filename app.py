from flask import Flask
from urllib2 import urlopen, URLError, HTTPError
from urllib import unquote_plus, quote_plus
import re
from flask import request, render_template
from credentials import API_KEY

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_api_results():
	error = ''
	data = ''
	format = ''
	url = request.args.get('url', '')
	if url:
		url = unquote_plus(url)
		if re.search(r'^http:\/\/api\.trove\.nla\.gov\.au', url):
			format = 'json' if 'json' in url else 'xml'
			api_url = '{}&key={}'.format(url, API_KEY) if '?' in url else '{}?key={}'.format(url, API_KEY)
			try:
				response = urlopen(quote_plus(api_url, safe="%/:=&?~#+!$,;'@()*[]"))
			except HTTPError, e:
				if e.code == 400:
					error = 'Error: {}'.format(e.read())
				else:
					error = 'Error: {}'.format(e.code)
			except URLError, e:
				error = 'Error: {}'.format(e.reason)
			else:
				data = response.read().decode('utf-8').replace('<', '&lt;').replace('>', '&gt;')
		else:
			error = 'Error: That doesn''t look like a valid Trove url.'
	return render_template('results.html', url=url, data=data, error=error, format=format)

if __name__ == '__main__':
    app.run(debug=True)