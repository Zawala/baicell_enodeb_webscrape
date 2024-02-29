import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import logging
import pyppeteer.errors
import traceback # Ensure this is imported
import json

logging.basicConfig(filename='table_data.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

async def main():
    # Read and parse the inventory file
    with open('inventory', 'r') as file:
        inventory_data = json.load(file)

    # Iterate over each site in the inventory
    for site in inventory_data['sites']:
        ip = site['ip']
        username = site['username']
        password = site['password']
        print(ip,username,password)

        try:
            browser = await launch(headless=True)
            page = await browser.newPage()
            await page.setViewport({'width': 1365, 'height': 976})

            # Navigate to the URL using the IP address
            await page.goto(ip)

            # Interact with elements
            await page.waitForSelector('#username')
            await page.click('#username')
            await page.type('#username', username)

            await page.waitForSelector('#password')
            await page.click('#password')
            await page.type('#password', password)

            # Click the login button
            await page.waitForSelector('#log_button')
            await page.click('#log_button')

            # Wait for navigation to complete
            await page.waitForNavigation({"timeout": 60000})

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
            data_list = []

            # Iterate over each row in the table body, skipping the header row
            for row in table.find_all('tr')[1:]:
                row_data = [td.text.strip() for td in row.find_all('td')]
                # Create a dictionary for each row, using the keys as keys
                row_dict = dict(zip(keys, row_data))
                data_list.append(row_dict)

            # Print the list of dictionaries
            for item in data_list:
                logging.info(item)

            await browser.close()

        except pyppeteer.errors.TimeoutError as e:
        # Log the traceback along with the error message
            logging.error(f"TimeoutError: {e}\n{traceback.format_exc()}")
        except pyppeteer.errors.PageError as e:
            logging.error(f"PageError: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())