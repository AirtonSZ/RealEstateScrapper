import time, os, random
import tempfile
import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import pandas as pd

def scroll_until_element_appears(driver,timeout=30):
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
            driver.execute_script("arguments[0].scrollIntoView();", element)
            return element
        except NoSuchElementException:
            scroll_offset = int(random.uniform(500, 1000))
            driver.execute_script(f"window.scrollBy(0, {scroll_offset});")  # scroll down
            time.sleep(random.uniform(3, 6))
            if time.time() - start_time > timeout:
                return None
            

def get_text_between(text, start_str, end_str):
    """
    Gets the text between two strings.

    Parameters
    ----------
    text : str
        The text to search.
    start_str : str
        The starting string. If None, the text is returned.
    end_str : str
        The ending string. If None, the text is returned.

    Returns
    -------
    str
        The text between the two strings.
    """
    if start_str == None and end_str == None:
        return text
    
    start = 0
    offset = 0
    if start_str != None and text.find(start_str) != -1:
        start = text.find(start_str)
        offset = len(start_str)

    if end_str != None and text.find(end_str) != -1:
        end = text.find(end_str)
        return text[start+offset:end]

    return text[start+offset:]

def clean_price(text):
    """
    Cleans a price string by removing spaces, the 'R$' currency symbol, decimal points, and unwanted strings.
    
    Parameters
    ----------
    text : str
        The string to clean.
    
    Returns
    -------
    str
        The cleaned string.
    """
    text=text.replace(' ','')
    text=text.replace('R$','').replace('.','')
    text=text.replace('Apartirde','').replace('apartirde','')
    text=text.replace('Valorsobconsulta','-')

# Initialize lists
ids=[]
url=[]
property_type=[]
address=[]
neighbor=[]
area=[]
room=[]
bath=[]
park=[]
price=[]
condo=[]
iptu=[]

# Get the number of pages to extract information
pages_number = 2
tic = time.time()

# Configure msedgedriver
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Required for headless mode
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

# Set a temporary unique user data dir (optional but helps avoid conflicts)
user_data_dir = tempfile.mkdtemp()
options.add_argument(f'--user-data-dir={user_data_dir}')

driver = webdriver.Edge(options=options)

# Create a folder to save downloaded HTML pages
dirName = 'pages'
try:
    os.mkdir(dirName)
    print("Directory", dirName, "Created ") 
except FileExistsError:
    print("Directory", dirName, "already exists")

# Get Link to the first page !
link = 'https://www.vivareal.com.br/venda/sp/sao-paulo/?transacao=venda&onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,-21.292246,-50.342843,&pagina=1'
driver.get(link)

