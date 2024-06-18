import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import random
from db.db_connector import get_connection
from web_split.website_categorizer import WebsiteCategorizer

def configure_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=site-per-process')
    options.add_argument('--disable-features=FeaturePolicy')
    options.add_argument('--disable-features=EnableMediaRouterService')
    options.add_argument('--disable-features=AudioServiceOutOfProcess')
    options.add_argument('--disable-features=AudioServiceOutOfProcessByDefault')
    options.add_argument('--disable-features=SpeakerServiceOutOfProcess')
    options.add_argument('--disable-features=SpeakerServiceOutOfProcessByDefault')
    
    # Disable cookies
    prefs = {"profile.default_content_setting_values.cookies": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)
    return driver

def insert_into_db(query, data):
    connection = get_connection()
    inserted_id = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
            inserted_id = cursor.lastrowid
        connection.commit()
    except Exception as e:
        print(f"Error executing query: {query} with data: {data} - Error: {e}")
    finally:
        connection.close()
    return inserted_id

def extract_website_data(url, categorizer):
    try:
        connection = get_connection()
        
        # Use Selenium for dynamic content
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)  # wait to load completely

        # Check if the webste returns a "403 Forbidden" error
        if "403 Forbidden" in driver.page_source:
            print(f"Skipping {url} due to '403 Forbidden' error")
            meta_description = "403 Forbidden"
        else:
            # Meta title and description
            meta_title = driver.title
            meta_description = None
            try:
                meta_description = driver.find_element(By.NAME, 'description').get_attribute('content')
            except:
                pass
            
            # Fallback text for categorization if meta descrption is missing
            if not meta_description:
                meta_description = driver.page_source[:5000]  # Going bck to the first 5000 characters of the page source

        # Website language
        lang = 'unknown'  # if language is nt found insert
        try:
            lang_element = driver.find_element(By.TAG_NAME, 'html')
            lang = lang_element.get_attribute('lang')
        except:
            pass

        # Check if the website already exist
        check_query = "SELECT id FROM websites WHERE url = %s"
        with connection.cursor() as cursor:
            cursor.execute(check_query, (url,))
            result = cursor.fetchone()
        
        if result:
            print(f"Website already exists in the database: {url}")
            driver.quit()
            return
        
        # Insert website data
        website_query = "INSERT INTO websites (url, meta_title, meta_description, language) VALUES (%s, %s, %s, %s)"
        website_id = insert_into_db(website_query, (url, meta_title, meta_description, lang))
        
        if not website_id:
            print(f"Failed to insert or retrieve website_id for {url}. Skipping related data insertion.")
            driver.quit()
            return
        
        print(f"Retrieved website_id: {website_id}")
        
        # Social media links
        social_links = {}
        social_patterns = {
            'Facebook': r'https?://(www\.)?facebook\.com/\S+',
            'Twitter': r'https?://(www\.)?twitter\.com/\S+',
            'LinkedIn': r'https?://(www\.)?linkedin\.com/\S+',
            'Instagram': r'https?://(www\.)?instagram\.com/\S+'
        }

        page_source = driver.page_source
        for platform, pattern in social_patterns.items():
            match = re.search(pattern, page_source)
            if match:
                # Remove any characters like quotation marks or comma
                url = match.group(0).rstrip(',"')
                social_links[platform] = url
        
        for platform, link in social_links.items():
            try:
                print(f"Inserting social media link for {platform}: {link}")
                social_query = "INSERT INTO social_media_links (website_id, platform, url) VALUES (%s, %s, %s)"
                insert_into_db(social_query, (website_id, platform, link))
            except Exception as e:
                print(f"Failed to insert social media link: {e}")
        
        # Tech stack detector
        tech_stack = set()

        tech_stack_patterns = {
            'jquery': 'jQuery',
            'angular': 'AngularJS',
            'react': 'React',
            'vue': 'Vue.js',
            'bootstrap': 'Bootstrap',
            'typescript': 'TypeScript',
            'nodejs': 'Node.js',
            'django': 'Django',
            'flask': 'Flask',
            'laravel': 'Laravel',
            'wordpress': 'WordPress',
            'drupal': 'Drupal',
            'opencart': 'OpenCart',
            'woocommerce': 'WooCommerce',
            'express': 'Express.js',
            'ruby on rails': 'Ruby on Rails',
            'spring': 'Spring',
            'fastapi': 'FastAPI',
            'django-orm': 'Django ORM',
            'sqlalchemy': 'SQLAlchemy',
            'mongodb': 'MongoDB',
            'redis': 'Redis',
            'kafka': 'Kafka',
            'kubernetes': 'Kubernetes',
            'docker': 'Docker',
            'aws': 'AWS',
            'azure': 'Azure',
            'gcp': 'Google Cloud Platform',
            'firebase': 'Firebase',
            'react-native': 'React Native',
            'flutter': 'Flutter',
            'xamarin': 'Xamarin',
            'three.js': 'Three.js',
            'd3.js': 'D3.js',
            'chart.js': 'Chart.js'
       
        }

        scripts = driver.find_elements(By.TAG_NAME, 'script')
        for script in scripts:
            src = script.get_attribute('src')
            if src:
                for keyword, tech in tech_stack_patterns.items():
                    if keyword in src.lower():
                        tech_stack.add(tech)

        if tech_stack:
            try:
                for tech in tech_stack:
                    tech_query = "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)"
                    insert_into_db(tech_query, (website_id, tech))
            except Exception as e:
                print(f"Failed to insert technologies: {e}")

        
        # Payment gateways
        payment_gateways = []  # Init an empty list
        payment_patterns = [
                            'paypal', 'stripe', 'razorpay', 'worldpay', 'authorizenet', 
                            'shopify payments', '2checkout', 'payoneer', 'payza', 'skrill', 
                            'dwolla', 'adyen', 'alipay', 'klarna', 'bitpay', 'paddle', 
                            'amazon payments', 'braintree', 'venmo', 'internet banking',
                            # Credit card
                            'visa', 'mastercard', 'discover', 'american express', 'maestro',
                            'credit card', 'credit', 'EMI',
                            # UPI 
                            'upi', 'bhim', 'upi id', 'vpa',
                            #for Debit cards
                            'debit card', 'maestro', 'visa debit', 'mastercard debit'
                        ]

        for pattern in payment_patterns:
            if re.search(pattern, page_source, re.IGNORECASE):
                payment_gateways.append(pattern.capitalize())

        for gateway in payment_gateways:
            try:
                payment_query = "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)"
                insert_into_db(payment_query, (website_id, gateway))
            except Exception as e:
                print(f"Failed to insert payment gateway: {e}")

        # Clear the list after processing all gateways for currnt website
        payment_gateways = []
        
        # Determine category basd on meta description
        category = categorizer.categorize_website(meta_description)  # Categorize
        
        category_query = "UPDATE websites SET category=%s WHERE id=%s"
        try:
            insert_into_db(category_query, (category, website_id))
        except Exception as e:
            print(f"Failed to update category: {e}")
        
        driver.quit()
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    # Paths to the model
    model_path = "./models/model"
    tokenizer_path = "./models/tokenizer" #load token

    # Initialize the WebsiteCatgorizer with the model
    categorizer = WebsiteCategorizer(model_path, tokenizer_path)

    # Read the list of websites from websites.txt
    with open('websites.txt', 'r') as file:
        websites = [line.strip() for line in file.readlines()]
    
    for website in websites:
        extract_website_data(website, categorizer)
        time.sleep(random.uniform(1, 3))  # waiting 

if __name__ == "__main__":
    main()

### End of the story