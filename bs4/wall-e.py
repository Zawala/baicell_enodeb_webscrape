import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import logging
import json
import os
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

# Get the paths from the configuration file
inventory_file_path = config.get('DEFAULT', 'inventory_file')
log_file_path = config.get('DEFAULT', 'log_file')

# Check if the inventory file exists and create it if it doesn't
if not os.path.exists(inventory_file_path):
    with open(inventory_file_path, 'w') as f:
        f.write('') # You can write initial content here if needed

# Check if the log file exists and create it if it doesn't
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        f.write('') 

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

async def scrape(url,username,password):
    print(url,username,password)
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 550, 'height': 976})

    try:
        # Navigate to the URL
        await page.goto(url, timeout=60000)

        # Interact with elements
        await page.evaluate('document.querySelector("#username").value = "";')
        await page.type('#username', username)

        # Fill in the password
        await page.type('#password', password)

        await page.click('#log_button')

        # Wait for navigation to complete
        await page.waitForNavigation()

        # Wait for the specific table to load
        await page.waitForSelector('#ftr.lockedTr')

        # Get the page content
        content = await page.content()

        # Parse the content with Beautiful Soup
        soup = BeautifulSoup(content, 'html.parser')

        # Find the table with the ID 'UE_table'
        table = soup.find('table', {'id': 'UE_table'})

        header_row = table.find('tr', {'id': 'ftr'})
        keys = [th.text.strip() for th in header_row.find_all('td')]

        # Initialize an empty list to hold the dictionaries

        # Iterate over each row in the table body, skipping the header row
        for row in table.find_all('tr')[1:]:
            row_data = [td.text.strip() for td in row.find_all('td')]
            # Create a dictionary for each row, using the keys as keys
            row_dict = dict(zip(keys, row_data))
            # Log the dictionary directly
            logging.info(row_dict)

    except Exception as e:
        logging.error(f"An error occurred while scraping {url}: {e}")

    finally:
        await browser.close()



if __name__ == "__main__":
    with open(inventory_file_path, 'r') as file:
        inventory_data = json.load(file)

    # Iterate over each site in the inventory
    for site in inventory_data['sites']:
        url = site['url']
        username = site['username']
        password = site['password']
        asyncio.get_event_loop().run_until_complete(scrape(url,username,password))