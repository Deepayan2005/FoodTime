import json

import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def give_details():
    text = str(request.args.get('input'))
    page = requests.get(text)
    # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find('div',class_='recipetabsdata ingredients_lilsting clearfix')

    compo = []
    steps = []

    for name in items.find_all('li',class_='clearfix'):
        compo.append(name.text)

    serving = soup.find('div',class_='servingselect').find('option').text.strip()

    for data in soup.find('div',class_='steps_listings clearfix').find_all('li'):
        s2 = BeautifulSoup(str(data),'html.parser')
        steps.append(s2.find('p').text)

    dict = {'components':compo,'servings':serving,'steps':steps}
    return json.dumps(dict)

