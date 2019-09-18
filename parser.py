import datetime
import os
import time

import grab
import pandas as pd
from bs4 import BeautifulSoup

data_url = 'https://www.utdallas.edu/services/transit/garages/_code.php'
pass_to_csv = 'PATH_TO_RESULT_CSV'


def get_data(url):
    df = pd.DataFrame(columns=['Time', 'Parking', 'Level', 'Option', 'Spaces'])
    update_time = datetime.datetime.now()
    html_doc = grab.Grab().go(url).body
    soup = BeautifulSoup(html_doc, 'lxml')
    structures = soup.find_all('table')
    for structure in structures:
        structure_df = get_parking(structure, update_time)
        df = df.append(structure_df, ignore_index=True)

    return df


def get_parking(parking_structure, scrape_time=datetime.datetime.now()):
    parking_df = pd.DataFrame(columns=['Time', 'Parking', 'Level', 'Option', 'Spaces'])
    name = parking_structure.attrs['id']
    levels_body = parking_structure.find_all('tbody')
    levels = levels_body[0].find_all('tr')
    for level in levels:
        data = [value.get_text() for value in level.find_all('td')]
        level_df = pd.DataFrame(
            {'Time': [scrape_time], 'Parking': [name], 'Level': [data[0]], 'Option': [data[1]], 'Spaces': [data[2]]})
        parking_df = parking_df.append(level_df, ignore_index=True)

    return parking_df


result_df = get_data(data_url)

if os.stat(pass_to_csv).st_size == 0:
    with open(pass_to_csv, 'a') as f:
        result_df.to_csv(f, sep='\t', index=False, header=True)
else:
    with open(pass_to_csv, 'a') as f:
        result_df.to_csv(f, sep='\t', index=False, header=False)

for i in range(2):
    result_df = get_data(data_url)
    with open(pass_to_csv, 'a') as f:
        result_df.to_csv(f, sep='\t', index=False, header=False)

    time.sleep(10)
