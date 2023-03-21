import yaml
import requests
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv() 

TROVE_API_KEY = os.environ['TROVE_API_KEY']

def get_urls(version=""):
    urls = []
    yaml_data = yaml.safe_load(Path(f'examples{version}.yml').read_text())
    for section in yaml_data["sections"]:
        for example in section["examples"]:
            urls.append(example["url"])
    return urls

@pytest.mark.parametrize("url", get_urls("-v3"))
def test_url(url):
    response = requests.get(f"{url}&key={TROVE_API_KEY}")
    assert response.status_code == 200
    