import time
import requests
from bs4 import BeautifulSoup
import os
import csv

def scrape_ids(makes, car_base_url):
    url = 'https://www.cars.com/shopping/results/?maximum_distance=all&page_size=100&sort=best_match_desc&stock_type=all'
    for make in makes:
        page = 1
        ids = set()  
        previous_len = 0

        while True:
            r = requests.get(f'{url}&makes[]={make}&page={page}')
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'html.parser')

            hrefs = soup.find_all('a', attrs={'class': 'vehicle-card-link js-gallery-click-link'})
            for href in hrefs:
                vehicle_id = href['href'].split('/')[2]
                car_url = f'{car_base_url}{vehicle_id}/'
                ids.add(car_url)

            if len(ids) == previous_len:
                break

            previous_len = len(ids)
            page += 1
            time.sleep(5)
    
    
    idlist = list(ids)
    return idlist

if __name__== "__main__":

    # makes = ["AC", "Acura", "Alfa Romeo", "Am General", "American Motors", "Aston Martin", "Audi", "Austin-Healey", "Avanti Motors", "Bentley", "BMW", "Bugatti", "Buick", "Cadillac", "Chevrolet", "Chrysler", "Daewoo", "Datsun", "Delorean", "Desoto", "DeTomaso", "Dodge", "Eagle", "Edsel", "Ferrari", "FIAT", "Fisker", "Ford", "Genesis", "Geo", "GMC", "Honda", "Hudson", "Hummer", "Hyundai", "INEOS", "INFINITI", "International", "Isuzu", "Jaguar", "Jeep", "Jensen", "Kaiser", "Karma", "Kia", "Koenigsegg", "Lamborghini", "Land Rover", "LaSalle", "Lexus", "Lincoln", "Lotus", "Lucid", "Maserati", "Maybach", "Mazda", "McLaren", "Mercedes-Benz", "Mercury", "MG", "MINI", "Mitsubishi", "Morgan", "Nash", "Nissan", "Oldsmobile", "Opel", "Packard", "Pagani", "Panoz", "Plymouth", "Polestar", "Pontiac", "Porsche", "RAM", "Renault", "Rivian", "Rolls-Royce", "Rover", "Saab", "Saturn", "Scion", "smart", "Spyker", "Studebaker", "Subaru", "Sunbeam", "Suzuki", "Tesla", "Toyota", "Triumph", "Volkswagen", "Volvo", "Willys"]
    
    makes = ["AC"]
    car_base_url = "https://www.cars.com/vehicledetail/"
    car_urls = scrape_ids(makes, car_base_url)

    os.makedirs('data', exist_ok=True)

    PATH = os.path.join('data', "results.csv")
    # with open(PATH, "w") as file:
    #     for url in car_urls:
    #         file.write(url + "\n")
    with open(PATH, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        for url in car_urls:
            csv_writer.writerow([url])


    print(len(car_urls))
