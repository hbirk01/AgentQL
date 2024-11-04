import agentql
from playwright.sync_api import sync_playwright
import pandas as pd
import time

# Define the AgentQL query
QUERY = """
{
    products[] {
        name
        price
    }
}
"""

def scrape_limited_products(max_products_per_page, max_pages):
    # Initialize an empty list to hold product data and counters for pages
    all_products = []
    page_count = 1  # Start at page 1

    with sync_playwright() as playwright:
        # Launch the browser
        browser = playwright.chromium.launch(headless=True)
        page = agentql.wrap(browser.new_page())

        # Starting URL (page 1)
        base_url = "https://medical-tools.com/shop/orthopedic-instruments"
        page.goto(base_url)
        print(f"Scraping Page {page_count}")

        while page_count <= max_pages:
            # Scrape the data on the current page
            response = page.query_data(QUERY)
            products = response.get('products', [])

            # Add up to max_products_per_page items from the current page
            page_products = []
            for product in products[:max_products_per_page]:  # Limit to the specified count per page
                page_products.append(product)
            all_products.extend(page_products)

            print(f"Page {page_count} scraped: {len(page_products)} products added.")

            # Check if we've reached the page limit
            page_count += 1
            if page_count > max_pages:
                break

            # Attempt to navigate to the next page
            next_button_href = page.eval_on_selector("a.action.next[title='Next']", "element => element.href")

            if next_button_href:
                print(f"Navigating to: {next_button_href}")
                page.goto(next_button_href)
                time.sleep(2)  # Delay to ensure the next page loads
            else:
                print("No 'Next' button found or pagination ended.")
                break

        # Convert the data to a DataFrame
        df = pd.DataFrame(all_products)

        # Save the data to an Excel file
        df.to_excel('limited_medical_products.xlsx', index=False)
        print("Data has been saved to limited_medical_products.xlsx")

        # Close the browser
        browser.close()

# Run the scraper to collect 3 products per page from up to 2 pages
if __name__ == "__main__":
    scrape_limited_products(max_products_per_page=3, max_pages=2)
