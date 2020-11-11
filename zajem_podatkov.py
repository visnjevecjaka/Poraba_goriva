import requests
import xml.etree.ElementTree as ET
import csv

def get_LKM(tree):
    MPG = int(tree[19].text)
    ##Pretvorba v evropske enote
    LKM = round(235.15 / MPG, 2)

    return LKM

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

    with open('data.csv', mode='w', newline='') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['make','model','year','cylinder number','displacement', 'fuel type', 'consumption'])

        for i in range(15589, 43425):
            request = requests.get(f'https://www.fueleconomy.gov/ws/rest/vehicle/{i}')
            print(i)

            tree = ET.fromstring(request.content)
            
            try:
                make = get_make(tree)
                model = get_model(tree)
                year = get_year(tree)
                displacement = get_displacement(tree)
                cylinder_nr = get_cylinder_nr(tree)
                fuel_type = get_fuelType(tree)
                LKM = get_LKM(tree)
            except:
                continue

            data_writer.writerow([make, model, year, cylinder_nr, displacement, fuel_type, LKM])

get_data()
