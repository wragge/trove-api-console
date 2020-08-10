from flask import Flask
import requests
from requests.exceptions import HTTPError
from urllib.parse import unquote_plus, quote_plus
import re
from flask import request, render_template
import os
from pathlib import Path
import yaml
from flask_misaka import Misaka
from slugify import slugify

TROVE_API_KEY = os.environ['TROVE_API_KEY']

app = Flask(__name__)
md = Misaka()
md.init_app(app)

@app.route('/', methods=['GET'])
def show_api_results():
    error = ''
    data = ''
    format = ''
    examples = yaml.load(Path('examples.yml').read_text())
    url = request.args.get('url', '')
    if url:
        url = unquote_plus(url)
        if re.search(r'^https?:\/\/api\.trove\.nla\.gov\.au', url):
            format = 'json' if 'json' in url else 'xml'
            api_url = '{}&key={}'.format(url, TROVE_API_KEY) if '?' in url else '{}?key={}'.format(url, TROVE_API_KEY)
            try:
                # response = urlopen(quote_plus(api_url, safe="%/:=&?~#+!$,;'@()*[]"))
                response = requests.get(api_url)
                response.raise_for_status()
            except HTTPError:
                error = 'Error: {}'.format(response.status_code)
            else:
                data = response.text.replace('<', '&lt;').replace('>', '&gt;')
        else:
            error = 'Error: That doesn''t look like a valid Trove url.'
    return render_template('new_results.html', url=url, data=data, error=error, format=format, examples=examples)

@app.template_filter()
def slugified(value):
    return slugify(value)

if __name__ == '__main__':
    app.run(debug=True)
