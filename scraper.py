from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
import json
from collections import defaultdict

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Download and output directories
download_directory = os.path.join(current_directory, 'downloads')
output_directory = os.path.join(current_directory, 'output')

# Create folders if they don't exist
if not os.path.exists(download_directory):
    os.makedirs(download_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Start the webdriver with headless option
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Download preferences
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)

# Start webdriver service
print("Starting Chrome in headless mode...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
print("Connecting to the website...")
driver.get('https://www.e-icisleri.gov.tr/Anasayfa/MulkiIdariBolumleri.aspx')

# Wait for the page to load
time.sleep(2)

# Click the Excel download button
print("Clicking the download button...")
excel_button = driver.find_element(By.ID, 'ctl00_cph1_CografiBirimControl_imgButtonMahalleSayisiExcel')
excel_button.click()

# Wait until download is complete
print("Downloading the file, please wait...")
time.sleep(5)

# Get the list of downloaded files
files = os.listdir(download_directory)
print(f"Downloaded files: {files}")

# Find the most recently downloaded file
most_recent_file = max(
    [os.path.join(download_directory, f) for f in files],
    key=os.path.getmtime
)

print(f"Most recent downloaded file: {most_recent_file}")

# Close the browser
print("Closing the browser...")
driver.quit()

# Read the Excel file
print(f"Reading the Excel file: {most_recent_file}")
df = pd.read_excel(most_recent_file)

# Clean the data by dropping unnecessary columns
print("Cleaning data...")
df_cleaned = df.dropna(axis=1, how='all')  # Drop columns that are completely NaN
df_cleaned = df_cleaned[df_cleaned['Unnamed: 0'].notna()]  # Drop rows with NaN in 'Unnamed: 0'
df_cleaned = df_cleaned[['Unnamed: 0', 'Unnamed: 3', 'Unnamed: 5']]  # Keep necessary columns
df_cleaned = df_cleaned.rename(columns={'Unnamed: 0': 'Sıra', 'Unnamed: 3': 'Mahalle Adı', 'Unnamed: 5': 'Bağlılık Bilgisi'})

# Filter out rows with NaN or unwanted values in specific columns
df_cleaned = df_cleaned[df_cleaned['Mahalle Adı'].notna() & df_cleaned['Bağlılık Bilgisi'].notna()]

# Organize data into a nested dictionary
print("Organizing data into nested structure...")
nested_data = defaultdict(lambda: defaultdict(list))

# Populate the nested dictionary
for _, row in df_cleaned.iterrows():
    try:
        provinces = row['Bağlılık Bilgisi'].split("->")
        province = provinces[0].strip()
        district = provinces[1].strip()
        mahalle = row['Mahalle Adı']
        nested_data[province][district].append(mahalle)
    except IndexError:
        continue

# Convert data to JSON format
print("Converting data to JSON format...")
json_data = json.dumps(nested_data, ensure_ascii=False, indent=4)

# Define the output JSON file path
json_file_name = 'mahalleler.json'
if os.path.exists(os.path.join(output_directory, json_file_name)):
    json_file_name = json_file_name.split(".")[0] + "_1"
json_file_path = os.path.join(output_directory, json_file_name)

# Write the JSON data to a file
print(f"Saving JSON file: {json_file_path}")
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print(f"JSON file saved successfully: {json_file_path}")

# Delete the downloaded Excel file
os.remove(most_recent_file)
print(f"Deleted the Excel file: {most_recent_file}")
