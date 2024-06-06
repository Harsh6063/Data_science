import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import schedule

# Configuration
product_list = ['B0BDK62PDX']
base_url = 'https://www.amazon.in'
url_template = 'https://www.amazon.in/dp/{}'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'}

# Function to get session
def get_session():
    session = requests.Session()
    session.headers.update(headers)
    session.get(base_url)  # Initial GET request to set cookies
    return session

# Function to track prices
def track_prices():
    session = get_session()
    results = []
    
    for product_id in product_list:
        url = url_template.format(product_id)
        response = session.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            price_element = soup.find(class_='a-price-whole')
            
            if price_element:
                price = price_element.get_text(strip=True)
                results.append(f"{url} - Price: {price}")
            else:
                results.append(f"No price found for {product_id}")
        else:
            results.append(f"Failed to retrieve {url}. Status code: {response.status_code}")
    
    return results

# Streamlit App
st.title('Amazon Price Tracker')

# Display the current time
st.write("Current Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Schedule the price tracking
if st.button('Start Tracking'):
    st.write("Started tracking prices...")
    
    def run_schedule():
        results = track_prices()
        st.write("Results:")
        for result in results:
            st.write(result)
        
    schedule.every(1).minutes.do(run_schedule)

    while True:
        schedule.run_pending()
        time.sleep(1)
