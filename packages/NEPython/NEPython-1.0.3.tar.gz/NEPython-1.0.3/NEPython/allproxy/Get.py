import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from packaging import version
from concurrent.futures import ThreadPoolExecutor, as_completed

current_version = "1.2.2"

response = requests.get('https://pypi.org/pypi/allproxy/json')
web_version = response.json()["info"]["version"]

if version.parse(web_version) > version.parse(current_version):
    print("Hey there! Please update to the new version of allproxy by using pip install --upgrade allproxy!")

working = []
working_s = []

def combine_and_store(url):
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table with specified headers
            table = soup.find('table')

            if table:
                combined_data = []

                # Extract headers
                headers = [th.text.strip() for th in table.find_all('th')]
                header_indexes = [headers.index('IP Address'), headers.index('Port'), headers.index('Https')]

                # Extract data rows
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip the first row if it contains headers
                    row_data = [td.text.strip() for td in row.find_all('td')]

                    if row_data:
                        # Extract relevant data based on header indexes
                        extracted_data = [row_data[i] for i in header_indexes]

                        # Check if Https is "no" and combine IP and Port
                        if extracted_data[2].lower() == 'no':
                            combined_data.append(extracted_data[0] + ':' + extracted_data[1])
                            
                return combined_data

            else:
                return None  # Return None if table not found

        else:
            return None  # Return None if response status code is not 200

    except requests.RequestException as e:
        return None  # Return None if an error occurs
    
def combine_and_store_s(url):
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table with specified headers
            table = soup.find('table')

            if table:
                combined_data = []

                # Extract headers
                headers = [th.text.strip() for th in table.find_all('th')]
                header_indexes = [headers.index('IP Address'), headers.index('Port'), headers.index('Https')]

                # Extract data rows
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip the first row if it contains headers
                    row_data = [td.text.strip() for td in row.find_all('td')]

                    if row_data:
                        # Extract relevant data based on header indexes
                        extracted_data = [row_data[i] for i in header_indexes]

                        # Check if Https is "yes" and combine IP and Port
                        if extracted_data[2].lower() == 'yes':
                            combined_data.append(extracted_data[0] + ':' + extracted_data[1])
                            
                return combined_data

            else:
                return None  # Return None if table not found

        else:
            return None  # Return None if response status code is not 200

    except requests.RequestException as e:
        return None  # Return None if an error occurs

def check_proxie_reachable(urls):
    total_urls = len(urls)
    working = []

    def check_proxy(url):
        try:
            # Add 'http://' or 'https://' based on your needs
            full_url_with_protocol = 'http://' + url if not url.startswith('http') else url

            response = requests.get(full_url_with_protocol, timeout=5)
            if response.status_code == 200:
                working.append(url)

        except requests.RequestException as e:
            pass  # Handle exception if needed

    with tqdm(total=total_urls, desc="Checking Http Proxies", unit="proxy") as pbar:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_proxy, url) for url in urls]

            for _ in tqdm(as_completed(futures), total=len(futures), desc="Processing Http Proxies", unit="proxy"):
                pbar.update(1)

    return working

def check_proxie_reachable_s(urls):
    total_urls = len(urls)
    working = []

    def check_proxy_s(url):
        try:
            # Add 'http://' or 'https://' based on your needs
            full_url_with_protocol = 'https://' + url if not url.startswith('https') else url

            response = requests.get(full_url_with_protocol, timeout=5)
            if response.status_code == 200:
                working.append(url)

        except requests.RequestException as e:
            pass  # Handle exception if needed

    with tqdm(total=total_urls, desc="Checking Https Proxies", unit="proxy") as pbar:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_proxy_s, url) for url in urls]

            for _ in tqdm(as_completed(futures), total=len(futures), desc="Processing Https Proxies", unit="proxy"):
                pbar.update(1)

    return working

def get_proxies():
    website_url = 'https://free-proxy-list.net/'

    result_http = combine_and_store(website_url)
    if result_http:
        working_http_proxies = check_proxie_reachable(result_http)

        if working_http_proxies:
            pass
        else:
            print("No working http proxies found.")
            return None, None
    else:
        print("Failed to retrieve the page or table not found.")
        return None, None

    result_https = combine_and_store_s(website_url)
    if result_https:
        working_https_proxies = check_proxie_reachable_s(result_https)

        if working_https_proxies:
            return working_http_proxies, working_https_proxies
        else:
            print("No working https proxies found.")
            return working_http_proxies, None
    else:
        print("Failed to retrieve the page or table not found.")
        return working_http_proxies, None

def checkIpProxy():
    proxy = get_proxies()[0]
    print("Proxy:", proxy)

    try:
        res = requests.get("http://api.myip.com", proxies={"http": proxy}, timeout=5)
        print(res.text)
    except Exception as e:
        print("Error:", e)