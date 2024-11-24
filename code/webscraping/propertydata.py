from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the WebDriver
driver_service = Service(ChromeDriverManager().install())

# Uncomment the line below to specify the path to ChromeDriver locally
# driver_service = Service('/path/to/your/chromedriver')

# Ignore ssl errors
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(service=driver_service, options=options)

# URL of the NYC Open Data Air Quality page
url = "https://data.ct.gov/Housing-and-Development/Real-Estate-Sales-2001-2021-GL/5mzw-sjtu/data_preview"
driver.get(url)

# Allow the page to load
time.sleep(5)

def get_all_headers():
    global columns
    header_elements = driver.find_elements(By.CSS_SELECTOR, '.ag-header-cell-label .ag-header-cell-text')
    # Ensure all headers are captured
    columns = [header.text if header.text.strip() != '' else f"Unnamed_Column_{i+1}" for i, header in enumerate(header_elements)]
    print("Headers found:", columns)

def scrape_table():
    global columns
    # Locate the table
    table = driver.find_element(By.CLASS_NAME, 'ag-root-wrapper-body')
    
    # Retrieve the table headers only on the first page
    if not columns:
        get_all_headers()
    
    # Retrieve the table rows
    rows = table.find_elements(By.CSS_SELECTOR, '.ag-row')

    # Collect data
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, '.ag-cell')
        row_data = [cell.text for cell in cells]
        
        # Debugging: Print row length
        print(f"Row length: {len(row_data)}, Expected: {len(columns)}")
        
        # Ensure row length matches column length, adjust headers if necessary
        if len(row_data) > len(columns):
            additional_columns = len(row_data) - len(columns)
            for i in range(additional_columns):
                columns.append(f"Extra_Column_{i+1 + len(columns) - len(header_elements)}") # type: ignore
        
        # Ensure row length matches columns length by padding with empty strings
        while len(row_data) < len(columns):
            row_data.append('')
        
        data.append(tuple(row_data))  # Use tuple to handle duplicates later

def click_next_button():
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, '.ag-button.ag-paging-button[ref="btNext"]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)  # Allow time for the next page to load
    except Exception as e:
        print(f"Error clicking next button: {e}")

def scroll_table_horizontally():
    try:
        horizontal_scroll = driver.find_element(By.CSS_SELECTOR, '.ag-body-horizontal-scroll-viewport')
        driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", horizontal_scroll)
        time.sleep(2)  # Allow time for the table to adjust
    except Exception as e:
        print(f"Error scrolling horizontally: {e}")

data = []
columns = []  # Ensure columns is defined

# Scrape the first page
scrape_table()

# Pagination logic
page_number = 1
max_pages = 50

while page_number < max_pages:
    try:
        click_next_button()
        scrape_table()
        # scroll_table_horizontally()
        # scrape_table()
        page_number += 1
    except Exception as e:
        print("No more pages or error:", e)
        break

# Close the driver
driver.quit()

# Remove duplicate rows
data = list(set(data))

# Save the scraped data to a local file
if data:
    df = pd.DataFrame(data, columns=columns)
    local_file_path = 'Real-Estate-Sales_data.csv'
    df.to_csv(local_file_path, index=False)
    print(f"Data successfully saved to {local_file_path}")
else:
    print("No data found")


