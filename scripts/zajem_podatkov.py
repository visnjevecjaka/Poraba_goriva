import requests
import xml.etree.ElementTree as ET
import csv
from datetime import date, datetime

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
    
    # zajeli pa bomo vse avtomobile od leta 1985 do danes. id zadnjega je 43424

    with open('main_export_with_consumptions2.csv', mode='w', newline='') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['make','model','year','cylinder number',
        'displacement', 'fuel type', 'combined consumption',
        'city consumption', 'highway consumption'])

        for i in range(0, 43425):
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

get_data()