# Loop through the website's pages
for page in range(1,pages_number+1):
    
    time.sleep(random.uniform(2, 3))
    next_page_button = scroll_until_element_appears(driver)
    
    data = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup_complete_source = BeautifulSoup(data.encode('utf-8'), 'html.parser')
    
    soup = soup_complete_source.find(class_='listings-wrapper flex flex-col gap-3')    
    
    # download page html
    with open('pages//site'+str(page)+'.html', 'w', encoding='utf-16') as outf:
        outf.write(str(soup_complete_source))

    # Web-Scraping
    for line in soup.find_all('li', attrs={"data-cy": "rp-property-cd"}):
        try:
            # Get Apto's Id    
            href=line.find('a', class_="block border border-neutral-90 rounded-1 overflow-hidden text-neutral-120 group/card text-start shadow-bottom-0 duration-1 hover:shadow-bottom-6 transition-shadow ease-in")['href']
            start = href.rfind('-')
            end = href.rfind('/')
            id=href[start+1:end]
            ids.append(id)
        except:
            ids.append('')
        
        try:
            # Get Apto's Link
            href=line.find('a', class_="block border border-neutral-90 rounded-1 overflow-hidden text-neutral-120 group/card text-start shadow-bottom-0 duration-1 hover:shadow-bottom-6 transition-shadow ease-in")['href']
            url.append(href)
        except:
            url.append('')
        
        try:
            # Get Property Type
            property=line.find('span', class_="block font-secondary text-1-5 font-regular text-neutral-110 mb-1").text.strip()
            property=get_text_between(property, None, ' para ')
            property_type.append(property)
        except:
            property_type.append('')
        
        try:
            # Get Apto's
            street=line.find('p', class_="text-1-75 font-regular text-ellipsis overflow-hidden").text.strip()
            address.append(street)
        except:
            address.append('')

        try:
            # Get Apto's Neighborhood
            neighborhood=line.find('h2', class_="text-ellipsis text-2 font-semibold overflow-hidden font-secondary").text.strip()
            neighborhood=get_text_between(neighborhood, ' em ', ',')
            neighbor.append(neighborhood)
        except:
            neighbor.append('')

        try:        
            # Get Apto's Area
            full_area=line.find('li', attrs={"data-cy": "rp-cardProperty-propertyArea-txt"}).text.strip()
            full_area=get_text_between(full_area, 'Tamanho do imóvel ', ' m²')
            full_area=get_text_between(full_area, None, '-')
            area.append(full_area)
        except:
            area.append('')

        try:
            # Get Apto's Rooms
            full_room=line.find('li', attrs={"data-cy": "rp-cardProperty-bedroomQuantity-txt"}).text.strip()
            full_room=get_text_between(full_room, 'Quantidade de quartos ', '-')
            room.append(full_room)
        except:
            room.append('')

        try:
            # Get Apto's Bathrooms
            full_bath=line.find('li', attrs={"data-cy": "rp-cardProperty-bathroomQuantity-txt"}).text.strip()        
            full_bath=get_text_between(full_bath, 'Quantidade de banheiros ', '-')
            bath.append(full_bath)
        except:
            bath.append('')

        try:
            # Get Apto's parking lot
            full_park=line.find('li', attrs={"data-cy": "rp-cardProperty-parkingSpacesQuantity-txt"}).text.strip()        
            full_park=get_text_between(full_park, 'Quantidade de vagas de garagem ', '-')

            park.append(full_park)
        except:
            park.append('')

        try:
            # Get Apto's price
            full_price=line.find('p', class_='text-2-25 text-neutral-120 font-semibold').text.strip()      
            full_price=clean_price(full_price)
            price.append(full_price)
        except:
            price.append('')

        try:
            # Get Apto's condo price
            full_condo=line.find('p', class_='text-1-75 text-neutral-110 overflow-hidden text-ellipsis').text.strip()
            if full_condo.find('Cond.') == -1:
                raise Exception
            
            full_condo=get_text_between(full_condo, 'Cond.', ' • ')
            full_condo=clean_price(full_condo)                       
            condo.append(full_condo)
        except:
            condo.append('')

        try:
            # Get Apto's iptu
            full_iptu=line.find('p', class_='text-1-75 text-neutral-110 overflow-hidden text-ellipsis').text.strip()
            if full_iptu.find('IPTU') == -1:
                raise Exception
            
            full_iptu=get_text_between(full_iptu, 'IPTU', None)
            full_iptu=clean_price(full_iptu)
            iptu.append(full_iptu)
        except:
            iptu.append('')

    driver.execute_script("arguments[0].click();", next_page_button)
    next_page_button.click()
            
# Close msedgedriver
driver.quit()
shutil.rmtree(user_data_dir)
output_file = 'output/VivaReal.csv'

with open(output_file, 'w', encoding='utf-16', newline='') as f:
    f.write('Id,Url,Property type,Address,Neighborhood,Area,Rooms,Bathrooms,Parking,Price,Condo,IPTU\n')

# Save as a CSV file
for i in range(0,len(ids)):
    combinacao=[
        ids[i],
        url[i],
        property_type[i],
        address[i],
        neighbor[i],
        area[i],
        room[i],
        bath[i],
        park[i],
        price[i],
        condo[i],
        iptu[i]
    ]
    df=pd.DataFrame(combinacao)
    with open(output_file, 'a', encoding='utf-16', newline='') as f:
        df.transpose().to_csv(f, encoding='iso-8859-1', index=False, header=False)

# Execution time
toc = time.time()
get_time=round(toc-tic,3)
print('Finished in ' + str(get_time) + ' seconds')
print(str(len(price))+' results!')