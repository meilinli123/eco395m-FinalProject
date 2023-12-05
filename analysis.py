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
                        df["total"] = df["total"].astype(int, errors="ignore")
                        return df
                return None
        except Exception as e:
                print(e)
                return None
top10 = top_10_brands()
print(top_10_brands())
print()

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
            df["avg_price"] = df["avg_price"].astype(float, errors = "ignore")
            return df
        return None
    except Exception as e:
        print(e)
        return None
top5 = top_5_expensive_brand()
print(top5)
print()

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
            df["avg_price"] = df["avg_price"].astype(float, errors="ignore")
            return df
        return None
    except Exception as e:
        print(e)
        return None

top5 = top_10_brands()
print(top5)
print()

def make_state():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "select make,  state, COUNT(*) AS total_cars FROM (SELECT * FROM seller_final JOIN car_basic ON seller_final.vin = car_basic.vin) as makestate GROUP BY make, state ORDER BY make, state"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            df = pd.DataFrame(rows, columns=["make", "state",'total_cars'])
            #df["make"] = df["state"].astype(float, errors="ignore")
            return df
        return None
    except Exception as e:
        print(e)
        return None
makestate = make_state()
print(makestate)
print()

def model_state():
    try:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            query = "select model,  state, COUNT(*) AS total_cars FROM (SELECT * FROM seller_final JOIN car_basic ON seller_final.vin = car_basic.vin) as modelstate GROUP BY model, state ORDER BY model, state"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            df = pd.DataFrame(rows, columns=["model", "state",'total_cars'])
            #df["make"] = df["state"].astype(float, errors="ignore")
            return df
        return None
    except Exception as e:
        print(e)
        return None
modelstate = model_state()
print(modelstate)
print()