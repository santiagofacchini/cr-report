import json
import requests
import bs4


json_file = open('/home/santiago/vlex/cr-report/7718.json', 'r')
vids = json.load(json_file)

session = requests.Session()

log_file = open('/home/santiago/vlex/downloads/7718.csv', 'a')
log_file.write('NAME\tVID\tSOURCE_URL\tVLEX_DATE\tSOURCE_DATE\n')

for vid in vids:
    # Parse vLex date
    vlex_metdata = session.get(f'https://api.vlex.com/vid/{vid}.json').json()

    # Check if law is repealed
    try:
        vlex_date = vlex_metdata['in_force_date'].split('-')
        vlex_date = f'{vlex_date[2]}/{vlex_date[1]}/{vlex_date[0]}'
    except:
        vlex_date = vlex_metdata['status']

    # Parse source date
    source_url = session.get(vids[vid]['url'])
    soup_object = bs4.BeautifulSoup(source_url.content, 'html.parser')
    tds = soup_object.find_all('td', class_='tabla_texto3b')
    source_date = tds[-2].text.strip()[-10:]

    print(f'{vids[vid]["name"]}\thttps://app.vlex.com/#vid/{vid}\t{vids[vid]["url"]}\t{vlex_date}\t{source_date}')

    # Write metadata to file
    log_file.write(f'{vids[vid]["name"]}\t{vid}\t{vids[vid]["url"]}\t{vlex_date}\t{source_date}\n')

log_file.close()
