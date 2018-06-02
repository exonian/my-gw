import json
import re

import requests
from bs4 import BeautifulSoup


class Breadcrumbs(object):
    output_file_path = 'breadcrumbs.json'
    product_ranges = {'www.games-workshop.com': ['Warhammer', 'Warhammer-40-000']}
    regions = ['en-GB']

    def __init__(self, *args, **kwargs):
        self.browse_pages = []

    def assemble(self):
        for region in self.regions:
            for website, product_ranges in self.product_ranges.items():
                for product_range in product_ranges:
                    self.get_browse_pages_for_product_range(product_range, website, region)

    def get_browse_pages_for_product_range(self, product_range, website, region):
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
            self.browse_pages.extend(browse_pages)
            print('  Found {} browse pages'.format(len(browse_pages)))


if __name__ == '__main__':
    breadcrumbs = Breadcrumbs()
    breadcrumbs.assemble()
