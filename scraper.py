import sys
import csv
import json
import pandas as pd
from playwright.sync_api import sync_playwright
import logging
import time
import random
import os
import re
from urllib.parse import quote_plus, urlencode

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

class LinkedInAdvancedScraper:
    def __init__(self, search_params):
        self.search_params = search_params
        self.profile_data = []
        self.profile_urls = set()
        
    def build_advanced_search_url(self):
        """Build LinkedIn search URL with proper advanced filters"""
        base_url = "https://www.linkedin.com/search/results/people/"
        
        # Initialize query parameters
        query_params = {}
        
        # Build keywords from job roles and skills
        keywords = []
        if self.search_params.get('job_roles'):
            keywords.extend(self.search_params['job_roles'])
        
        if self.search_params.get('skills'):
            keywords.extend(self.search_params['skills'])
        
        # Combine keywords with proper spacing
        if keywords:
            keyword_query = " ".join(keywords)
            query_params['keywords'] = keyword_query
        
        # Add location filter (LinkedIn uses 'location' parameter)
        if self.search_params.get('locations'):
            location_query = " ".join(self.search_params['locations'])
            query_params['location'] = location_query
        
        # Add company filter (LinkedIn uses 'company' parameter)
        if self.search_params.get('companies'):
            company_query = " ".join(self.search_params['companies'])
            query_params['company'] = company_query
        
        # Add industry filter (LinkedIn uses 'industry' parameter)
        if self.search_params.get('industries'):
            industry_query = " ".join(self.search_params['industries'])
            query_params['industry'] = industry_query
        
        # Add experience level filter (LinkedIn uses 'experience' parameter)
        if self.search_params.get('experience_levels'):
            experience_query = " ".join(self.search_params['experience_levels'])
            query_params['experience'] = experience_query
        
        # Add education filter (LinkedIn uses 'education' parameter)
        if self.search_params.get('education_levels'):
            education_query = " ".join(self.search_params['education_levels'])
            query_params['education'] = education_query
        
        # Add company size filter (LinkedIn uses 'companySize' parameter)
        if self.search_params.get('company_sizes'):
            company_size_query = " ".join(self.search_params['company_sizes'])
            query_params['companySize'] = company_size_query
        
        # Add connection degree filter
        if self.search_params.get('min_connections', 0) > 0:
            query_params['connectionOf'] = "F"  # First connections
            query_params['network'] = "F"       # First network
        
        # Add profile language filter (optional)
        query_params['profileLanguage'] = "en"  # English profiles
        
        # Add result type filter
        query_params['resultType'] = "PEOPLE"   # People results only
        
        # Build the final URL
        if query_params:
            # Encode each parameter properly
            encoded_params = []
            for key, value in query_params.items():
                if value:
                    encoded_key = quote_plus(key)
                    encoded_value = quote_plus(str(value))
                    encoded_params.append(f"{encoded_key}={encoded_value}")
            
            url = f"{base_url}?{'&'.join(encoded_params)}"
        else:
            url = base_url
        
        logger.info(f"Built optimized search URL: {url}")
        logger.info(f"Search parameters: {query_params}")
        
        return url
    
    def apply_advanced_filters(self, page):
        """Apply advanced LinkedIn filters using the interface for better targeting"""
        try:
            logger.info("Applying advanced LinkedIn filters for targeted results...")
            
            # Wait for filters to load
            time.sleep(3)
            
            # Try multiple selector patterns for the filters button
            filter_selectors = [
                'button[aria-label="All filters"]',
                'button:has-text("All filters")',
                'button:has-text("Filters")',
                '[data-control-name="all_filters"]',
                'button[class*="filter"]',
                'button[class*="search"]',
                'button[class*="advanced"]'
            ]
            
            all_filters_button = None
            for selector in filter_selectors:
                try:
                    all_filters_button = page.query_selector(selector)
                    if all_filters_button:
                        logger.info(f"Found filters button with selector: {selector}")
                        break
                except:
                    continue
            
            if all_filters_button:
                all_filters_button.click()
                time.sleep(3)
                logger.info("Opened all filters panel")
                
                # Apply company size filters
                if self.search_params.get('company_sizes'):
                    self._apply_company_size_filters(page)
                
                # Apply experience level filters
                if self.search_params.get('experience_levels'):
                    self._apply_experience_filters(page)
                
                # Apply education filters
                if self.search_params.get('education_levels'):
                    self._apply_education_filters(page)
                
                # Apply industry filters
                if self.search_params.get('industries'):
                    self._apply_industry_filters(page)
                
                # Apply connection filters
                if self.search_params.get('min_connections', 0) > 0:
                    self._apply_connection_filters(page)
                
                # Try multiple selectors for the show results button
                show_results_selectors = [
                    'button[aria-label="Apply current filters to show results"]',
                    'button:has-text("Show results")',
                    'button:has-text("Apply")',
                    'button[class*="apply"]',
                    'button[class*="show"]',
                    'button[class*="results"]'
                ]
                
                show_results_button = None
                for selector in show_results_selectors:
                    try:
                        show_results_button = page.query_selector(selector)
                        if show_results_button:
                            logger.info(f"Found show results button with selector: {selector}")
                            break
                    except:
                        continue
                
                if show_results_button:
                    show_results_button.click()
                    time.sleep(5)
                    logger.info("Applied advanced filters for targeted results")
                else:
                    logger.warning("Could not find 'Show results' button")
            else:
                logger.info("All filters button not found, using basic search with URL parameters")
                
        except Exception as e:
            logger.warning(f"Error applying advanced filters: {e}")
    
    def _apply_connection_filters(self, page):
        """Apply connection degree filters"""
        try:
            connection_section = page.query_selector('text="Connection of"')
            if connection_section:
                connection_section.click()
                time.sleep(1)
                
                # Try to select "1st" connections
                first_connection = page.query_selector('input[value="1st"]')
                if first_connection:
                    first_connection.check()
                    logger.info("Applied 1st connection filter")
                else:
                    logger.warning("Could not find 1st connection filter")
        except Exception as e:
            logger.warning(f"Error applying connection filters: {e}")
    
    def _apply_company_size_filters(self, page):
        """Apply company size filters"""
        try:
            company_size_section = page.query_selector('text="Company size"')
            if company_size_section:
                company_size_section.click()
                time.sleep(1)
                
                for size in self.search_params.get('company_sizes', []):
                    size_checkbox = page.query_selector(f'input[value="{size}"]')
                    if size_checkbox:
                        size_checkbox.check()
                        logger.info(f"Applied company size filter: {size}")
        except Exception as e:
            logger.warning(f"Error applying company size filters: {e}")
    
    def _apply_experience_filters(self, page):
        """Apply experience level filters"""
        try:
            experience_section = page.query_selector('text="Experience level"')
            if experience_section:
                experience_section.click()
                time.sleep(1)
                
                for level in self.search_params.get('experience_levels', []):
                    level_checkbox = page.query_selector(f'input[value="{level}"]')
                    if level_checkbox:
                        level_checkbox.check()
                        logger.info(f"Applied experience filter: {level}")
        except Exception as e:
            logger.warning(f"Error applying experience filters: {e}")
    
    def _apply_education_filters(self, page):
        """Apply education filters"""
        try:
            education_section = page.query_selector('text="Education"')
            if education_section:
                education_section.click()
                time.sleep(1)
                
                for education in self.search_params.get('education_levels', []):
                    education_checkbox = page.query_selector(f'input[value="{education}"]')
                    if education_checkbox:
                        education_checkbox.check()
                        logger.info(f"Applied education filter: {education}")
        except Exception as e:
            logger.warning(f"Error applying education filters: {e}")
    
    def _apply_industry_filters(self, page):
        """Apply industry filters"""
        try:
            industry_section = page.query_selector('text="Industry"')
            if industry_section:
                industry_section.click()
                time.sleep(1)
                
                for industry in self.search_params.get('industries', []):
                    industry_checkbox = page.query_selector(f'input[value="{industry}"]')
                    if industry_checkbox:
                        industry_checkbox.check()
                        logger.info(f"Applied industry filter: {industry}")
        except Exception as e:
            logger.warning(f"Error applying industry filters: {e}")
    
    def find_profile_elements(self, page):
        """Find profile elements using multiple selector strategies"""
        profile_elements = []
        
        # Strategy 1: Try the standard LinkedIn selectors
        selectors = [
            'li[class*="entity-result__item"]',
            'li[class*="search-result"]',
            'li[class*="result-item"]',
            'li[class*="profile"]',
            'div[class*="entity-result__item"]',
            'div[class*="search-result"]',
            'div[class*="result-item"]',
            'div[class*="profile"]'
        ]
        
        for selector in selectors:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    logger.info(f"Found {len(elements)} profile elements with selector: {selector}")
                    profile_elements = elements
                    break
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue
        
        # Strategy 2: If no elements found, try finding by profile links
        if not profile_elements:
            try:
                profile_links = page.query_selector_all('a[href*="/in/"]')
                if profile_links:
                    logger.info(f"Found {len(profile_links)} profile links")
                    # Create wrapper elements for the links
                    profile_elements = profile_links
            except Exception as e:
                logger.debug(f"Profile links search failed: {e}")
        
        # Strategy 3: Look for any elements containing profile information
        if not profile_elements:
            try:
                # Look for elements with common profile text patterns
                profile_containers = page.query_selector_all('div, li, article')
                for container in profile_containers:
                    try:
                        text = container.inner_text()
                        if any(keyword in text.lower() for keyword in ['connect', 'message', 'follow', 'view profile']):
                            profile_elements.append(container)
                    except:
                        continue
                
                if profile_elements:
                    logger.info(f"Found {len(profile_elements)} potential profile containers")
            except Exception as e:
                logger.debug(f"Profile container search failed: {e}")
        
        return profile_elements
    
    def extract_profile_data(self, page, profile_element):
        """Extract detailed profile information"""
        try:
            profile_data = {
                'linkedin_profile': '',
                'name': '',
                'headline': '',
                'location': '',
                'company': '',
                'connection_degree': '',
                'mutual_connections': '',
                'profile_views': ''
            }
            
            # Extract profile URL - try multiple strategies
            profile_link = None
            link_selectors = [
                'a[href*="/in/"]',
                'a[href*="linkedin.com/in/"]',
                'a[class*="profile"]',
                'a[class*="name"]'
            ]
            
            for selector in link_selectors:
                try:
                    profile_link = profile_element.query_selector(selector)
                    if profile_link:
                        break
                except:
                    continue
            
            if profile_link:
                href = profile_link.get_attribute('href')
                if href and '/in/' in href:
                    clean_url = href.split('?')[0]
                    if not clean_url.startswith('http'):
                        clean_url = 'https://www.linkedin.com' + clean_url
                    profile_data['linkedin_profile'] = clean_url
            
            # Extract name - try multiple strategies
            name_selectors = [
                'span[aria-hidden="true"]',
                'span[class*="name"]',
                'a[class*="name"]',
                'div[class*="name"]',
                'h3',
                'h4',
                'strong'
            ]
            
            for selector in name_selectors:
                try:
                    name_element = profile_element.query_selector(selector)
                    if name_element:
                        name_text = name_element.inner_text().strip()
                        if name_text and len(name_text) < 100:  # Reasonable name length
                            profile_data['name'] = name_text
                            break
                except:
                    continue
            
            # Extract headline - try multiple strategies
            headline_selectors = [
                'div[class*="entity-result__primary-subtitle"]',
                'div[class*="headline"]',
                'div[class*="title"]',
                'span[class*="headline"]',
                'p[class*="headline"]',
                'div[class*="subtitle"]'
            ]
            
            for selector in headline_selectors:
                try:
                    headline_element = profile_element.query_selector(selector)
                    if headline_element:
                        headline_text = headline_element.inner_text().strip()
                        if headline_text and len(headline_text) < 200:  # Reasonable headline length
                            profile_data['headline'] = headline_text
                            break
                except:
                    continue
            
            # Extract location - try multiple strategies
            location_selectors = [
                'div[class*="entity-result__secondary-subtitle"]',
                'div[class*="location"]',
                'span[class*="location"]',
                'div[class*="subtitle"]',
                'span[class*="subtitle"]'
            ]
            
            for selector in location_selectors:
                try:
                    location_element = profile_element.query_selector(selector)
                    if location_element:
                        location_text = location_element.inner_text().strip()
                        if location_text and len(location_text) < 100:  # Reasonable location length
                            profile_data['location'] = location_text
                            break
                except:
                    continue
            
            # Extract company - try multiple strategies
            company_selectors = [
                'div[class*="entity-result__primary-subtitle"] span',
                'div[class*="company"]',
                'span[class*="company"]',
                'div[class*="organization"]',
                'span[class*="organization"]'
            ]
            
            for selector in company_selectors:
                try:
                    company_element = profile_element.query_selector(selector)
                    if company_element:
                        company_text = company_element.inner_text().strip()
                        if company_text and len(company_text) < 100:  # Reasonable company length
                            profile_data['company'] = company_text
                            break
                except:
                    continue
            
            # Extract connection degree and mutual connections
            connection_selectors = [
                'span[class*="entity-result__secondary-subtitle"]',
                'span[class*="connection"]',
                'div[class*="connection"]',
                'span[class*="network"]',
                'div[class*="network"]'
            ]
            
            for selector in connection_selectors:
                try:
                    connection_element = profile_element.query_selector(selector)
                    if connection_element:
                        connection_text = connection_element.inner_text().strip()
                        if 'connection' in connection_text.lower():
                            profile_data['connection_degree'] = connection_text
                        elif 'mutual' in connection_text.lower():
                            profile_data['mutual_connections'] = connection_text
                except:
                    continue
            
            return profile_data
            
        except Exception as e:
            logger.warning(f"Error extracting profile data: {e}")
            return profile_data
    
    def validate_search_results(self, page):
        """Validate that search results match our criteria"""
        try:
            logger.info("Validating search results match our criteria...")
            
            # Check if we're on the right page
            current_url = page.url
            if "search/results/people" not in current_url:
                logger.warning("Not on people search results page")
                return False
            
            # Check page title for search confirmation
            page_title = page.title()
            if "Search" not in page_title and "Results" not in page_title:
                logger.warning("Page title doesn't indicate search results")
                return False
            
            # Look for search result indicators
            search_indicators = [
                'search-result',
                'entity-result',
                'profile-card',
                'people-result'
            ]
            
            found_indicators = []
            for indicator in search_indicators:
                try:
                    elements = page.query_selector_all(f'[class*="{indicator}"]')
                    if elements:
                        found_indicators.append(indicator)
                except:
                    continue
            
            if found_indicators:
                logger.info(f"Found search result indicators: {', '.join(found_indicators)}")
                return True
            else:
                logger.warning("No search result indicators found")
                return False
                
        except Exception as e:
            logger.warning(f"Error validating search results: {e}")
            return False
    
    def filter_relevant_profiles(self, profile_data):
        """Filter profiles to ensure they match our search criteria"""
        if not profile_data:
            return profile_data
        
        filtered_profiles = []
        search_criteria = {
            'job_roles': [role.lower() for role in self.search_params.get('job_roles', [])],
            'locations': [loc.lower() for loc in self.search_params.get('locations', [])],
            'companies': [comp.lower() for comp in self.search_params.get('companies', [])],
            'industries': [ind.lower() for ind in self.search_params.get('industries', [])]
        }
        
        for profile in profile_data:
            relevance_score = 0
            profile_text = f"{profile.get('name', '')} {profile.get('headline', '')} {profile.get('company', '')} {profile.get('location', '')}".lower()
            
            # Check job role relevance
            for role in search_criteria['job_roles']:
                if role in profile_text:
                    relevance_score += 2
                    break
            
            # Check location relevance
            for location in search_criteria['locations']:
                if location in profile_text:
                    relevance_score += 2
                    break
            
            # Check company relevance
            for company in search_criteria['companies']:
                if company in profile_text:
                    relevance_score += 3
                    break
            
            # Check industry relevance
            for industry in search_criteria['industries']:
                if industry in profile_text:
                    relevance_score += 1
                    break
            
            # Only include profiles with minimum relevance
            if relevance_score >= 2:
                profile['relevance_score'] = relevance_score
                filtered_profiles.append(profile)
                logger.info(f"Profile {profile.get('name', 'Unknown')} - Relevance: {relevance_score}")
            else:
                logger.debug(f"Filtered out profile {profile.get('name', 'Unknown')} - Relevance: {relevance_score}")
        
        logger.info(f"Filtered {len(filtered_profiles)} relevant profiles from {len(profile_data)} total")
        return filtered_profiles
    
    def scrape_linkedin(self):
        """Main scraping function with advanced features"""
        profile_urls = set()
        profile_data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False, 
                slow_mo=self.search_params.get('delay_min', 100)
            )
            context = browser.new_context()
            context.set_default_timeout(30000)
            page = context.new_page()

            # Step 1: Manual Login
            logger.info("Navigate to LinkedIn login page and log in manually in the browser.")
            page.goto("https://www.linkedin.com/login", timeout=0)

            # Step 2: Wait for successful login (no terminal input needed)
            login_verified = False
            for _ in range(15):  # Increased attempts for premium accounts
                try:
                    page.wait_for_selector(".global-nav__me", timeout=10000)
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

            # Step 3: Navigate to advanced search
            search_url = self.build_advanced_search_url()
            logger.info(f"Navigating to: {search_url}")
            page.goto(search_url, timeout=0)
            time.sleep(5)  # Increased wait time

            # Step 4: Apply advanced filters if enabled
            if self.search_params.get('use_advanced_filters', True):
                self.apply_advanced_filters(page)

            # Step 5: Validate search results
            if not self.validate_search_results(page):
                logger.warning("Search results validation failed. Taking screenshot for debugging.")
                page.screenshot(path="search_validation_failed.png")
                logger.info("Saved search validation screenshot")
                
                # Try to refresh and validate again
                page.reload()
                time.sleep(5)
                if not self.validate_search_results(page):
                    logger.error("Search validation failed after refresh. Check search parameters.")
                    browser.close()
                    return

            # Step 6: Scrape profiles from multiple pages
            for page_num in range(1, self.search_params.get('pages', 10) + 1):
                logger.info(f"Processing page {page_num}...")
                
                # Wait for page to load
                time.sleep(3)
                
                # Scroll to load more profiles
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(self.search_params.get('scroll_pause', 3))
                
                # Scroll back up to see all profiles
                page.evaluate("window.scrollTo(0, 0)")
                time.sleep(2)
                
                # Wait for profiles to load
                time.sleep(random.uniform(
                    self.search_params.get('delay_min', 3),
                    self.search_params.get('delay_max', 6)
                ))

                # Find all profile elements using multiple strategies
                profile_elements = self.find_profile_elements(page)
                
                if not profile_elements:
                    logger.warning(f"No profile elements found on page {page_num}")
                    # Take a screenshot for debugging
                    page.screenshot(path=f"page_{page_num}_no_profiles.png")
                    logger.info(f"Saved screenshot: page_{page_num}_no_profiles.png")
                    continue
                
                logger.info(f"Found {len(profile_elements)} profile elements on page {page_num}")
                
                for i, profile_element in enumerate(profile_elements):
                    try:
                        # Extract profile data
                        if self.search_params.get('include_profile_data', False):
                            profile_info = self.extract_profile_data(page, profile_element)
                            if profile_info['linkedin_profile']:
                                profile_data.append(profile_info)
                                profile_urls.add(profile_info['linkedin_profile'])
                                logger.info(f"Added profile {i+1}: {profile_info['name']} - {profile_info['linkedin_profile']}")
                        else:
                            # Just extract URLs
                            anchors = profile_element.query_selector_all('a[href*="/in/"]')
                            for a in anchors:
                                href = a.get_attribute('href')
                                if href and '/in/' in href:
                                    clean_url = href.split('?')[0]
                                    if not clean_url.startswith('http'):
                                        clean_url = 'https://www.linkedin.com' + clean_url
                                    if clean_url not in profile_urls:
                                        profile_urls.add(clean_url)
                                        logger.info(f"Added profile {i+1}: {clean_url}")
                    except Exception as e:
                        logger.warning(f"Error processing profile element {i+1}: {e}")
                        continue

                # Navigate to next page
                next_button = page.query_selector('button[aria-label="Next"]')
                if next_button and next_button.is_enabled():
                    logger.info("Clicking next page...")
                    next_button.click()
                    time.sleep(random.uniform(
                        self.search_params.get('delay_min', 4),
                        self.search_params.get('delay_max', 7)
                    ))
                else:
                    logger.info("No more pages or next button disabled.")
                    break

            # Step 7: Filter profiles for relevance
            if self.search_params.get('include_profile_data', False) and profile_data:
                logger.info("Filtering profiles for relevance...")
                profile_data = self.filter_relevant_profiles(profile_data)
                
                # Update profile URLs to only include relevant profiles
                profile_urls.clear()
                for profile in profile_data:
                    if profile.get('linkedin_profile'):
                        profile_urls.add(profile['linkedin_profile'])

            # Step 8: Export data in multiple formats
            self.export_data(profile_urls, profile_data)
            
            browser.close()

    def export_data(self, profile_urls, profile_data):
        """Export data in multiple formats"""
        csv_filename = self.search_params.get('csv_filename', 'candidates.csv')
        export_format = self.search_params.get('export_format', 'CSV')
        
        # Ensure CSV filename has correct extension
        if not csv_filename.endswith('.csv'):
            csv_filename += '.csv'
        
        base_filename = csv_filename.replace('.csv', '')
        
        if export_format == 'CSV' or export_format == 'All':
            # Export as CSV
            if self.search_params.get('include_profile_data', False) and profile_data:
                # Export detailed profile data
                df = pd.DataFrame(profile_data)
                df.to_csv(csv_filename, index=False, encoding='utf-8')
                logger.info(f"Exported {len(profile_data)} detailed profiles to {csv_filename}")
            else:
                # Export just URLs
                with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['linkedin_profile'])
                    for url in profile_urls:
                        writer.writerow([url])
                logger.info(f"Exported {len(profile_urls)} profile URLs to {csv_filename}")
        
        if export_format == 'JSON' or export_format == 'All':
            # Export as JSON
            json_filename = f"{base_filename}.json"
            if self.search_params.get('include_profile_data', False) and profile_data:
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(profile_data, f, indent=2, ensure_ascii=False)
                logger.info(f"Exported {len(profile_data)} detailed profiles to {json_filename}")
            else:
                data = {'profiles': list(profile_urls)}
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Exported {len(profile_urls)} profile URLs to {json_filename}")
        
        if export_format == 'Excel' or export_format == 'All':
            # Export as Excel
            try:
                excel_filename = f"{base_filename}.xlsx"
                if self.search_params.get('include_profile_data', False) and profile_data:
                    df = pd.DataFrame(profile_data)
                    df.to_excel(excel_filename, index=False, engine='openpyxl')
                    logger.info(f"Exported {len(profile_data)} detailed profiles to {excel_filename}")
                else:
                    df = pd.DataFrame(list(profile_urls), columns=['linkedin_profile'])
                    df.to_excel(excel_filename, index=False, engine='openpyxl')
                    logger.info(f"Exported {len(profile_urls)} profile URLs to {excel_filename}")
            except ImportError:
                logger.warning("openpyxl not installed. Skipping Excel export.")
            except Exception as e:
                logger.error(f"Error exporting to Excel: {e}")

def main():
    """Main function to run the scraper"""
    # Check if search parameters file exists
    if not os.path.exists("search_params.json"):
        logger.error("search_params.json not found. Please run the Streamlit app first.")
        sys.exit(1)
    
    # Load search parameters
    try:
        with open("search_params.json", "r") as f:
            search_params = json.load(f)
        logger.info("Loaded search parameters successfully")
    except Exception as e:
        logger.error(f"Error loading search parameters: {e}")
        sys.exit(1)
    
    # Create scraper instance
    scraper = LinkedInAdvancedScraper(search_params)
    
    # Start scraping
    try:
        scraper.scrape_linkedin()
        logger.info("Scraping completed successfully!")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()