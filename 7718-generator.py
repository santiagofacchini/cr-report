import requests
import bs4
import browser_cookie3
import re
import json


json_file = open('/Users/santiagofacchini/Desktop/vlex-dotfiles/7718.json', 'r')
vids_json = json.load(json_file)

vid_regex = re.compile(r'/vid/.*-\d+')

cookies = browser_cookie3.chrome()
seed_url = 'https://admin.vlex.com/source/7718?page='
pages = ['1', '2', '3', '4', '5', '6']

session = requests.Session()

for page in pages:
    r = session.get(f'{seed_url}{page}', cookies=cookies)

    soup = bs4.BeautifulSoup(r.content, 'html.parser')

    vids = soup.find_all('a', href=vid_regex)

    for vid in vids:
        title = vid.text.strip()
        vid = re.sub(r'/vid/.*-(\d+)$', r'\1', vid['href'])
        print(vid)

        if vid not in vids_json:
            print(
                {
                    vid: {
                        "name": title,
                        "url": "",
                        "versions": False
                    }
                }
            )

