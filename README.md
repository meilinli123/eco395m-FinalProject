# eco395m-FinalProject

<h1 align="center" id="heading"> <span style="color:red"> <em> Automotive Insights: </em> <br> Analysis and Visualization of Used Car Market through PostSQL Database </span> </h1>
<h3 align="center" id="heading"> Dec. 7, 2023 <br> 
<em> Python, Big Data, and Databases (ECO395m)  </em> <br> <h3>
<h3 align="center" id="heading"> Bevo’s Group: Meilin Li, Tianyu Wang, Macheddie Baker, Xiangmeng Qin, Yueting Zhang
 </h3>


## Introduction & Background

Navigating the automotive landscape involves more than just choosing between makes and models; it's about deciphering nuanced data that underlies every transaction. In a world of rapidly evolving automotive markets, having comprehensive insights into various aspects of car data is paramount.

Whether you're a buyer looking for the best deal, a seller seeking optimal pricing strategies, or an enthusiast curious about market trends, understanding the details of car information becomes a crucial asset.

Our project, **Automotive Data Insights**, is designed with the goal of scraping, analyzing, and modeling essential car details from a car sales website. We delve into factors such as pricing, regression models, and location-based trends, utilizing SQL databases and StreamLit to provide valuable information. This enables users to make informed decisions in the dynamic landscape of the automotive industry.


## Data

For this study, we leverage data obtained from [Cars.com](https://www.cars.com), a prominent online advertising and research service tailored for car buyers, sellers, and enthusiasts. The richness of our data source comes from its user-friendly interface and comprehensive listings of vehicle models, makes, and geographical information.


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

In the course of our project, we have encountered a series of limitations that have impacted the breadth and depth of our analysis:

- **Efficiency and Data Loss**: The scraping process was less efficient than anticipated, and complications with our code led to unforeseen data loss. This not only slowed our progress but also restricted the amount of data available for analysis.
  
- **Incomplete Vehicle Information**: The lack of comprehensive vehicle information on the website compromised our ability to forecast prices accurately, limiting the scope of our predictions.

- **Representativeness**: Data from Cars.com may not fully reflect the entire automotive market due to the platform's user demographics and the types of vehicles listed.

- **Temporal Factors**: The dynamic nature of the automotive market means that the data might quickly become outdated after collection.


## Findings & Results

Our comprehensive findings and results are derived from an in-depth analysis of the scraped car data from Cars.com:

- **Interactive Web Interface**: We utilize Streamlit to generate a web application that provides:

  - **Rankings**:
    - Top 5 most popular brands
    - Top 5 most expensive brands
    - Top 5 cheapest brands

  These rankings help customers gain a general understanding of the market.

- **Price vs. Mileage Regression**: We developed a regression model for the top 10 popular brands to explore how mileage impacts vehicle price and which brands offer a higher discount rate.


## Analysis Extension

Our analysis could be enriched further by considering the following aspects:

- **Environmental Impact Assessment**: Analyzing factors like fuel efficiency and emissions data to provide insights into the ecological footprint of popular vehicles.
  
- **Competitor Analysis**: Extending the analysis to include data from competing platforms to compare pricing, popularity, and features.

- **Seasonal Trends**: Investigating potential seasonal trends in car pricing or demand, and offering recommendations for optimal buying times.


## Reproducibility

### Programs Used:
- Python IDEs: PyCharm, Visual Studio Code
- SQL Database: PostgreSQL
- Data Visualization and Interaction: Streamlit

### Steps to Rerun the Analysis:

1. **Install the Packages**: Install the packages listed in `requirements.txt`.
   ```sh
   pip install -r requirements.txt

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

**Automotive Data Insights** is more than a project; it's a portal to a deeper comprehension of the automotive market. The value of our work is in empowering users to make well-informed decisions, whether they are buying, selling, or simply keeping up with market trends. Through the application of regression models, price analysis, and geographic data, we strive to offer a comprehensive view of the market. This ensures users can confidently navigate the ever-changing terrain of the automotive industry. Our analysis of the relationship between various factors has revealed insightful findings...

## References & Acknowledgements

**Data Sources:**
- [Cars.com](https://www.cars.com/?utm_source=google&utm_medium=cpc&utm_campaign_id=8628229388&utm_trusted=TRUE&network=g&aff=acqgeosem10&KNC=acqgeosem10&gad_source=1&gclid=Cj0KCQiAgqGrBhDtARIsAM5s0_nRh1gwkesHa6iaKrfN_vAare0AW6FPa3C0jeUNQdYVjQwEeUO1RT0aAvg-EALw_wcB&gclsrc=aw.ds) - Utilized for data acquisition and analysis.

**Reference Material:**
- Krueger, Edward. Menon, Shree. “API Calls & Data Scraping.” “SQL & Databases.” ECO395, University of Texas, Austin. October 2023.
- [Streamlit.io](https://streamlit.io/) - Used for creating interactive web applications.
- [Real Python - Linear Regression in Python](https://realpython.com/linear-regression-in-python/) - Provided guidance on regression analysis techniques.



