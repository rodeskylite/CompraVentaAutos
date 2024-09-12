from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import time

# Configurar el WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Opcional, para ejecutar sin interfaz gráfica

# Update this path to the location where you have extracted chromedriver
service = Service('C:/path/to/chromedriver.exe')  # Ensure the path is correct

# Configurar logging
logging.basicConfig(level=logging.INFO)

def extract_car_details(detail_url):
    logging.info(f"Extracting details from {detail_url}")
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        if driver is None:
            raise Exception("Failed to initialize WebDriver")
        
        driver.get(detail_url)
        time.sleep(2)  # Esperar a que se cargue la página
        
        # Verificar si la página se ha cargado correctamente
        if "expected_title_or_element" not in driver.page_source:
            raise Exception("Failed to load the page or find the expected element")
        
        # Extraer los detalles del auto
        car_details = {
            'name': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-vehculo"]').text.strip(),
            'precio': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-precio"]').text.strip(),
            'kilometraje': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-kilmetros"]').text.strip(),
            'transmision': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-transmisin-tipo-de-transmisin"]').text.strip(),
            'motor': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-litros-motor"]').text.strip(),
            'vendedor': driver.find_element(By.XPATH, '//span[@class="adtype-value"]').text.strip(),
            'region': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-regin"]').text.strip(),
            'comuna': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-comuna"]').text.strip(),
            'combustible': driver.find_element(By.XPATH, '//div[@class="col features-item-value features-item-value-combustible-tipo-de-combustible-primario"]').text.strip()
        }
        
        logging.info(f"Extracted details: {car_details}")
        return car_details
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
    
    finally:
        if driver:
            driver.quit()

def scrape_chileautos():
    logging.info("Starting to scrape chileautos")
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.chileautos.cl/vehiculos/autos-veh%C3%ADculo/?offset=0')
        time.sleep(2)  # Esperar a que se cargue la página

        # Extraer URLs de detalles
        detail_urls = []
        car_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/vehiculos/detalles/")]')
        for car in car_elements:
            detail_urls.append(car.get_attribute('href'))

        logging.info(f"Found {len(detail_urls)} detail URLs")
        
        # Extraer detalles para cada URL
        all_car_details = []
        for url in detail_urls:
            details = extract_car_details(url)
            if details:
                all_car_details.append(details)
        
        logging.info(f"Scraped details for {len(all_car_details)} cars")
        return all_car_details
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    car_details = scrape_chileautos()
    logging.info(f"Scraping completed. Total cars scraped: {len(car_details)}")