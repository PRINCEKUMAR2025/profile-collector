import sys
import csv
from playwright.sync_api import sync_playwright
import logging
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),          # Log to terminal
        logging.FileHandler('scraper.log')# Log to file
    ]
)
logger = logging.getLogger()

def scrape_linkedin(email, password, role, location, experience, max_pages, csv_filename):
    profile_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        context.set_default_timeout(30000)
        page = context.new_page()

        # Step 1: Manual Login
        logger.info("Navigate to LinkedIn login page and log in manually in the browser.")
        page.goto("https://www.linkedin.com/login", timeout=0)

        # Step 2: Wait for successful login (no terminal input needed)
        login_verified = False
        for _ in range(10):  # Try up to 10 times (adjust as needed)
            try:
                page.wait_for_selector(".global-nav__me", timeout=10000)  # 10s timeout per attempt
                login_verified = True
                logger.info("Login verified. Proceeding to search...")
                break
            except:
                logger.info("Waiting for manual login...")
                time.sleep(3)
        if not login_verified:
            logger.error("Login verification failed. Did you log in?")
            page.screenshot(path="login_error.png")
            logger.info("Saved login_error.png for inspection.")
            browser.close()
            return

        # Step 3: Navigate to search (with experience filter)
        search_query = f"{role} {experience} year of experience".strip().replace(" ", "%20")
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query}&location={location}"
        logger.info(f"Navigating to: {search_url}")
        page.goto(search_url, timeout=0)
        time.sleep(2)

        for page_num in range(1, max_pages + 1):
            logger.info(f"Processing page {page_num}...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(2, 4))

            anchors = page.query_selector_all('a[href*="/in/"]')
            for a in anchors:
                href = a.get_attribute('href')
                if href and '/in/' in href:
                    clean_url = href.split('?')[0]
                    if clean_url not in profile_urls:
                        profile_urls.add(clean_url)
                        logger.info(f"Added profile: {clean_url}")

            next_button = page.query_selector('button[aria-label="Next"]')
            if next_button and next_button.is_enabled():
                logger.info("Clicking next page...")
                next_button.click()
                time.sleep(random.uniform(3, 5))
            else:
                logger.info("No more pages or next button disabled.")
                break

        logger.info(f"Writing {len(profile_urls)} profile URLs to {csv_filename}")
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['linkedin_profile'])
            for url in profile_urls:
                writer.writerow([url])

        browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python scraper.py <email> <password> <role> <location> <experience> <max_pages> <csv_filename>")
        sys.exit(1)

    email, password, role, location, experience, max_pages, csv_filename = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7]
    scrape_linkedin(email, password, role, location, experience, max_pages, csv_filename)
