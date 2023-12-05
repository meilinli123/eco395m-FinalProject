import pandas as pd
import psycopg2
import pandas as pd

# Connect to your PostgreSQL database
def connect_to_database():
        connection = psycopg2.connect(
            user="postgres",
            password="luolex",
            host="34.173.71.254",
            port=5432,
            database="finalproject",
        )
        return connection

def top_10_brands():
        try:
                connection = connect_to_database()
                if connection:
                        cursor = connection.cursor()
                        query = "select make, count(*) total from car_basic group by make order by total desc limit 10;"
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        cursor.close()
                        connection.close()
                        df = pd.DataFrame(rows, columns=["brand", "total"])
                        return df
                return None
        except Exception as e:
                print(e)
                return None
brands = top_10_brands()
print(brands)


def top_5_expensive_brand():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "select make, avg (price) avg_price from car_basic group by make order by avg_price desc limit 5"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            df = pd.DataFrame(rows, columns = ["brand","avg_price"])
            return df
        return None
    except Exception as e:
        print(e)
        return None

expensive = top_5_expensive_brand()
print(expensive)

def top_5_cheapest_brand():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "select * from (select make, avg (price) avg_price from car_basic group by make order by avg_price) as T where avg_price > 0 limit 5;"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            df = pd.DataFrame(rows, columns=["brand", "avg_price"])
            return df
        return None
    except Exception as e:
        print(e)
        return None

cheap = top_5_cheapest_brand()
print(cheap)

