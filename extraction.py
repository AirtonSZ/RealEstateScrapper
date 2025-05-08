from cleasing import get_text_between, clean_price

def getId(line):
    try:
        href=line.find('li', attrs={"data-cy": "rp-property-cd"})['href']
        start = href.rfind('-')
        end = href.rfind('/')
        id=href[start+1:end]
        return id
    except:
        return ''


def getUrl(line):
    try:
        href=line.find('li', attrs={"data-cy": "rp-property-cd"})['href']
        return href
    except:
        return ''


def getPropertyType(line):
    try:
        property=line.find('span', class_="block font-secondary text-1-5 font-regular text-neutral-110 mb-1").text.strip()
        property=get_text_between(property, None, ' para ')
        return property
    except:
        return ''


def getAddress(line):
    try:
        street=line.find('p', class_="text-1-75 font-regular text-ellipsis overflow-hidden").text.strip()
        return street
    except:
        return ''


def getNeighbor(line):
    try:
        neighborhood=line.find('h2', class_="text-ellipsis text-2 font-semibold overflow-hidden font-secondary").text.strip()
        neighborhood=get_text_between(neighborhood, ' em ', ',')
        return neighborhood
    except:
        return ''


def getArea(line):
    try:        
        full_area=line.find('li', attrs={"data-cy": "rp-cardProperty-propertyArea-txt"}).text.strip()
        full_area=get_text_between(full_area, 'Tamanho do imóvel ', ' m²')
        full_area=get_text_between(full_area, None, '-')
        return full_area
    except:
        return ''


def getRoom(line):
    try:
        full_room=line.find('li', attrs={"data-cy": "rp-cardProperty-bedroomQuantity-txt"}).text.strip()
        full_room=get_text_between(full_room, 'Quantidade de quartos ', '-')
        return full_room
    except:
        return ''


def getBath(line):
    try:
        full_bath=line.find('li', attrs={"data-cy": "rp-cardProperty-bathroomQuantity-txt"}).text.strip()        
        full_bath=get_text_between(full_bath, 'Quantidade de banheiros ', '-')
        return full_bath
    except:
        return ''


def getPark(line):
    try:
        full_park=line.find('li', attrs={"data-cy": "rp-cardProperty-parkingSpacesQuantity-txt"}).text.strip()        
        full_park=get_text_between(full_park, 'Quantidade de vagas de garagem ', '-')
        return full_park
    except:
        return ''


def getPrice(line):
    try:
        full_price=line.find('p', class_='text-2-25 text-neutral-120 font-semibold').text.strip()      
        full_price=clean_price(full_price)
        return full_price
    except:
        return ''


def getCondo(line):
    try:
        full_condo=line.find('p', class_='text-1-75 text-neutral-110 overflow-hidden text-ellipsis').text.strip()
        if full_condo.find('Cond.') == -1:
            raise Exception
        
        full_condo=get_text_between(full_condo, 'Cond.', ' • ')
        full_condo=clean_price(full_condo)                       
        return full_condo
    except:
        return ''


def getIptu(line):
    try:
        full_iptu=line.find('p', class_='text-1-75 text-neutral-110 overflow-hidden text-ellipsis').text.strip()
        if full_iptu.find('IPTU') == -1:
            raise Exception
        
        full_iptu=get_text_between(full_iptu, 'IPTU', None)
        full_iptu=clean_price(full_iptu)
        return full_iptu
    except:
        return ''
