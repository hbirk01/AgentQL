import agentql
from playwright.sync_api import sync_playwright
import pandas as pd

# Define the AgentQL query
QUERY = """
{
    products[] {
        name
        price
    }
}
"""

# Function to scrape data from the specified page
def scrape_medical_products():
    with sync_playwright() as playwright:
        # Launch the browser
        browser = playwright.chromium.launch(headless=True)
        page = agentql.wrap(browser.new_page())

        # Navigate to the medical products page
        page.goto("https://medical-tools.com/shop/orthopedic-instruments")

        # Use AgentQL to fetch product data
        response = page.query_data(QUERY)

        # Extract product data from the response
        products = response.get('products', [])
        if not products:
            print("No products found.")
            return

        # Convert the data into a DataFrame
        df = pd.DataFrame(products)

        # Save the data to an Excel file
        df.to_excel('medical_products.xlsx', index=False)
        print("Data has been saved to medical_products.xlsx")

        # Close the browser
        browser.close()

# Run the scraper
if __name__ == "__main__":
    scrape_medical_products()
