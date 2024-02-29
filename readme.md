# Project Title: EnodeB Client Info Scraper

## Overview

This project aims to enhance the capabilities of Baicells eNodeB devices by enabling the retrieval of client information, which is currently not supported via SNMP. By leveraging web scraping techniques, we can extract valuable client data directly from the eNodeB's web interface.

## Background

Initially, the project was developed using Go, utilizing the GoColly framework for web scraping and Chromedp for browser automation. However, due to the need for more advanced parsing and interaction capabilities, the project was transitioned to Python. The new implementation leverages Beautiful Soup for HTML parsing and Pyppeteer for controlling a headless Chrome browser, providing a powerful combination for web scraping tasks.

## Features

- **Web Scraping**: Utilizes Beautiful Soup for parsing HTML and extracting client information from eNodeB web pages.
- **Browser Automation**: Employs Pyppeteer to automate browser interactions, such as logging into the eNodeB's web interface and navigating to the client information page.
- **Asynchronous Operations**: Leverages Python's asyncio library for efficient asynchronous execution, allowing for concurrent scraping tasks.
- **Logging**: Implements logging to track the scraping process and errors, with logs stored in a dedicated file for easy review.
- **Compilation**: Utilizes Nuitka for compiling the Python script into a standalone executable, enabling easy distribution and execution on systems without Python installed.
- **Log Management**: Connects logs to Loki for centralized logging and then visualizes them in Grafana, providing REST APIs to query the logs.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Beautiful Soup 4
- Pyppeteer
- Nuitka
- Loki
- Grafana

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Zawala/baicell_enodeb_webscrape.git
   ```
2. Navigate to the project directory:
   ```
   cd baicell_enodeb_webscrape
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Usage

1. Ensure your eNodeB device is accessible and its web interface is enabled.
2. Update the `inventory` file with the URLs, usernames, and passwords for the eNodeB devices you wish to scrape.
3. Run the scraper:
   ```
   python wall-e.py
   ```

### Building with Nuitka

To compile the Python script into a standalone executable, use the following command:

```
nuitka3 --standalone --onefile main.py
```

### Log Management with Loki and Grafana

To connect the logs to Loki and then visualize them in Grafana, follow these steps:

1. **Configure Loki**: Ensure Loki is set up and running. Configure it to receive logs from your application.
2. **Send Logs to Loki**: Modify the logging configuration in your application to send logs to Loki. This can be done by configuring the logging library to use a Loki-compatible log shipper or by directly sending logs to Loki's HTTP API.
3. **Set Up Grafana**: Install and configure Grafana to connect to Loki as a data source.
4. **Visualize Logs**: Create dashboards in Grafana to visualize the logs collected by Loki. Grafana's Explore feature can be used to query the logs and create visualizations.
5. **Integrate with ERPNext**: Use Grafana's REST API to query the logs and integrate them into ERPNext. This can be done by creating custom scripts or using ERPNext's API to fetch and display the log data within the ERPNext interface.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The GoColly and Chromedp teams for their excellent libraries.
- The Beautiful Soup and Pyppeteer teams for their powerful tools.
- Baicells for their eNodeB devices.
- The Nuitka team for providing a powerful Python compiler.
- The Loki and Grafana teams for their powerful log management and visualization tools.