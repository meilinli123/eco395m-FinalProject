import requests
from bs4 import BeautifulSoup
import random 
import re
import backoff

def extract_car_make(soup):
    try:
        title_tag = soup.find('h1', class_='listing-title')
        title = title_tag.text.strip() if title_tag else None

        if title:
            
            title_words = title.split()
            if len(title_words) >= 2:
                make = title_words[1]
                return make
        return None

    except Exception as e:
        print(f"Error extracting car make: {e}")
        return None
    
def extract_produce_year(soup):
    try:
        title_tag = soup.find('h1', class_='listing-title')
        title = title_tag.text.strip() if title_tag else None

        if title:
            
            title_words = title.split()
            if len(title_words) >= 2:
                make = title_words[0]
                return make
        return None

    except Exception as e:
        print(f"Error extracting car make: {e}")
        return None
    
def extract_car_model(soup):
    try:
        title_tag = soup.find('h1', class_='listing-title')
        title = title_tag.text.strip() if title_tag else None

        if title:
            
            title_words = title.split()
            if len(title_words) >= 3:
                model = ' '.join(title_words[2:]) 
                return model
        return None

    except Exception as e:
        print(f"Error extracting car make: {e}")
        return None
    
def extract_car_title(soup):
    try:
        
        title_tag = soup.find('h1', class_='listing-title')
        title = title_tag.text.strip() if title_tag else None
        return title
    
    except Exception as e:
        print(f"Error extracting car title: {e}")
        return None
    
def new_used(soup):
    try:
        
        title_tag = soup.find('p', class_='new-used')
        title = title_tag.text.strip() if title_tag else None
        if title:
            if title == 'Used': title = 1
            if title == 'New': title = 0
        return title
    
    except Exception as e:
        print(f"Error extracting car title: {e}")
        return None
    
def extract_mileage(soup):
    try:
        
        title_tag = soup.find('div', class_='listing-mileage')
        title = title_tag.text.strip() if title_tag else None
       
        if title:
                
            mile_num = title.rstrip(' mi.')  
            mile = mile_num.replace(',', '')
            return mile
        return None
        
    except Exception as e:
        print(f"Error extracting car title: {e}")
        return None
    

def extract_price(soup):
    try:
        price_tag = soup.find('span', class_='primary-price')
        price_text = price_tag.text.strip() if price_tag else None

        if price_text:
            
            price_num = price_text.lstrip('$')  
            price = price_num.replace(',', '')
            return price
        return None

    except Exception as e:
        print(f"Error extracting car price: {e}")
        return None

def extract_car_info_table(url, soup):
    
    try:
        table_tag = soup.find('dl', class_='fancy-description-list')
        car_info = {
            "Exterior color": '',
            "Interior color": '',
            "Drivetrain": '',
            "MPG": '',
            "Fuel type": '',
            "Transmission": '',
            "Engine": '',
            "VIN": '',
            "Stock #": '',
            "Mileage": ''
        }
  
        if table_tag:
            dt_tags = table_tag.find_all('dt')
            dd_tags = table_tag.find_all('dd')

            for dt, dd in zip(dt_tags, dd_tags):
                key = dt.text.strip()
                value = dd.text.strip()

                if key in car_info:
                    if key == 'MPG':
                        try:
                            mpg_num = value.split('\n')[0].strip()
                            value = re.sub(r'[^0-9]', ',', mpg_num)
                            value = int(value)
                        except ValueError:
                            value = None
                    elif key == 'Mileage':
                        value_num = value.rstrip(' mi.')
                        if value_num == None:
                            value = None
                        else:
                            value = value_num.replace(',', '')

                    car_info[key] = value

        return car_info
    except Exception as e:
        print(f"Error extracting car info table for {url}: {e}")
        return car_info

def extract_seller_info(url,soup):
    
    try:
        
        title_tag1 = soup.find('h3', class_='spark-heading-5 heading seller-name')
        title1 = title_tag1.text.strip() if title_tag1 else None

    except Exception as e:
        print(f"Error extracting car title: {e}")
        return None
    
    try:
        
        title_tag2 = soup.find('div', class_='dealer-address')
        title2 = title_tag2.text.strip() if title_tag2 else None

        state = None  
        zip_code = None  

        if title2 != None:
            parts = title2.split(', ')
            if len(parts) == 2:
                state_zip = parts[1]  
                state = state_zip[:2]  
                zip_code = state_zip[-5:]  

        car_info = extract_car_info_table(url, soup)
        vin = car_info.get("VIN") if car_info is not None else None

    except Exception as e:
        print(f"Error extracting state and zip code: {e}")
        return None
    
    return {"VIN":vin, "seller":title1, "zip code":zip_code, "state":state, "address":title2}

def scrape_car(url):
    try:
        # proxy = get_proxy()
        soup = get_soup(url)
        if soup is None:
            return None
        soup = get_soup(url)
        make = extract_car_make(soup)
        year = extract_produce_year(soup)
        model = extract_car_model(soup)
        mileage = extract_mileage(soup)
        condition = new_used(soup)
        price = extract_price(soup)
        car_more_info = extract_car_info_table(url,soup)
        seller = extract_seller_info(url, soup)
        car_basic ={"VIN":car_more_info.get("VIN") if car_more_info is not None else None, "Make":make, "Produce Year":year, "Model":model, "Mileage":mileage, "New/Used":condition, "Price":price}
        return car_basic, car_more_info, seller
    
    except Exception as e:
        print(f"Error scraping car data: {e}")
        return None
    
def scrape_(urls):
    basic_data = []
    more_info = []
    seller_info = []
    

    for url in urls:
        car_info, car_more_info, seller = scrape_car(url)
            
        if car_info:
            basic_data.append(car_info)
            more_info.append(car_more_info)
            seller_info.append(seller)
            
        if not car_info:
            break

    return basic_data, more_info, seller_info

def _backoff_hdlr(details):
    print(f"Backing off {details['wait']} seconds after {details['tries']} tries due to exception: {details['exception']}")

@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.RequestException,
        Exception,
    ),
    on_backoff=_backoff_hdlr,
)

def get_soup(url):
    try:
        r = requests.get(url)
        # print(r.status_code)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Error getting soup: {e}")
        return None
    
# def get_proxy():
    
#     proxies = []
#     return random.choice(proxies)

if __name__ == "__main__": 

    url= ['https://www.cars.com/vehicledetail/5567e9dc-81fe-4731-bfee-04595a8e34c2/?attribution_type=premier']
    scrape_(url)
    basic_data, car_more_info, seller = scrape_(url)
    print(basic_data)
 
    
    
    
    
