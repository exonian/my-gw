import json
import os
import re
import time
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


class Breadcrumbs(object):
    output_dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
    product_ranges = {
        'www.games-workshop.com': [
            'Warhammer',
            'Warhammer-40-000',
            'The-Hobbit',
            'Le-Hobbit',
            'Der-Hobbit',
            'El-Hobbit',
            'Lo-Hobbit',
            'Black-Library',
            'Painting-Modelling',
            'Peinture-Modélisme',
            'Malen-Basteln',
            'Pintura-Y-Modelismo',
            'Pittura-E-Modellismo',
            'Boxed-Games',
            'Boites-de-Jeu',
            'Spielsets',
            'Juegos-en-caja',
            'Giochi-in-scatola',
        ],
        'www.forgeworld.co.uk': [
            'Warhammer-40-000',
            'The-Horus-Heresy',
            'Warhammer-Age-of-Sigmar',
            'The-Hobbit-Trilogy',
            'More-Games',
            'Modelling',
        ],
    }
    regions = [
        'en-AU',
        'en-JP',
        'en-GB',
        'en-US',
        # 'en-BE',
        # 'en-CA',
        # 'en-DK',
        # 'en-DE',
        # 'en-ES',
        # 'en-FI',
        # 'en-FR',
        # 'en-IE',
        # 'en-IT',
        # 'en-NL',
        # 'en-NZ',
        # 'en-NO',
        # 'en-PL',
        # 'en-EU',
        # 'en-WW',
        # 'en-SE',
        # 'en-AT',
        # 'fr-BE',
        # 'fr-CA',
        # 'de-DE',
        # 'es-ES',
        # 'fr-FR',
        # 'it-IT',
        # 'de-AT',
    ]
    banned_category_names = [
        'New & Exclusive', 'Nouveau et en Exclusivité', 'Neu & Exklusiv', 'Nuevo y Exclusivo', 'Novità ed Esclusive',
        'Language', 'La langue', 'Sprache', 'Idioma', 'Lingua',
        "What's New",  # FW-only
    ]
    banned_entry_names = [
        'Bestsellers', 'Meilleures ventes', 'Bestseller', 'Los más vendidos', 'I più venduti',
        'Last Chance to Buy',  # only not in New & Exclusive on FW
    ]

    def assemble(self):
        for region in self.regions:
            for website, product_ranges in self.product_ranges.items():
                output_file_path = os.path.join(self.output_dir_path, '{}-{}-breadcrumbs.json'.format(website, region))
                print('https://{website}/{region}/'.format(website=website, region=region))
                browse_pages = []
                for product_range in product_ranges:
                    browse_pages.extend(self.get_browse_pages_for_product_range(product_range, website, region))
                print('')
                print('  Found {} browse pages in total'.format(len(browse_pages)))
                print('')

                product_pages = defaultdict(list)
                for i, browse_page in enumerate(browse_pages):
                    name, full_browse_url, partial_browse_url = browse_page
                    print('  {i} of {total}'.format(i=i + 1, total=len(browse_pages)))
                    print('  Fetching "{name}" {url}'.format(name=name, url=full_browse_url))
                    response = requests.get(full_browse_url)
                    if response.status_code == 200:
                        print('    Parsing the browse page for product page links')
                        link_partial_urls = re.findall('"product.seoUrl"\: \["([\w-]+)"\]', response.content.decode('utf-8'))
                        for partial_url in link_partial_urls:
                            product_pages[partial_url].append((name, partial_browse_url))
                    # time.sleep(0.5)
                print('')
                print('  Writing data to {}'.format(output_file_path))
                with open(output_file_path, 'w') as f:
                    f.write('breadcrumbs = ' + json.dumps(product_pages))


    def get_browse_pages_for_product_range(self, product_range, website, region):
        params = {'website': website, 'product_range': product_range, 'region': region}
        url = 'https://{website}/{region}/{product_range}'.format(**params)
        print('  Fetching {}'.format(url))
        response = requests.get(url)
        if response.status_code == 200:
            print('    Parsing the nav for browse pages')
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
                        browse_url = '{}{}&view=all'.format(url, entry['navigationState'])
                        breadcrumb_url = '/{}/{}{}'.format(region, product_range, entry['navigationState'])
                        if name not in self.banned_entry_names:
                            browse_pages.append((name, browse_url, breadcrumb_url))
            print('    Found {} browse pages'.format(len(browse_pages)))
            return browse_pages
        return []


if __name__ == '__main__':
    breadcrumbs = Breadcrumbs()
    breadcrumbs.assemble()
