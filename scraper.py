import os
import subprocess

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import re
import datetime
import time

def setup_driver():
    options = Options()
    options.headless = True

    # Find and use the correct Firefox binary
    try:
        # Check for Firefox within the snap ecosystem
        snap_bin = subprocess.check_output(['snap', 'run', 'firefox', '--version'])
        options.binary_location = '/snap/bin/firefox'
        print("Using Snap Firefox binary at /snap/bin/firefox")
    except Exception as e:
        print("Defaulting to /usr/bin/firefox")
        options.binary_location = '/usr/bin/firefox'
    
    service = Service(log_path='geckodriver.log')
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def scrape_data(driver, page_id):
    url = f'https://aqarmap.com.eg/ar/listing/{page_id}-a/'
    try:
        driver.get(url)
        time.sleep(3)  # Wait for content to load
        return driver.page_source
    except Exception as e:
        print(f'Error fetching {url}:', e)
    return ''

def extract_contacts(page_content):
    phones = set(re.findall(r'\b\d{11}\b', page_content))
    emails = set(re.findall(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+', page_content))
    return phones, emails

def save_results(phones, emails):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    os.makedirs('results', exist_ok=True)
    with open(f'results/{timestamp}_phones.txt', 'w') as phone_file:
        phone_file.write('\n'.join(sorted(phones)))
    with open(f'results/{timestamp}_emails.txt', 'w') as email_file:
        email_file.write('\n'.join(sorted(emails)))

if __name__ == '__main__':
    driver = setup_driver()
    all_phones = set()
    all_emails = set()
    for i in range(1, 1001):
        print(f'Scraping page {i}...')
        content = scrape_data(driver, i)
        if content:
            phones, emails = extract_contacts(content)
            all_phones.update(phones)
            all_emails.update(emails)
            print(f'Page {i}: Found {len(phones)} phone numbers and {len(emails)} emails.')
        else:
            print(f'Page {i}: No content found.')
    save_results(all_phones, all_emails)
    driver.quit()
    print('Scraping complete. Results have been saved.')
