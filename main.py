import time, random
import tempfile
import extraction
import handleFile
import navegation

# Initialize lists
ids = []
url = []
propertyType = []
address = []
neighbor = []
area = []
room = []
bath = []
park = []
price = []
condo = []
iptu = []

# Get the number of pages to extract information
pages_number = 100
tic = time.time()

# Initialize driver
userDataDir = tempfile.mkdtemp()
driver = navegation.buildDriver(userDataDir)

# Create auxiliar folders
handleFile.createFolder('pages')
handleFile.createFolder('output')

# Get Link to the first page !
link = 'https://www.vivareal.com.br/venda/sp/sao-paulo/zona-oeste/?transacao=venda&onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,Zona%20Oeste,,,,zone,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo%3EZona%20Oeste,-23.555771,-46.639557,&pagina=1&precoMaximo=1000000'
driver.get(link)

# Loop through the website's pages
for page in range(1,pages_number+1):
    
    time.sleep(random.uniform(2, 3))
    nextPageButton = navegation.scrollUntilElementAppears(driver)
    soup = navegation.getAndDownloadPage(driver, page)

    # Web-Scraping
    for line in soup.find_all('li', attrs={"data-cy": "rp-property-cd"}):
        ids.append(extraction.getId(line))
        url.append(extraction.getUrl(line))
        propertyType.append(extraction.getPropertyType(line))
        address.append(extraction.getAddress(line))
        neighbor.append(extraction.getNeighbor(line))
        area.append(extraction.getArea(line))
        room.append(extraction.getRoom(line))
        bath.append(extraction.getBath(line))
        park.append(extraction.getPark(line))
        price.append(extraction.getPrice(line))
        condo.append(extraction.getCondo(line))
        iptu.append(extraction.getIptu(line))
    
    driver.execute_script("arguments[0].click();", nextPageButton)
            
# Close msedgedriver
navegation.closeDriver(driver, userDataDir)

# Create Output csv 
filePath = handleFile.createOutputCsv(ids, url, propertyType, address, neighbor, area, room, bath, park, price, condo, iptu)
handleFile.uploadToS3(filePath)

# Execution time
toc = time.time()
get_time = round(toc-tic,3)
print('Finished in ' + str(get_time) + ' seconds')
print(str(len(ids))+' results!')