import os
import pandas as pd

def createFolder(dirName):
    try:
        os.mkdir(dirName)
        print("Directory", dirName, "Created ") 
    except FileExistsError:
        print("Directory", dirName, "already exists")


def createOutputCsv(ids, url, propertyType, address, neighbor, area, room, bath, park, price, condo, iptu):

    output_file = 'output/VivaReal.csv'

    with open(output_file, 'w', encoding='utf-16', newline='') as f:
        f.write('Id,Url,Property type,Address,Neighborhood,Area,Rooms,Bathrooms,Parking,Price,Condo,IPTU\n')

    # Save as a CSV file
    for i in range(0,len(ids)):
        combinacao=[
            ids[i],
            url[i],
            propertyType[i],
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