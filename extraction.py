from cleasing import get_text_between, clean_price

def getId(line, ids):
    try:
        href=line.find('a', class_="block border border-neutral-90 rounded-1 overflow-hidden text-neutral-120 group/card text-start shadow-bottom-0 duration-1 hover:shadow-bottom-6 transition-shadow ease-in")['href']
        start = href.rfind('-')
        end = href.rfind('/')
        id=href[start+1:end]
        ids.append(id)
    except:
        ids.append('')


def getUrl(line, url):
    try:
        href=line.find('a', class_="block border border-neutral-90 rounded-1 overflow-hidden text-neutral-120 group/card text-start shadow-bottom-0 duration-1 hover:shadow-bottom-6 transition-shadow ease-in")['href']
        url.append(href)
    except:
        url.append('')


def getPropertyType(line, propertyType):
    try:
        property=line.find('span', class_="block font-secondary text-1-5 font-regular text-neutral-110 mb-1").text.strip()
        property=get_text_between(property, None, ' para ')
        propertyType.append(property)
    except:
        propertyType.append('')


def getAddress(line, address):
    try:
        street=line.find('p', class_="text-1-75 font-regular text-ellipsis overflow-hidden").text.strip()
        address.append(street)
    except:
        address.append('')


def getNeighbor(line, neighbor):
    try:
        neighborhood=line.find('h2', class_="text-ellipsis text-2 font-semibold overflow-hidden font-secondary").text.strip()
        neighborhood=get_text_between(neighborhood, ' em ', ',')
        neighbor.append(neighborhood)
    except:
        neighbor.append('')


def getArea(line, area):
    try:        
        full_area=line.find('li', attrs={"data-cy": "rp-cardProperty-propertyArea-txt"}).text.strip()
        full_area=get_text_between(full_area, 'Tamanho do imóvel ', ' m²')
        full_area=get_text_between(full_area, None, '-')
        area.append(full_area)
    except:
        area.append('')


def getRoom(line, room):
    try:
        full_room=line.find('li', attrs={"data-cy": "rp-cardProperty-bedroomQuantity-txt"}).text.strip()
        full_room=get_text_between(full_room, 'Quantidade de quartos ', '-')
        room.append(full_room)
    except:
        room.append('')


def getBath(line, bath):
    try:
        full_bath=line.find('li', attrs={"data-cy": "rp-cardProperty-bathroomQuantity-txt"}).text.strip()        
        full_bath=get_text_between(full_bath, 'Quantidade de banheiros ', '-')
        bath.append(full_bath)
    except:
        bath.append('')


def getPark(line, park):
    try:
        full_park=line.find('li', attrs={"data-cy": "rp-cardProperty-parkingSpacesQuantity-txt"}).text.strip()        
        full_park=get_text_between(full_park, 'Quantidade de vagas de garagem ', '-')

        park.append(full_park)
    except:
        park.append('')


def getPrice(line, price):
    try:
        full_price=line.find('p', class_='text-2-25 text-neutral-120 font-semibold').text.strip()      
        full_price=clean_price(full_price)
        price.append(full_price)
    except:
        price.append('')


def getCondo(line, condo):
    try:
        full_condo=line.find('p', class_='text-1-75 text-neutral-110 overflow-hidden text-ellipsis').text.strip()
        if full_condo.find('Cond.') == -1:
            raise Exception
        
        full_condo=get_text_between(full_condo, 'Cond.', ' • ')
        full_condo=clean_price(full_condo)                       
        condo.append(full_condo)
    except:
        condo.append('')


def getIptu(line, iptu):
    try:
        full_iptu=line.find('p', class_='text-1-75 text-neutral-110 overflow-hidden text-ellipsis').text.strip()
        if full_iptu.find('IPTU') == -1:
            raise Exception
        
        full_iptu=get_text_between(full_iptu, 'IPTU', None)
        full_iptu=clean_price(full_iptu)
        iptu.append(full_iptu)
    except:
        iptu.append('')
