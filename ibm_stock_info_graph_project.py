import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")

tesla_data.reset_index(inplace=True)
tesla_data['Date'] = tesla_data['Date'].astype(str)  # Convert 'Date' column to string
print(tesla_data.head())

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, "html.parser")

table = soup.find_all("tbody")[1]
rows = table.find_all("tr")
data = []
for row in rows:
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

tesla_revenue = pd.DataFrame(data, columns=["Date", "Revenue"])

tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',',"").str.replace('$','')
tesla_revenue = tesla_revenue[tesla_revenue["Revenue"].apply(lambda x: x.replace('.', '', 1).isdigit())]
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype(float)

tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail())

#Create a ticker object for GameStop
gme = yf.Ticker("GME")

#Extract stock information
gme_data = gme.history(period="max")

#Reset the index
gme_data.reset_index(inplace=True)

#Display the first five rows
print(gme_data.head())


#Download the webpage content
url_gme = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
response_gme = requests.get(url_gme)
html_data_gme = response_gme.text

#Parse the content using BeautifulSoup
soup_gme = BeautifulSoup(html_data_gme, "html.parser")

#Extract the table data
table_gme = soup_gme.find_all("tbody")[1]
rows_gme = table_gme.find_all("tr")
data_gme = []
for row in rows_gme:
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    data_gme.append(cols)

gme_revenue = pd.DataFrame(data_gme, columns=["Date", "Revenue"])

#Clean the data
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")

gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

#Display the last five rows of the dataframe
print(gme_revenue.tail())

# Plotting Tesla Stock Graph
# make_graph(tesla_data, tesla_revenue, 'Tesla')

gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(',', '').str.replace('$', '')
gme_revenue = gme_revenue[gme_revenue["Revenue"].apply(lambda x: x.replace('.', '', 1).isdigit())]
gme_revenue["Revenue"] = gme_revenue["Revenue"].astype(float)
make_graph(gme_data, gme_revenue, 'GameStop')