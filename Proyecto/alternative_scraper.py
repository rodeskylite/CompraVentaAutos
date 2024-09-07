
import logging

from bs4 import BeautifulSoup
import requests
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError

logging.basicConfig(
    level=logging.ERROR,
    format='[%(name)s] [%(levelname)s] [%(asctime)s] - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_html(url: str) -> str:
    """Get html code from a URL.
    Args:
        url: URL to visit.
    Return:
        HTML code.
    """
    headers = {
        # ":authority": "www.chileautos.cl",
        # ":method": "GET",
        # ":path": "/vehiculos/autos-veh%C3%ADculo/?offset=0",
        # ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5",
        "cookie": "__qca=I0-784578517-1725717682794; optimizelyEndUserId=oeu1723849895335r0.23152365560038102; csnclientid=67425BD7-D07C-6B68-0619-FF246AC9252F-CF9F0944-DC5C-4399-B401-4505C2C8C367-1723849895777; cidgenerated=client; gaclientId=1058421002.1723849897; _fbp=fb.1.1723849896899.34329523970709420; usprivacy=1N--; AMCV_72FF3B526128B17A0A495F9B%40AdobeOrg=MCMID|02206876517326689881733491416567740416; _hjSessionUser_620944=eyJpZCI6IjkyYzZjYTQ2LWU4Y2UtNTExNy04NDNhLTlmMDQwMDgxNjA0OSIsImNyZWF0ZWQiOjE3MjM4NDk5MTIzMDMsImV4aXN0aW5nIjpmYWxzZX0=; DeviceId=b432765b-4316-4904-b687-8b2883e06bdc; csncidcf=C639DF58-58A7-4D27-921D-181E1ACFC7CD; csn.bi=1725716973686; _gid=GA1.2.825800359.1725716974; kndctr_72FF3B526128B17A0A495F9B_AdobeOrg_identity=CiYwMjIwNjg3NjUxNzMyNjY4OTg4MTczMzQ5MTQxNjU2Nzc0MDQxNlISCLTn1-uVMhABGAEqA1ZBNjAA8AGVoP3lnDI=; kndctr_72FF3B526128B17A0A495F9B_AdobeOrg_cluster=va6; a360Fb=true; cmp.ret.enq.afgtoken=CfDJ8Efs2BAxx71EoBhTrHnI3sPkYnNKcT5AO68ejDfBDQQyAGBT0XL7QOtjuan9rJunZ7_TGgDFgc8vKvJicYo0JW_Kzf4vu9wdYZpJAl9XPiEjYQ-uv7njI3pAyB7-r2JVGMzCHJHwVaLGJlntJaSyXaw; __gads=ID=6ee97ab56597a544:T=1723849898:RT=1725717432:S=ALNI_MbF-jJeG2eKPivC9sY5WIXxoOTBbQ; __gpi=UID=00000a4cc62e0846:T=1723849898:RT=1725717432:S=ALNI_MZ8EQHop9a9-qFDi7cFZ08KgieY9g; __eoi=ID=2414fc85d4deae9d:T=1723849898:RT=1725717432:S=AA-AfjaOPC8dAYBdFNm9lPmpbS50; g_state={\"i_p\":1725724641267,\"i_l\":1}; datadome=jX7ZhXte7XUJQ0sI0nVjMYq4d7p9pDndGzrX4Qe~r7YRr61RtQnKTZ_2fVnZYByIuuNkI3Hr8N5DJ8rRZW~wNrpBFLEjTZjdIsu6KgQamHK2S75_Mu4ima3Puj2fXygr; csnSessionId=N%2BpNPHrqDE6B2F88U0M2ZwAAFWKU1OutWL22TPDCmvT35PU7F0qDUR1%2FgIhlmTkE9DLWFw%3D%3D; cto_bundle=4meHCF9yMEFNQUJES0JDcGp6bHNpcjdUc01UbmNsTloyYzFLQXJZTTdGNlQ1ODZKVDl5QTVQdnZWRFMwam1NQWExQ0lXb2ZJN04zOHhYZXdHMkRTNVZ0Rm9ZZTA2RmtmNjNXWHZkelZXJTJCckt5dGx2SFdUUGFWSjBsaXk4SjV3a0tOY09MNVNFWXBOemEwakV6OHhvZmpTbUI1QSUzRCUzRA; cto_bidid=9x4ZBF8wbzN3c1ZRbGZXUUt2bDlWNmklMkJ0QnQ0Rk9aSHZKUjVXeCUyQkRDUFEzZklmcVAzUU9leEplJTJGNHZVRHpiTk5zRm5wSm5xUlZHeWlQN1h2RjElMkJacXhhekQ4VmtDZW0weGdyRm1TU2t5aGVsZWo0JTNE; cto_dna_bundle=4kHnVF9yMEFNQUJES0JDcGp6bHNpcjdUc01SZFB4cTF0QkZJYWVaOWZLVkl6MTBtNWtBUlFnVGtCWXJhSEhDOSUyRktUJTJCSkRpRkozNzM0dXd1SEhrMFdZWFM5dnclM0QlM0Q; _gat_csn=1; FCNEC=%5B%5B%22AKsRol8uR_6DwMw-K2yk_iNDscAEW8DVVaY2YJmDZ-yV2zwKzGup9Y8EzkOwmFx62Ap68NZdYstRck9PdsYkoffPadLU45EC6TF8EE2g8aoCtrOb0NCstDW4-mMftwttlV9xSC_yQXuVSZfN87sV3TJBg3fqd1GEpA%3D%3D%22%5D%5D; _ga=GA1.1.1058421002.1723849897; aws-waf-token=96630bbf-8534-431f-bd46-6c3a0c770610:EAoAg3Fg99FIAwAA:Yuc68n0YVhg/CRhXCd3WoOuoz5/9TZ5vbqMByHr7Ppe1UVakGLiSWA4zaBHaDCpbmEQpg3km5QguaFqAblBoZP+1hSQ1Ic5WjKcEZ+eTEZklzNTgO9i0Eyhl1R4Kcbcf9CpYeu3/Nr9mTcF19beiLX274FUc254uSw90V4DSq7Jf4+s9/P9k0RnmVE/IsjTfpEF5bA9UjOCwVhspryaSsb1koUXETB52TBXslgGdBvnlKO6eDbCcVM4W; _ga_2S06LYQ1G3=GS1.1.1725716974.3.1.1725717726.43.0.0; _ga_KPC4YK8R9E=GS1.1.1725716974.3.1.1725717726.43.0.0",
        "priority": "u=0, i",
        "referer": "https://www.chileautos.cl/vehiculos/autos-veh%C3%ADculo/?offset=24",
        "sec-ch-device-memory": "8",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
        "sec-ch-ua-arch": "\"x86\"",
        "sec-ch-ua-full-version-list": "\"Chromium\";v=\"128.0.6613.120\", \"Not;A=Brand\";v=\"24.0.0.0\", \"Microsoft Edge\";v=\"128.0.2739.63\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    try:
        response = requests.get(url, headers=headers)
    except InvalidSchema:
        return
    except ConnectionError:
        logger.error("Connection error [%s]" % url)
        return
    else:
        if response.status_code != 200:
            logger.info("Error loading page [%s]" % url)
            return
        return response.text


def parse_item(item):
    result = {}
    brand = item['data-webm-make']
    model = item['data-webm-model']
    net_id = item['data-webm-networkid']
    price = item['data-webm-price']
    state = item['data-webm-state']
    seller_type = item.find('span', class_='seller-type').contents[-1]
    year = item.find("a", {
        "data-webm-clickvalue": "sv-title"}).contents[-1].split(' ')[0]

    result = {
        'brand': item['data-webm-make'],
        'model': item['data-webm-model'],
        'net_id': item['data-webm-networkid'],
        'price': item['data-webm-price'],
        'state': item['data-webm-state'],
        'seller_type': item.find('span', class_='seller-type').contents[-1],
        'year': year,
    }

    for key_detail in item.find_all("div", class_="key-detail-value"):
        key_detail_type = key_detail['data-type'].lower().replace(" ", "_")
        # logger.debug(f"{key_detail_type}: {key_detail.contents[-1]}")
        result[key_detail_type] = key_detail.contents[-1]
    return result


def scraper(url: str, pagination_limit=5) -> None:
    base_url = "https://www.chileautos.cl"
    result = []
    for i in range(pagination_limit):
        logger.info(f"Scraping [{url}]")
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='listing-item standard')
        for item in items:
            logger.debug(parse_item(item))
            result.append(parse_item(item))
        next_btn = soup.find('a', class_='page-link next')
        if next_btn and 'href' in next_btn.attrs:
            url = base_url + next_btn.attrs['href']
            logger.info(f"Pagination - URL = [{url}]")
            continue
        next_btn = soup.find_all('a', class_='page-link next disabled')
        if next_btn:
            logger.info("Last page!")
            break
        else:
            logger.error("PAGINATION ERROR")
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Scraping chileautos.cl')
    parser.add_argument('--page', help='URL for the start page', required=True)
    parser.add_argument(
        '--pagination_limit',
        help='Maximum number of pages visited',
        required=True)
    args = parser.parse_args()

    scraper(url=args.page, pagination_limit=args.pagination_limit)
