#libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium_stealth import stealth 
import pandas as pd 
from datetime import datetime 
import time 
 
URL = "https://coinmarketcap.com/" 
CSV_FILE = "cryptocurrencyprices.csv" 
TOP_N = 10
# configure webdriver or chrome  options
options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized")
options.add_argument("--disable-blinkfeatures=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--ignore-certificate-errors")

#Enable headless mode (no visible browser window)
HEADLESS = True
if HEADLESS: 
    options.add_argument("--headless=new") 

# Initialize the Chrome driver or webdriver manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#Apply selenium-stealth to evade detection
stealth(driver,languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)

# Navigate to the CoinMarketCap homepage
driver.get(URL) 
print("Loading CoinMarketCap homepage...") 

# Wait for the main table to load
try:
    WebDriverWait(driver, 30).until(   EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")) 

 ) 
    time.sleep(5) 
except Exception as e: 
    print("Could not load table:", e) 
    driver.quit()     
    exit()

# Scroll down to load more data if necessary
driver.execute_script("window.scrollTo(0, 800);") 
time.sleep(3)

# Extract data from the table
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr") 
print(f"Found {len(rows)} rows on the page")    

#Extract data form top rows
data = [] 
for row in rows[:TOP_N]:
      try:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 7: 
            name = cols[2].text.split('\n')[0]  
            symbol = cols[2].text.split('\n')[1] if '\n' in cols[2].text else False
            price = cols[3].text 
            change_24h = cols[4].text 
            market_cap = cols[7].text 
            data.append({"Name": name, "Symbol": symbol, 
                "Price": price, 
                "24h Change": change_24h, 
                "Market Cap": market_cap, 
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) 
      except Exception:
          continue
      
# Create a DataFrame and save to CSV    
df = pd.DataFrame(data) 
print(df)

# Append or save to CSV file
if not df.empty:
    df.to_csv(CSV_FILE, mode='a', index=False, header=not pd.io.common.file_exists(CSV_FILE))    
    print(f"\n  Data saved successfully to {CSV_FILE}")
else:
        print(" Still empty.")
driver.quit()