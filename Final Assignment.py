#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork900-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
#     </a>
# </p>
# 

# <h1>Extracting and Visualizing Stock Data</h1>
# <h2>Description</h2>
# 

# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.
# 

# <h2>Table of Contents</h2>
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ul>
#         <li>Define a Function that Makes a Graph</li>
#         <li>Question 1: Use yfinance to Extract Stock Data</li>
#         <li>Question 2: Use Webscraping to Extract Tesla Revenue Data</li>
#         <li>Question 3: Use yfinance to Extract Stock Data</li>
#         <li>Question 4: Use Webscraping to Extract GME Revenue Data</li>
#         <li>Question 5: Plot Tesla Stock Graph</li>
#         <li>Question 6: Plot GameStop Stock Graph</li>
#     </ul>
# <p>
#     Estimated Time Needed: <strong>30 min</strong></p>
# </div>
# 
# <hr>
# 

# In[2]:


get_ipython().system('pip install yfinance==0.1.67')
get_ipython().system('mamba install bs4==4.10.0 -y')
get_ipython().system('pip install nbformat==4.2.0')


# In[26]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ## Define Graphing Function
# 

# In this section, we define the function `make_graph`. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.
# 

# In[11]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1: Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
# 

# In[13]:


get_ipython().system('pip install yfinance')


# In[14]:


import yfinance as yf
tesla = yf.Ticker("TSLA")


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[9]:


tesla_data = tesla.history(period="max")


# **Reset the index** using the `reset_index(inplace=True)` function on the tesla_data DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.
# 

# In[11]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# 

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named `html_data`.
# 

# In[21]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# Parse the html data using `beautiful_soup`.
# 

# In[3]:


import requests
from bs4 import BeautifulSoup

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html.parser')


# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Quarterly Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.
# 

# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# 
# ```
# 
# </details>
# 

# In[3]:


import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html.parser')
table = soup.find_all("table")[1]  # Assuming the table you want is at index 1
tesla_revenue = pd.read_html(str(table))[0]
tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue.head()


# Execute the following line to remove the comma and dollar sign from the `Revenue` column. 
# 

# In[4]:


tesla_revenue = tesla_revenue.rename(columns={"Tesla Quarterly Revenue(Millions of US $)": "Date", "Tesla Quarterly Revenue(Millions of US $).1": "Revenue"})
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "", regex=True)
tesla_revenue.head()



# Execute the following lines to remove an null or empty strings in the Revenue column.
# 

# In[13]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# Display the last 5 row of the `tesla_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[14]:


tesla_revenue.tail()


# ## Question 3: Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.
# 

# In[1]:


import yfinance as yf

game_stop = yf.Ticker("GME")


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[3]:


gme_data = game_stop.history(period="max")


# **Reset the index** using the `reset_index(inplace=True)` function on the gme_data DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
# 

# In[4]:


gme_data.reset_index(inplace=True)
gme_data.head()


# ## Question 4: Use Webscraping to Extract GME Revenue Data
# 

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named `html_data`.
# 

# In[1]:


import requests

url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text


# Parse the html data using `beautiful_soup`.
# 

# In[2]:


import requests
from bs4 import BeautifulSoup

url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')


# Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Quarterly Revenue` and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`. Make sure the comma and dollar sign is removed from the `Revenue` column using a method similar to what you did in Question 2.
# 

# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# 
# ```
# 
# </details>
# 

# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')

gme_revenue = pd.read_html(url, match="GameStop Quarterly Revenue", flavor='bs4')[0]
gme_revenue = gme_revenue.rename(columns={"GameStop Quarterly Revenue(Millions of US $)": "Date", "GameStop Quarterly Revenue(Millions of US $).1": "Revenue"})
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(',|\$', "", regex=True)
gme_revenue.head()


# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[4]:


gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph
# 

# Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`. Note the graph will only show data upto June 2021.
# 

# In[18]:


import pandas as pd
import matplotlib.pyplot as plt

tesla_revenue = pd.DataFrame({
    'Date': [
        '2023-03-31', '2022-12-31', '2022-09-30', '2022-06-30', '2022-03-31',
        # ... add more dates
    ],
    'Revenue': [
        23329, 24318, 21454, 16934, 18756,
        # ... add more revenue values
    ]
})

