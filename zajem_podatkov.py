import requests
import xml.etree.ElementTree as ET
import csv
from datetime import date, datetime
import pandas as pd

startTime = datetime.now()

def getCombined_LKM(tree):
    MPG = int(tree[19].text)
    #Pretvorba v evropske enote
    combLKM = round(235.15 / MPG, 2)
    return combLKM

def getCity_LKM(tree):
    MPG = int(tree[8].text)
    cityLKM = round(235.15 / MPG, 2)
    return cityLKM

def getHighway_LKM(tree):
    MPG = int(tree[43].text)
    highwayLKM = round(235.15 / MPG, 2)
    return highwayLKM

def get_displacement(tree):
    displacement = float(tree[28].text)

    return displacement

def get_cylinder_nr(tree):
    cylinder_nr = int(tree[27].text)

    return cylinder_nr

def get_fuelType(tree):
    fuel_type = tree[37].text

    return fuel_type

def get_make(tree):
    make = tree[55].text

    return make

def get_model(tree):
    model = tree[57].text

    return model

def get_year(tree):
    year = tree[81].text

    return year

def get_data():
    
    # id prvega avta proizvedenega leta 2000 je 15589, zajeli pa bomo vse avtomobile od takrat do danes. id zadnjega je 43424

    with open('main_export.csv', mode='w', newline='') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['make','model','year','cylinder number',
        'displacement', 'fuel type', 'combined consumption',
        'city consumption', 'highway consumption'])

        for i in range(40199, 43425):
            print(i)
            request = requests.get(f'https://www.fueleconomy.gov/ws/rest/vehicle/{i}')
            print(datetime.now() - startTime)

            tree = ET.fromstring(request.content)
            
            try:
                make = get_make(tree)
                model = get_model(tree)
                year = get_year(tree)
                displacement = get_displacement(tree)
                cylinder_nr = get_cylinder_nr(tree)
                fuel_type = get_fuelType(tree)
                combLKM = getCombined_LKM(tree)
                cityLKM = getCity_LKM(tree)
                highwayLKM = getHighway_LKM(tree)

            except:
                continue

            data_writer.writerow([make, model, year, cylinder_nr, displacement, fuel_type, combLKM, cityLKM, highwayLKM])

# get_data()

def createMainDB():
    db = pd.read_csv('podatki/main_export.csv')

    # get all the makes in a list for referencing
    makes = db['make']
    makes = list(dict.fromkeys(makes))
    makes.sort()
    makes.remove('make')

    # get all the years in a list for referencing
    years = db['year']
    years = list(dict.fromkeys(years))
    years.sort()
    years.remove('year')

    big_data_dict = {
        'year': years
    }

    # sort by make year, 4 cylinders and calculate all avg consumptions
    big_data = pd.DataFrame(data=big_data_dict)

    for make in makes:
        averages = []
        for year in years:
            print(make, year)
            # print(make, year)
            temporary_db = db.loc[
            (db['make'] == make) & 
            (db['year'] == year) & 
            (db['cylinder number'] == '4') &
            (db['fuel type'] != 'Diesel')]

            averages.append(temporary_db['consumption'].astype(float).mean())

        big_data[make] = averages

    # drop all brands without consumption records, sort by year
    # save filtered data as csv

    big_data.sort_values(by=['year'])
    big_data.dropna(how='all', axis=1, inplace=True)
    big_data.to_csv('podatki/yearXbrand.csv', index=False)
    print('File created.')

def createBrandAverages():
    # Calculate the averages of all brand for all years
    yearXbrandDB = pd.read_csv('podatki/yearXbrand.csv')
    
    brandAveragesDict = {}

    for make in yearXbrandDB.columns:
        brandAveragesDict[make]=yearXbrandDB[make].astype(float).mean()

    brandAverages = pd.DataFrame([brandAveragesDict])
    brandAverages.drop(columns=['year'], inplace=True)
    brandAverages.to_csv('podatki/brandAverages.csv', index=False)
    print('File created.')

createMainDB()
createBrandAverages()

