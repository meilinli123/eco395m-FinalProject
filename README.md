# eco395m-FinalProject

<h1 align="center" id="heading"> <span style="color:red"> <em> Automotive Insights: </em> <br> Analysis and Visualization of Used Car Market through PostSQL Database </span> </h1>
<h3 align="center" id="heading"> Dec. 7, 2023 <br> 
<em> Python, Big Data, and Databases (ECO395m)  </em> <br> <h3>
<h3 align="center" id="heading"> Bevo’s Group: Meilin Li, Tianyu Wang, Macheddie Baker, Xiangmeng Qin, Yueting Zhang
 </h3>

## Introduction & Background

Navigating the automotive landscape involves more than just choosing between makes and models; it's about deciphering nuanced data that underlies every transaction. In a world of rapidly evolving automotive markets, having comprehensive insights into various aspects of car data is paramount. Whether you're a buyer looking for the best deal, a seller seeking optimal pricing strategies, or an enthusiast curious about market trends, understanding the details of car information becomes a crucial asset. Our project, "Automotive Data Insights," is designed with the goal of scraping, analyzing, and modeling essential car details from a car sales website, then delving into factors such as pricing, regression models, and location-based trends, with the use of SQL databases and StreamLit. Our project aims to provide valuable information that empowers users to make informed decisions in the dynamic landscape of the automotive industry.

## Data
For this study, we leverage data obtained from Cars.com (see “References” for link), a prominent online advertising and research service tailored for car buyers, sellers, and enthusiasts. The richness of our data source, Cars.com, stems from its user-friendly interface and comprehensive listings of vehicle models, makes, and geographical information.



## Methodology

### Step 1: Data Scraping
We performed data scraping from cars.com by:
- Extracting URLs to each listed car.
- Scraping information page by page.
- Organizing the data into three tables: `car_basic`, `car_more_info`, and `seller`, which include details such as makes, models, prices, mileage, and seller's information.
- Including the VIN (Vehicle Identification Number) for each car, ensuring a unique identifier for each entry.

### Step 2: Data Storage
The extracted tables were loaded into a PostgreSQL database hosted on GCP (Google Cloud Platform).

### Step 3: Price Prediction Model
For price estimation, we:
- Chose a decision tree model from the `sklearn` library.
- Used features such as 'make', 'model', 'produce_year', 'mileage', and 'zip_code'.
- Created a model that generates price predictions based on user input compared to our database.

### Step 4: Regression Analysis
To analyze the data further:
- We counted all makes and identified the top 10 most popular in the country.
- Conducted regression analysis using "RLM" (Robust Linear Models) to ensure robustness against real-life data variations.

### Step 5: Data Visualization and Interaction
We developed a web interface using `streamlit` where users can:
- Utilize an interactive search bar linked to the price prediction model.
- View the most popular makes nationwide.
- Access a dashboard displaying regression analysis of price vs. mileage for the top 10 makes.






## Limitations
In the course of our project, we have encountered a series of limitations that have impacted the breadth and depth of our analysis. The scraping process we utilized was less efficient than we had hoped, and complications with our code led to unforeseen data loss. This issue not only slowed our progress but also restricted the amount of data we could analyze. Moreover, our ability to forecast prices was compromised by the lack of comprehensive vehicle information on the website, limiting the scope of our predictions.

Further limitations of our analysis include:

Representativeness: The data available on Cars.com may not be fully representative of the entire automotive market. The platform's user demographics and the types of vehicles listed might skew your findings towards certain segments.
Temporal Factors: As the automotive market is dynamic, the data you scrape might quickly become outdated. Changes in prices, models, or other features might occur after your data collection, potentially 
Findings & Results
In this section, we present the comprehensive findings and results derived from the thorough analysis of the scraped car data from Cars.com.
We use streamlit to generate a Web with the following functions:
Some Rankings include 
	Top 5 most popular branches
	Top 5 most expensive branches
Top 5 cheapest branches
to help customer to have a general understanding of the market, making it less
Price vs mileage regression model for the top 10 popular branches. We want to explore how the mileage of a vehicle impacts its price, which make(brand) has higher discount rate 






## Analysis Extension
Environmental Impact Assessment: We could explore the environmental impact of certain car models by analyzing factors like fuel efficiency and emissions data. Provide insights into the ecological footprint of popular vehicles. 
Competitor Analysis: The analysis can be extended to include data from competing platforms, comparing the pricing, popularity, and features of cars listed on multiple websites. 
Seasonal Trends: We could investigate whether there are seasonal trends in car pricing or demand and provide recommendations for buyers based on optimal times to purchase.
Repoducability
Programs Used:
Python IDLE (Pycharm, Visual Studios)
SQL Database (Postgres)
StreamLit


## Steps to Rerun the Analysis

1. **Install the Packages**:
   Install the packages listed in `requirements.txt`.

2. **Data Acquisition**:
- Run `scrape_urls.py` to extract all URLs into a CSV file.
- Run `scrape.py` to scrape page by page and return three tables in the “data” folder in your directory.

3. **Database**:
The SQL queries are written in code `streamlit.py`, `analysis.py`, and `Mileage_vs_Price_Regression.py`. You may modify these queries in order to extract data.

4. **Data Manipulation**:
Execute the python steps for data manipulation as needed.

5. **Analysis and Visualization**:
Follow the Streamlit steps for analysis and visualization.


## Conclusion
In conclusion, "Automotive Data Insights" is not just a project; it's a gateway to a richer understanding of the automotive market. The significance of this information lies in its potential to guide users toward more informed decisions, whether they are navigating the complexities of buying, selling, or merely staying attuned to market dynamics. By combining regression models, price analysis, and location-specific data, our project aims to provide a holistic view, ensuring that users can confidently traverse the ever-evolving landscape of the automotive industry. Our investigation into the relationship between… revealed  …


## References & Acknowledgements
Data retrieved from the following sites:

https://www.cars.com/?utm_source=google&utm_medium=cpc&utm_campaign_id=8628229388&utm_trusted=TRUE&network=g&aff=acqgeosem10&KNC=acqgeosem10&gad_source=1&gclid=Cj0KCQiAgqGrBhDtARIsAM5s0_nRh1gwkesHa6iaKrfN_vAare0AW6FPa3C0jeUNQdYVjQwEeUO1RT0aAvg-EALw_wcB&gclsrc=aw.ds

Reference Material:

Krueger, Edward. Menon, Shree. “API Calls & Data Scraping.”, “SQL & Databases.”, ECO395, University of Texas, Austin, Austin, October, 2023.
https://streamlit.io/
https://realpython.com/linear-regression-in-python/


