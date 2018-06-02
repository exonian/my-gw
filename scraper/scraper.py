import json
import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


class Breadcrumbs(object):
    output_file_path = 'breadcrumbs.json'
    product_ranges = {'www.games-workshop.com': ['Warhammer', 'Warhammer-40-000']}
    regions = ['en-GB']
    banned_category_names = ['Language']
    banned_entry_names = ['Pre-orders', 'New releases', 'Last chance to buy']

    def __init__(self, *args, **kwargs):
        self.browse_pages = []
        self.product_pages = defaultdict(list)

    def assemble(self):
        for region in self.regions:
            for website, product_ranges in self.product_ranges.items():
                for product_range in product_ranges:
                    self.get_browse_pages_for_product_range(product_range, website, region)
        print('')
        print('Found {} browse pages in total'.format(len(self.browse_pages)))

        for browse_page in self.browse_pages:
            pass
            # TODO add browse_page to the list for each product page linked to from it


    def get_browse_pages_for_product_range(self, product_range, website, region):
        params = {'website': website, 'product_range': product_range, 'region': region}
        url = 'https://{website}/{region}/{product_range}'.format(**params)
        print('Fetching {}'.format(url))
        response = requests.get(url)
        if response.status_code == 200:
            print('  Parsing the nav for browse pages')
            soup = BeautifulSoup(response.content, 'html.parser')
            start_phrase = "gw.cartridgeManager.renderPage("
            script_source = soup.find(text=re.compile(start_phrase.replace("(", "\(")))
            script_json = script_source[script_source.find(start_phrase) + len(start_phrase):].strip()[:-2]
            data = json.loads(script_json)
            browse_pages = []
            for category in data['contents'][0]['secondaryContent'][0]['contents'][0]['navigation']:
                if category['name'] not in self.banned_category_names:
                    for entry in category['refinements']:
                        name = entry['properties']['name']
                        browse_url = '{url}{nav_state}&view=all'.format(url=url, nav_state=entry['navigationState'])
                        if name not in self.banned_entry_names:
                            browse_pages.append((name, browse_url))

            self.browse_pages.extend(browse_pages)
            print('  Found {} browse pages'.format(len(browse_pages)))


if __name__ == '__main__':
    breadcrumbs = Breadcrumbs()
    breadcrumbs.assemble()