tesla_data = pd.DataFrame({
    'Date': [
        '2010-06-29', '2010-06-30', '2010-07-01', '2010-07-02', '2010-07-06',
        # ... add more dates
    ],
    'Open': [
        1.266667, 1.719333, 1.666667, 1.533333, 1.333333,
        # ... add more open values
    ],
    'High': [
        1.666667, 2.028000, 1.728000, 1.540000, 1.333333,
        # ... add more high values
    ],
    'Low': [
        1.169333, 1.553333, 1.351333, 1.247333, 1.055333,
        # ... add more low values
    ],
    'Close': [
        1.592667, 1.588667, 1.464000, 1.280000, 1.074000,
        # ... add more close values
    ],
    'Volume': [
        281494500, 257806500, 123282000, 77097000, 103003500,
        # ... add more volume values
    ],
    'Dividends': [
        0, 0, 0, 0, 0,
        # ... add more dividend values
    ],
    'Stock Splits': [
        0.0, 0.0, 0.0, 0.0, 0.0,
        # ... add more stock split values
    ]
})

def make_graph(stock_data, revenue_data, company_name):
    plt.figure(figsize=(10, 6))
    
    # Plot stock data
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Date'], stock_data['Close'])
    plt.title(f'{company_name} Stock Data')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.xticks(rotation=45)
    
    # Plot revenue data
    plt.subplot(2, 1, 2)
    plt.plot(revenue_data['Date'], revenue_data['Revenue'])
    plt.title(f'{company_name} Revenue Data')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()


# In[19]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[9]:


## Question 6: Plot GameStop Stock Graph


# Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`. Note the graph will only show data upto June 2021.
# 

# In[20]:


import matplotlib.pyplot as plt

def make_graph(stock_data, revenue_data, company_name):
    plt.figure(figsize=(10, 6))
    
    # Plot stock data
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Date'], stock_data['Revenue'])
    plt.title(f'{company_name} Stock Data')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.xticks(rotation=45)
    
    # Plot revenue data
    plt.subplot(2, 1, 2)
    plt.plot(revenue_data['Date'], revenue_data['Revenue'])
    plt.title(f'{company_name} Revenue Data')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()



# In[24]:


import pandas as pd
import matplotlib.pyplot as plt

def make_graph(stock_data, revenue_data, company_name):
    plt.figure(figsize=(10, 6))

    # Filter stock data up to June 2021
    stock_data = stock_data[stock_data['Date'] <= '2021-06-30']

    # Plot stock data
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Date'], stock_data['Close'])
    plt.title(f'{company_name} Stock Data')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.xticks(rotation=45)

    # Plot revenue data
    plt.subplot(2, 1, 2)
    plt.plot(revenue_data['Date'], revenue_data['Revenue'])
    plt.title(f'{company_name} Revenue Data')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


gme_revenue = pd.DataFrame({
    'Date': [
        '2023-04-30', '2023-01-31', '2022-10-31', '2022-07-31', '2022-04-30',
        # ... add more dates
    ],
    'Revenue': [
        1237, 2226, 1186, 1136, 1378,
        # ... add more revenue values
    ]
})

gme_data = pd.DataFrame({
    'Date': [
        '2002-02-13', '2002-02-14', '2002-02-15', '2002-02-19', '2002-02-20',
        # ... add more dates
    ],
    'Open': [
        1.620128, 1.712708, 1.683250, 1.666417, 1.615920,
        # ... add more open values
    ],
    'High': [
        1.693350, 1.716074, 1.687458, 1.666417, 1.662210,
        # ... add more high values
    ],
    'Low': [
        1.603296, 1.670626, 1.658002, 1.578047, 1.603296,
        # ... add more low values
    ],
    'Close': [
        1.691666, 1.683251, 1.674834, 1.607504, 1.662210,
        # ... add more close values
    ],
    'Volume': [
        76216000, 11021600, 8389600, 7410400, 6892800,
        # ... add more volume values
    ],
    'Dividends': [
        0.0, 0.0, 0.0, 0.0, 0.0,
        # ... add more dividend values
    ],
    'Stock Splits': [
        0.0, 0.0, 0.0, 0.0, 0.0,
        # ... add more stock split values
    ]
})

make_graph(gme_data, gme_revenue, 'GameStop')


# <h2>About the Authors:</h2> 
# 
# <a href="https://www.linkedin.com/in/joseph-s-50398b136/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork900-2022-01-01">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
# 
# Azim Hirjani
# 

# ## Change Log
# 
# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description        |
# | ----------------- | ------- | ------------- | ------------------------- |
# | 2022-02-28        | 1.2     | Lakshmi Holla | Changed the URL of GameStop |
# | 2020-11-10        | 1.1     | Malika Singla | Deleted the Optional part |
# | 2020-08-27        | 1.0     | Malika Singla | Added lab to GitLab       |
# 
# <hr>
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 
# <p>
# 
