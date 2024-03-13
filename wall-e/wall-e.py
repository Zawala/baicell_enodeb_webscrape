import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import logging
import json
import os
import configparser
from datetime import datetime
import schedule
from urllib.parse import urlparse
import time


config = configparser.ConfigParser()
config.read('/home/kelvin/wall-e/config.cfg')

# Get the paths from the configuration file
inventory_file_path = config.get('DEFAULT', 'inventory_file')
log_file_path = config.get('DEFAULT', 'log_file')

# Check if the inventory file exists and create it if it doesn't
if not os.path.exists(inventory_file_path):
    with open(inventory_file_path, 'w') as f:
        f.write('') # You can write initial content here if needed


def log_warnings(message):
    # Update the log file path based on the current date
    log_file = f"{log_file_path}{datetime.now().strftime('%Y%m%d')}-general.log"
    
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    
    # Create a file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(fh)
    
    # Log the message
    logger.warning(message)
    
    # Remove the handler to avoid logging to the same file in subsequent calls
    logger.removeHandler(fh)

def log_message(message):
    # Update the log file path based on the current date
    log_file = f"{log_file_path}{datetime.now().strftime('%Y%m%d')}-table_data.log"
    
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Create a file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(fh)
    
    # Log the message
    logger.info(message)
    
    # Remove the handler to avoid logging to the same file in subsequent calls
    logger.removeHandler(fh)


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
            parsed_url = urlparse(url)
            log_message(f'{parsed_url.hostname}:{row_dict}')

        count_enodeb=(len(table.find_all('tr')) - 1)
        return count_enodeb
    except Exception as e:
       log_warnings(f"An error occurred while scraping {url}: {e}")

    finally:
        await browser.close()


def rinnegan():
    with open(inventory_file_path, 'r') as file:
        inventory_data = json.load(file)

    # Iterate over each site in the inventory
    super_total_count_enodeb=0
    for site in inventory_data['sites']:
        url = site['url']
        username = site['username']
        password = site['password']
        total_count_enodeb=asyncio.get_event_loop().run_until_complete(scrape(url,username,password))
        if total_count_enodeb:
            super_total_count_enodeb+=total_count_enodeb

    log_message(f'Total connected clients: {super_total_count_enodeb}')

if __name__ == "__main__":
    schedule.every(60).minutes.do(rinnegan)
    while True:
        schedule.run_pending()
        time.sleep(1)