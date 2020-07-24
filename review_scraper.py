# This review scraper extract user reviews from Apple App Store and save important info of them in json file

from urllib.request import urlopen
import ssl
import xml.etree.ElementTree as et
from urllib.error import HTTPError
import json
import os

# just some examples, there's a very comprehensive list on https://gist.github.com/daFish/5990634
countries = {'Canada': 'ca', 'China': 'cn', 'United States': 'us', 'Singapore': 'sg', 'Egypt': 'eg'}
# two ways of sorting the reviews
sort_ways = ['mostRecent', 'mostHelpful']


def generate_url(country, page, app_id, sort_by):
    return f'https://itunes.apple.com/{country}/rss/customerreviews/page={page}/id={app_id}/sortBy={sort_by}/xml'


def save_xml(url):
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    req = response.read()
    with open('reviews.xml', 'wb') as f:
        f.write(req)


def parse_one_page(url):
    save_xml(url)
    tree = et.parse('reviews.xml')
    ns = {'d': 'http://www.w3.org/2005/Atom'}
    ns_rating = {'im': 'http://itunes.apple.com/rss'}
    items = []
    root = tree.getroot()
    for child in root:
        if child.tag == '{http://www.w3.org/2005/Atom}entry':
            date = child.find('d:updated', ns).text[:10]
            rating = child.find('im:rating', ns_rating).text
            title = child.find('d:title', ns).text
            content = child.find('d:content', ns).text
            items.append({'date': date,
                          'rating': rating,
                          'title': title,
                          'content': content})
    os.remove('reviews.xml')
    return items


# extract reviews of an app on a certain page in the App Store of the specified country
def get_reviews_on_page(country, page, app_id, sort_by='mostRecent', out_filename='reviews.json'):
    url = generate_url(country, page, app_id, sort_by)
    data = {'review': []}

    try:
        data['review'] = parse_one_page(url)
    except HTTPError:
        print('There is no review on this page or for this app.')
        return

    if not data['review']:
        print('There is no review for this app.')
    else:
        with open(out_filename, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, indent=4, ensure_ascii=False)


# extract reviews of an app from page from_page to to_page in the App Store of the specified country
def get_reviews_on_pages(country, from_page, to_page, app_id, sort_by='mostRecent', out_filename='reviews.json'):
    if from_page == to_page:
        get_reviews_on_page(country, from_page, app_id, sort_by='mostRecent', out_filename='reviews.json')
    elif from_page > to_page:
        raise Exception('Invalid input: pages should go from a smaller number to a larger number')

    data = {'review': []}
    for i in range(from_page, to_page + 1):
        url = generate_url(country, i, app_id, sort_by)
        try:
            data['review'].extend(parse_one_page(url))
        except HTTPError:
            break

    if not data['review']:
        print('There is no review for this app or on these pages.')
    else:
        with open(out_filename, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, indent=4, ensure_ascii=False)


# extract all existing reviews of an app in the App Store of the specified country
def get_all_reviews(country, app_id, sort_by='mostRecent', out_filename='reviews.json'):
    data = {'review': []}
    i = 1
    while True:
        url = generate_url(country, i, app_id, sort_by)
        try:
            data['review'].extend(parse_one_page(url))
            i += 1
        except HTTPError:
            break

    if not data['review']:
        print('There is no review for this app.')
    else:
        with open(out_filename, 'w', encoding='utf-8') as out_file:
            json.dump(data, out_file, indent=4, ensure_ascii=False)
