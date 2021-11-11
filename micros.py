import requests
from bs4 import BeautifulSoup

WIKI_URL = 'http://flip3.engr.oregonstate.edu:6231/?article='
TRAN_URL = 'http://flip2.engr.oregonstate.edu:6238/?text='


def wiki_scrape_translate(names, lang=None):

    text = []

    for name in names:
        r = requests.get(WIKI_URL + name)
        data = r.json()
        text.append(name.upper() + '\n\n' + data['info'][0:1000] + '...' + '\n\n')

    if lang:
        for index in range(0, len(text)):
            r = requests.get(TRAN_URL + text[index] + '&target=' + lang)
            soup = BeautifulSoup(r.content)
            text[index] = '\n\n' + soup.get_text()

    return text


if __name__ == '__main__':
    lst = ['apple', 'canada', 'wolf']
    lst = wiki_scrape_translate(lst)
    print(lst[1])
