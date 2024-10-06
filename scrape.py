import os
import time
import pdfkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

# Set up paths and options
chrome_driver_path = 'chromedriver-win64/chromedriver.exe'  # Update this to your ChromeDriver path
base_url = 'https://www.vit.edu/'
pdf_output_dir = 'vit_pages'

# Ensure PDF output directory exists
if not os.path.exists(pdf_output_dir):
    os.makedirs(pdf_output_dir)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

def save_page_as_pdf(page_url, pdf_filename):
    """Saves a web page as a PDF."""
    try:
        # Load the page
        driver.get(page_url)
        time.sleep(2)  # Wait for the page to fully load
        
        # Get the page title and convert it into a valid filename
        page_title = driver.title.strip().replace(" ", "_").replace("/", "_")
        pdf_path = os.path.join(pdf_output_dir, f"{page_title}.pdf")
        
        # Save the page as PDF using pdfkit
        pdfkit.from_url(page_url, pdf_path)
        print(f"Saved: {pdf_path}")
        
    except Exception as e:
        print(f"Failed to save {page_url} due to: {e}")

def extract_links_from_nav():
    """Extracts all links from the navigation bar."""
    links = []
    try:
        # Find all elements in the navigation bar
        nav_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav a")))
        
        # Get the href attribute of each link
        for element in nav_elements:
            href = element.get_attribute("href")
            if href and href.startswith("http"):  # Avoid non-absolute URLs
                links.append(href)
                
    except Exception as e:
        print(f"Error extracting navigation links: {e}")
    
    return links

def visit_departments_links(department_url):
    """Visit and save pages for each department."""
    driver.get(department_url)
    time.sleep(2)
    
    # Save the main department page
    save_page_as_pdf(department_url, department_url.split("/")[-1])

    # Find all department-specific links
    dept_nav_links = extract_links_from_nav()

    for dept_link in dept_nav_links:
        save_page_as_pdf(dept_link, dept_link.split("/")[-1])

def visit_all_pages(base_url):
    """Visits each page in the website and saves it as a PDF."""
    driver.get(base_url)
    time.sleep(2)  # Allow the page to load
    
    # Extract navigation links
    nav_links = extract_links_from_nav()

    for link in nav_links:
        if "departments" in link.lower():  # Special handling for department pages
            visit_departments_links(link)
        else:
            save_page_as_pdf(link, link.split("/")[-1])

if __name__ == "__main__":
    # Start from the base URL
    visit_all_pages(base_url)
    
    # Close the WebDriver session
    driver.quit()
