import time, os, random
import tempfile
import shutil
import extraction
import handleFile
import navegation

# Initialize lists
ids = url = propertyType = address = neighbor = area = room = bath = park = price = condo = iptu = []

# Get the number of pages to extract information
pages_number = 3
tic = time.time()

# Initialize driver
userDataDir = tempfile.mkdtemp()
driver = navegation.buildDriver(userDataDir)

# Create auxiliar folders
handleFile.createFolder('pages')
handleFile.createFolder('output')

# Get Link to the first page !
link = 'https://www.vivareal.com.br/venda/sp/sao-paulo/?transacao=venda&onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,-21.292246,-50.342843,&pagina=1'
driver.get(link)

# Loop through the website's pages
for page in range(1,pages_number+1):
    
    time.sleep(random.uniform(2, 3))
    nextPageButton = navegation.scrollUntilElementAppears(driver)
    soup = navegation.getAndDownloadPage(driver, page)

    # Web-Scraping
    for line in soup.find_all('li', attrs={"data-cy": "rp-property-cd"}):
        extraction.getId(line, ids)
        extraction.getUrl(line, url)
        extraction.getPropertyType(line, propertyType)
        extraction.getAddress(line, address)
        extraction.getNeighbor(line, neighbor)
        extraction.getArea(line, area)
        extraction.getRoom(line, room)
        extraction.getBath(line, bath)
        extraction.getPark(line, park)
        extraction.getPrice(line, price)
        extraction.getCondo(line, condo)
        extraction.getIptu(line, iptu)

    driver.execute_script("arguments[0].click();", nextPageButton)
            
# Close msedgedriver
navegation.closeDriver(userDataDir)

# Create Output csv 
handleFile.createOutputCsv(ids, url, propertyType, address, neighbor, area, room, bath, park, price, condo, iptu)

# Execution time
toc = time.time()
get_time = round(toc-tic,3)
print('Finished in ' + str(get_time) + ' seconds')
print(str(len(ids))+' results!')