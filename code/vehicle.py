import time
import requests
from bs4 import BeautifulSoup

# vehicle make
makes = ['Acura']

# 100 cards per page
base_url = 'https://www.cars.com/shopping/results/?maximum_distance=all&page_size=100&sort=best_match_desc&stock_type=all'

vehicle_ids = {}

for make in makes:
    # start from page 1
    page = 1
    # store vehicle ids
    ids = []
    while page < 5:
        r = requests.get(f'{base_url}&makes[]={make}&page={page}')
        # check if page exists
        if r.status_code != 200:
            break
        # parse html
        soup = BeautifulSoup(r.text, 'html.parser')
        # find all vehicle detail links
        hrefs = soup.find_all('a', attrs={'class':'vehicle-card-link js-gallery-click-link'})
        for href in hrefs:
            ids.append(href['href'].split('/')[2])
        page += 1
        time.sleep(5)
    vehicle_ids[make] = ids
    print(ids)