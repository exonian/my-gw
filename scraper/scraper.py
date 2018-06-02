import json
import re

import requests
from bs4 import BeautifulSoup


OUTPUT_FILE_PATH = 'categories.json'
PRODUCT_RANGES = {'www.games-workshop.com': ['Warhammer', 'Warhammer-40-000']}
REGIONS = ['en-GB']


if __name__ == '__main__':
    for website, product_ranges in PRODUCT_RANGES.items():
        product_range = product_ranges[0]
        region = REGIONS[0]
        params = {'website': website, 'product_range': product_range, 'region': region}
        url = 'https://{website}/{region}/{product_range}'.format(**params)
        print('Fetching {}'.format(url))
        response = requests.get(url)
        if response.status_code == 200:
            print('  Parsing the result')
            soup = BeautifulSoup(response.content, 'html.parser')
            start_phrase = "gw.cartridgeManager.renderPage("
            script_source = soup.find(text=re.compile(start_phrase.replace("(", "\(")))
            script_json = script_source[script_source.find(start_phrase) + len(start_phrase):].strip()[:-2]
            data = json.loads(script_json)
            browse_pages = []
            for category in data['contents'][0]['secondaryContent'][0]['contents'][0]['navigation']:
                for entry in category['refinements']:
                    browse_pages.append((entry['properties']['name'], entry['navigationState']))
            print('  Found {} browse pages'.format(len(browse_pages)))
