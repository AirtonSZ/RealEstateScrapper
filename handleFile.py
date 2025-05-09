import os, datetime
import boto3
import pandas as pd

def createFolder(dirName):
    try:
        os.mkdir(dirName)
        print("Directory", dirName, "Created ") 
    except FileExistsError:
        print("Directory", dirName, "already exists")


def createOutputCsv(ids, url, propertyType, address, neighbor, area, room, bath, park, price, condo, iptu):

    outputFile = 'output/VivaReal.csv'

    with open(outputFile, 'w', encoding='utf-8', newline='') as f:
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
        with open(outputFile, 'a', encoding='utf-8', newline='') as f:
            df.transpose().to_csv(f, encoding='iso-8859-1', index=False, header=False)

    return outputFile


def uploadToS3(filePath):
    # Generate timestamped key
    now  = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H-%M-%S")
    objectKey = f"raw/date={date}/viva_real_{time}.csv"
    bucketName = 'real-estate-scrapper'

    s3 = boto3.client('s3')
    s3.upload_file(filePath, bucketName, objectKey)
    print(f"Uploaded {filePath} to s3://{bucketName}/{objectKey}")
