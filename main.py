import json

import requests
from bs4 import BeautifulSoup
from flask import Flask
from concurrent.futures import ThreadPoolExecutor

from flask import request

app = Flask(__name__)

@app.route('/details')
def give_details():
    text = str(request.args.get('input'))
    with ThreadPoolExecutor(max_workers=1000) as p:
        p.map(give_details)
        page = requests.get(text)
        # Getting page HTML through request
        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find('div',class_='recipetabsdata ingredients_lilsting clearfix')

        compo = []
        foodName = soup.find("h1", class_="nheadingrs").text
        imageLink = soup.find("div", class_="lftImg").find("img").get("src")
        steps = []

        for name in items.find_all('li',class_='clearfix'):
            compo.append(name.text)

        serving = soup.find('div',class_='servingselect').find('option').text.strip()

        for data in soup.find('div',class_='steps_listings clearfix').find_all('li'):
            s2 = BeautifulSoup(str(data),'html.parser')
            steps.append(s2.find('p').text)

        dict = {"name": foodName, "image": imageLink, 'components': compo, 'servings': serving, 'steps': steps}

        return json.dumps(dict)

@app.route('/search')
def search_recipes():
    text = str(request.args.get('input'))
    with ThreadPoolExecutor(max_workers=1000) as p:
        p.map(search_recipes)
        page = requests.get(text)
        # Getting page HTML through request
        soup = BeautifulSoup(page.content, 'html.parser')

        data = soup.find('div', class_='clearfix nomrg recipe_like_listing') \
            .find_all('div', class_='mustTry_left')
        list = []
        for rec in data:
            try:
                s2 = BeautifulSoup(str(rec), 'html.parser')
                link = s2.find('span', class_='posrel').find('a').get('href')
                image = s2.find('span', class_='posrel').find('a').find('img').get('data-src')
                name = s2.find('div', class_='caption clearfix').find('h2').text.replace('\n', '')
                time = s2.find('div', class_='caption clearfix').find('div', class_='nrecipe_vegnonveg') \
                    .text.replace('\n', '')
                category = s2.find('div', class_='caption clearfix').find('div', class_='nrecipe_vegnonveg') \
                    .find('span', class_='vegnonveg').contents[0].__str__().replace('span', "").replace('<', '') \
                    .replace('>', '').replace('/', '').replace('"', '').replace('class', '').replace('=', '')
                sen = {"name": name, "image": image, "link": link, "time": time, "category": category}

                list.append(sen)

            except AttributeError:
                print("sorry")
        return json.dumps(list)
