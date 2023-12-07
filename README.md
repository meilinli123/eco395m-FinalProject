# eco395m-FinalProject

<h1 align="center" id="heading"> <span style="color:red"> <em> Automotive Insights: </em> <br> Analysis and Visualization of Used Car Market through PostSQL Database </span> </h1>
<h3 align="center" id="heading"> Dec. 7, 2023 <br> 
<em> Python, Big Data, and Databases (ECO395m)  </em> <br> <h3>
<h3 align="center" id="heading"> Bevo’s Group: Meilin Li, Tianyu Wang, Macheddie Baker, Xiangmeng Qin, Yueting Zhang
 </h3>

Introduction & Background 
Navigating the automotive landscape involves more than just choosing between makes and models; it's about deciphering nuanced data that underlies every transaction. In a world of rapidly evolving automotive markets, having comprehensive insights into various aspects of car data is paramount. Whether you're a buyer looking for the best deal, a seller seeking optimal pricing strategies, or an enthusiast curious about market trends, understanding the details of car information becomes a crucial asset. Our project, "Automotive Data Insights," is designed with the goal of scraping, analyzing, and modeling essential car details from a car sales website, then delving into factors such as pricing, regression models, and location-based trends, with the use of SQL databases and StreamLit. Our project aims to provide valuable information that empowers users to make informed decisions in the dynamic landscape of the automotive industry.

Data
For this study, we leverage data obtained from Cars.com (see “References” for link), a prominent online advertising and research service tailored for car buyers, sellers, and enthusiasts. The richness of our data source, Cars.com, stems from its user-friendly interface and comprehensive listings of vehicle models, makes, and geographical information.



Methodology 

Step 1: We scraped used cars’ data from cars.com by first extracting all the urls to each listed car, then scrape page by page. For the information in each page, we extracted them to three tables: car_basic, car_more_info, and seller, which contained makes, models, prices, mileage, and seller’s information, etc. Within all tables we inserted VIN (Vehicle Identification Number) as a column, which is unique for every single car in the US. 

Step 2: After getting the three tables, we loaded them into a PostgreSQL database through GCP database.

Step 3: We choose to use a decision tree model to estimate the price. We use the sklearn library in python to feature 'make', 'model', 'produce_year', 'mileage' and zip_code, thus when customers enter their cars data, a price prediction model is generated based on our database, and then will give the estimated price for their specific car.

Step 4: After making counts of all makes and returns the most popular 10 makes on the country, we generated regression analysis by extracting price and mileage data from these 10 makes. Since this is real life data from a website, we endured robustness by using “RLM” instead of “OLS”. 

Step 5: We used streamlit-related packages to generate a website which displays all our data-analysis visualizations. The website contains a menu bar which switches among three main functions: interactive search bar which is connected to the price prediction model; display of the most popular makes of the nation; and a dashboard shows regression analysis results of price vs. mileage for top 10 most popular makes. 





Limitations
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






Analysis Extension
Environmental Impact Assessment: We could explore the environmental impact of certain car models by analyzing factors like fuel efficiency and emissions data. Provide insights into the ecological footprint of popular vehicles. 
Competitor Analysis: The analysis can be extended to include data from competing platforms, comparing the pricing, popularity, and features of cars listed on multiple websites. 
Seasonal Trends: We could investigate whether there are seasonal trends in car pricing or demand and provide recommendations for buyers based on optimal times to purchase.
Repoducability
Programs Used:
Python IDLE (Pycharm, Visual Studios)
SQL Database (Postgres)
StreamLit

Steps to rerun the analysis:

Step 0: Install the packages listed in requirements.txt
Step 1: Data Acquisition 
Run scrape_urls.py to extract all urls into a csv file
Run scrape.py to scrape page by page and return three tables in “data” folder in your directory. 
Step 2: DataBase
The SQL queries are written in code streamlit.py, analysis.py, and Mileage_vs_Price_Regression.py. You may modify these queries in order to extract de
Step 3: Data Manipulation 
python steps
Step 4: Analysis and Visualization
Stream Lit steps
Conclusion
In conclusion, "Automotive Data Insights" is not just a project; it's a gateway to a richer understanding of the automotive market. The significance of this information lies in its potential to guide users toward more informed decisions, whether they are navigating the complexities of buying, selling, or merely staying attuned to market dynamics. By combining regression models, price analysis, and location-specific data, our project aims to provide a holistic view, ensuring that users can confidently traverse the ever-evolving landscape of the automotive industry. Our investigation into the relationship between… revealed  …
References & Acknowledgements
Data retrieved from the following sites:

https://www.cars.com/?utm_source=google&utm_medium=cpc&utm_campaign_id=8628229388&utm_trusted=TRUE&network=g&aff=acqgeosem10&KNC=acqgeosem10&gad_source=1&gclid=Cj0KCQiAgqGrBhDtARIsAM5s0_nRh1gwkesHa6iaKrfN_vAare0AW6FPa3C0jeUNQdYVjQwEeUO1RT0aAvg-EALw_wcB&gclsrc=aw.ds

Reference Material:

Krueger, Edward. Menon, Shree. “API Calls & Data Scraping.”, “SQL & Databases.”, ECO395, University of Texas, Austin, Austin, October, 2023.
https://streamlit.io/
https://realpython.com/linear-regression-in-python/


