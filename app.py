from flask import Flask
import requests
from requests.exceptions import HTTPError
from urllib.parse import unquote_plus, quote_plus, parse_qs, urlsplit
import re
from flask import request, render_template, redirect, url_for
import os
from pathlib import Path
import yaml
from flask_misaka import Misaka
from slugify import slugify

TROVE_API_KEY = os.environ['TROVE_API_KEY']

app = Flask(__name__)
md = Misaka()
md.init_app(app)

def get_url(request):
    error = ''
    data = ''
    format = ''
    query_params = ''
    url = request.args.get('url', '')
    if url:
        url = unquote_plus(url)
        query = urlsplit(url).query
        query_params = parse_qs(query)
        if re.search(r'^https?:\/\/api\.trove\.nla\.gov\.au', url):
            if 'v3' in request.path:
                format = 'xml' if 'xml' in url else 'json'
            else:
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
    comment = request.args.get('comment', '')
    if comment:
        comment = unquote_plus(comment)
    return url, data, error, format, comment, query_params

@app.route('/v2/', methods=['GET'])
def show_api_results():
    examples = yaml.safe_load(Path('examples.yml').read_text())
    url, data, error, format, _, _ = get_url(request)
    return render_template('new_results.html', url=url, data=data, error=error, format=format, examples=examples)

@app.route('/v3/', methods=['GET'])
@app.route('/', methods=['GET'])
def show_api_v3_results():
    if "/v2/" in request.args.get("url", ""):
        return redirect(url_for('show_api_results', **request.args))
    else:
        examples = yaml.safe_load(Path('examples-v3.yml').read_text())
        url, data, error, format, comment, query_params = get_url(request)
        return render_template('new_results_v3.html', url=url, data=data, error=error, format=format, examples=examples, comment=comment, query_params=query_params)


@app.template_filter()
def slugified(value):
    return slugify(value)

if __name__ == '__main__':
    app.run(debug=True)
