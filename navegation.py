import time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def buildDriver(userDataDir):
    # Configure msedgedriver
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Required for headless mode
    options.add_argument('--disable-browser-side-navigation')

    # Set a temporary unique user data dir (optional but helps avoid conflicts)
    options.add_argument(f'--user-data-dir={userDataDir}')

    driver = webdriver.Edge(options=options)
    return driver


def closeDriver(userDataDir):
    driver.quit()
    shutil.rmtree(userDataDir)


def scrollUntilElementAppears(driver,timeout=30):
    """Scrolls down the page until the next page button appears or the timeout is reached.
    
    Parameters
    ----------
    driver : selenium.webdriver
        The selenium webdriver object.
    timeout : int, optional
        The maximum time to wait in seconds until the next page button appears. Defaults to 30 seconds.
    
    Returns
    -------
    selenium.webdriver.remote.webelement.WebElement or None
        The next page button element if it appears, otherwise None.
    """
    start_time = time.time()
    while True:
        try:
            element = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="next-page"]')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(random.uniform(8, 10))
            return element
        except NoSuchElementException:
            scroll_offset = int(random.uniform(1500, 2500))
            driver.execute_script(f"window.scrollBy(0, {scroll_offset});")  # scroll down
            time.sleep(random.uniform(3, 6))
            if time.time() - start_time > timeout:
                return None


def getAndDownloadPage(driver, page):
    data = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup_complete_source = BeautifulSoup(data.encode('utf-8'), 'html.parser')
    soup = soup_complete_source.find(class_='listings-wrapper flex flex-col gap-3')    
    
    # download page html
    with open('pages//site'+str(page)+'.html', 'w', encoding='utf-16') as outf:
        outf.write(str(soup))
    
    return soup
