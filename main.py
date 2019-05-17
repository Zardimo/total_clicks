import argparse
import sys
import os
import requests
from dotenv import load_dotenv
load_dotenv()


class UrlFormatError(TypeError):
    pass


def counting_clicks(new_url,headers):
    generated_url = ('https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary').format(new_url)
    payload = {'unit' : 'week', 'units' : '-1'}
    total_clicks = requests.get(generated_url, params=payload,
    headers=headers)
    if total_clicks.ok:
        return total_clicks.json()
	
	
def parser_url():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', required=True)
    return parser


def reduction_url(new_url,headers):
    long_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    title = {'long_url' : new_url}
    web_site = requests.post(long_url, json=title, headers=headers)
    if web_site.ok:
        return web_site.json()
    if not web_site.ok:
        raise UrlFormatError('Uncorrect url')


if __name__ == '__main__':
    parser = parser_url()
    link_parser = parser.parse_args()
    new_url = link_parser.url
    secret_token = os.getenv("TOKEN")
    headers = {"Authorization": secret_token}
    if counting_clicks(new_url,headers) is None:
        try:
            print(reduction_url(new_url,headers))
        except UrlFormatError:
            print('Invalid URL, try again')
    else:
        print('Количество переходов по ссылке битли: ' + 
	         str((counting_clicks(new_url,headers))['total_clicks']))