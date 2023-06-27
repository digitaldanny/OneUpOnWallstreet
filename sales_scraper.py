import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sec.gov"
SEARCH_URL = f"{BASE_URL}/cgi-bin/browse-edgar"
FILINGS_PATH = "/Filings"
REPORT_PATH = "/10-K"
TABLE_CLASS = "report"
TOP_PRODUCTS_COUNT = 3

def scrape_sales_percentage(ticker):
    """
    Scrapes SEC EDGAR for a company's sales and calculates the percentage of total income for the top 3 products.
    Returns a list of tuples containing the product name and its sales percentage.
    """
    search_url = f"{SEARCH_URL}?CIK={ticker}&Find=Search&owner=exclude&action=getcompany"

    # Send a GET request to search for the company
    response = requests.get(search_url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the link to the company's filings
    filings_link = soup.find('a', string='Filings')

    if filings_link:
        filings_url = f"{BASE_URL}{filings_link['href']}"

        # Send a GET request to the filings page
        response = requests.get(filings_url)

        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the link to the latest annual report (Form 10-K)
        report_link = soup.find('a', string='10-K')

        if report_link:
            report_url = f"{BASE_URL}{report_link['href']}"

            # Send a GET request to the report page
            response = requests.get(report_url)

            # Create a BeautifulSoup object
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the HTML table containing the financial information
            table = soup.find('table', class_=TABLE_CLASS)

            products = []
            sales = []

            # Extract the product names and sales figures from the table
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 2:
                    product = cells[0].string.strip()
                    sale = float(cells[1].string.strip().replace(',', ''))
                    products.append(product)
                    sales.append(sale)

            # Calculate the percentage of total income for each product
            total_income = sum(sales)
            sales_percentages = [(product, sale / total_income * 100) for product, sale in zip(products, sales)]
            
            # Sort the sales percentages in descending order
            sales_percentages.sort(key=lambda x: x[1], reverse=True)
            
            # Return the top products and their sales percentages
            return sales_percentages[:TOP_PRODUCTS_COUNT]

    return []

if __name__ == "__main__":
    sales_percentages = scrape_sales_percentage("AMD")
    for product, percentage in sales_percentages:
        print(f"Product: {product}, Sales Percentage: {percentage:.2f}%")