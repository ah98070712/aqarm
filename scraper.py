import requests
import re
import datetime
import time

def scrape_data(page_id):
    url = f'https://140online.com/Company.aspx?CompanyId=NW{page_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        print(f'Page {page_id} status code: {response.status_code}')
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(f'Error fetching {url}:', e)
    return ''

def extract_contacts(page_content):
    phones = set(re.findall(r'\b\d{11}\b', page_content))
    emails = set(re.findall(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+', page_content))
    return phones, emails

def save_results(phones, emails):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open(f'results/{timestamp}_phones.txt', 'w') as phone_file:
        phone_file.write('\n'.join(sorted(phones)))
    with open(f'results/{timestamp}_emails.txt', 'w') as email_file:
        email_file.write('\n'.join(sorted(emails)))

if __name__ == '__main__':
    all_phones = set()
    all_emails = set()
    for i in range(7609, 7620):
        print(f'Scraping page {i}...')
        content = scrape_data(i)
        if content:
            phones, emails = extract_contacts(content)
            all_phones.update(phones)
            all_emails.update(emails)
            print(f'Page {i}: Found {len(phones)} phone numbers and {len(emails)} emails.')
        else:
            print(f'Page {i}: No content found.')
        time.sleep(2)  # Delay to be polite to the server
    save_results(all_phones, all_emails)
    print('Scraping complete. Results have been saved.')
