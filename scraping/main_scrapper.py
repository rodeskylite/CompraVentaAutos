import logging
import time
import random
from bs4 import BeautifulSoup
import requests
from requests.exceptions import InvalidSchema, ConnectionError

logging.basicConfig(
    level=logging.ERROR,
    format='[%(name)s] [%(levelname)s] [%(asctime)s] - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.52 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.68 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.74 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5538.80 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5595.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5648.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5701.91 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5754.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5807.97 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5860.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5913.103 Safari/537.36',
]

PROXIES = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080',
    'http://proxy4.example.com:8080',
    'http://proxy5.example.com:8080',
    'http://proxy6.example.com:8080',
    'http://proxy7.example.com:8080',
    'http://proxy8.example.com:8080',
    'http://proxy9.example.com:8080',
    'http://proxy10.example.com:8080',
    'http://proxy11.example.com:8080',
    'http://proxy12.example.com:8080',
    'http://proxy13.example.com:8080',
    'http://proxy14.example.com:8080',
    'http://proxy15.example.com:8080',
    'http://proxy16.example.com:8080',
    'http://proxy17.example.com:8080',
    'http://proxy18.example.com:8080',
    'http://proxy19.example.com:8080',
    'http://proxy20.example.com:8080',
]

def get_html(url: str) -> str:
    """Get html code from a URL.
    Args:
        url: URL to visit.
    Return:
        HTML code.
    """
    if not url.startswith(('http://', 'https://')):
        logger.error("Invalid URL: %s", url)
        return ""

    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }

    for _ in range(5):  # Retry up to 5 times
        proxy = {'http': random.choice(PROXIES), 'https': random.choice(PROXIES)}
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text
        except InvalidSchema:
            logger.error("Invalid schema for URL: %s", url)
            return ""
        except ConnectionError:
            logger.error("Connection error while accessing URL: %s", url)
            time.sleep(random.uniform(1, 3))  # Wait before retrying
        except requests.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
            return ""
        except Exception as err:
            logger.error("An error occurred: %s", err)
            return ""

    logger.error("Failed to retrieve URL after multiple attempts: %s", url)
    return ""

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scrape car data.')
    parser.add_argument('--page', type=int, required=True, help='Starting page number to scrape')
    parser.add_argument('--pagination_limit', type=int, required=True, help='Number of pages to scrape')

    args = parser.parse_args()

    base_url = "https://www.chileautos.cl/vehiculos/?q=Servicio.chileautos.&offset="

    for page in range(args.page, args.page + args.pagination_limit):
        offset = (page - 1) * 12
        url = f"{base_url}{offset}"
        logger.info("Scraping page [%s] with offset [%s]", page, offset)
        html = get_html(url)
        if html:
            # Process the HTML content
            pass
        else:
            logger.error("PAGINATION ERROR")
        time.sleep(random.uniform(1, 3))  # Add random delay to avoid rate limiting

if __name__ == "__main__":
    main()