import requests
import re
import datetime

def scrape_data(page_id):
    url = f'https://aqarmap.com.eg/ar/listing/{page_id}-a/'
    try:
        response = requests.get(url)
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
    for i in range(1, 1001):
        content = scrape_data(i)
        if content:
            phones, emails = extract_contacts(content)
            all_phones.update(phones)
            all_emails.update(emails)
    save_results(all_phones, all_emails)
  
