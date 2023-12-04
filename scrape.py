import os
import csv
from scrape_pages import scrape_

def write_to_csv(data, path):
    try:
        if data:
            with open(path, 'w', newline='') as file:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    except Exception as e:
        print(f"Error writing data to CSV: {e}")

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)

    url_path = os.path.join('data', "urls.csv")
    CSV_PATH1 = os.path.join('data', 'car_basic.csv')
    CSV_PATH2 = os.path.join('data', 'car_more_info.csv')
    CSV_PATH3 = os.path.join('data', 'seller.csv')

    with open(url_path, "r") as file:
        car_urls = [line.strip() for line in file]

    basic_data, more_info, seller_info = scrape_(car_urls)

    write_to_csv(basic_data, CSV_PATH1)
    write_to_csv(more_info, CSV_PATH2)
    write_to_csv(seller_info, CSV_PATH3)
    