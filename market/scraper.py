import requests
from bs4 import BeautifulSoup
import json
from market.routes import Cryptocurrency, User
from market import db
from sqlalchemy import update


def generate_json():
    page = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find('tbody').find_all('tr')
    data = {'cryptocurrencies': []}

    for crypto in range(10):

        search_for_span = rows[crypto].find_all('span')
        search_for_a = rows[crypto].find_all('a')
        search_for_p = rows[crypto].find_all('p')

        ########################################################
        # Special percent with signs
        percent24hours = search_for_span[2].text
        percent7days = search_for_span[4].text

        ########################################################
        temp_percent24hours = search_for_span[2].find('span')['class'][0].split('-')[2]
        temp_percent7days = search_for_span[4].find('span')['class'][0].split('-')[2]

        if temp_percent24hours == 'up':
            percent24hours = ('+' + percent24hours).rstrip(percent24hours[-1])
        else:
            percent24hours = ('-' + percent24hours).rstrip(percent24hours[-1])

        if temp_percent7days == 'up':
            percent7days = ('+' + percent7days).rstrip(percent7days[-1])
        else:
            percent7days = ('-' + percent7days).rstrip(percent7days[-1])
        ########################################################

        price = search_for_a[1].text[1:]
        name = search_for_p[1].text
        shortcut = search_for_p[2].text
        market_cap = search_for_p[3].text.split("$")[2]
        volume24h = search_for_p[4].text.split("$")[1]
        volume24h_coin = search_for_p[5].text.split(" ")[0]
        circulating_supply = search_for_p[6].text.split(" ")[0]

        # print(f'Name: {name}')
        # print(f'Shortcut: {shortcut}')
        # print(f'Price: ${price}')
        # print(f'24h %: {percent24hours}')
        # print(f'7d %: {percent7days}')
        # print(f'Market Cap: ${market_cap}')
        # print(f'Volume24h(USD): ${volume24h}')
        # print(f'Volume24h({shortcut}): {volume24h_coin} {shortcut}')
        # print(f'Circulating Supply: {circulating_supply} {shortcut}')
        # print()

        data['cryptocurrencies'].append({
            'name': f'{str(name)}',
            'shortcut': f'{str(shortcut)}',
            'price': f'{float("".join(price.split(",")))}',
            'percent24hours': f'{float(percent24hours)}',
            'percent7days': f'{float(percent7days)}',
            'market_cap': f'{float("".join(market_cap.split(",")))}',
            'volume24h': f'{float("".join(volume24h.split(",")))}',
            #'volume24h_coin': f'{float("".join(volume24h_coin.split(",")))}',
            'circulating_supply': f'{float("".join(circulating_supply.split(",")))}'
        })

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)


def read_from_json():
    with open('data.json') as json_file:
        data = json.load(json_file)
        for p in data['cryptocurrencies']:
            if Cryptocurrency.query.filter_by(name=str(p['name'])).first() is None:

                new_crypto = Cryptocurrency(name=str(p['name']),
                                            shortcut=str(p['shortcut']),
                                            price=float(p['price']),
                                            percent24hours=float(p['percent24hours']),
                                            percent7days=float(p['percent7days']),
                                            market_cap=float(p['market_cap']),
                                            volume24h=float(p['volume24h']),
                                            circulating_supply=float(p['circulating_supply'])
                                            )
                db.session.add(new_crypto)

            else:
                Cryptocurrency.query.filter_by(name=str(p['name'])).update(
                    dict(
                        name=str(p['name']),
                        shortcut=str(p['shortcut']),
                        price=float(p['price']),
                        percent24hours=float(p['percent24hours']),
                        percent7days=float(p['percent7days']),
                        market_cap=float(p['market_cap']),
                        volume24h=float(p['volume24h']),
                        circulating_supply=float(p['circulating_supply'])
                    )
                )

            db.session.commit()


