import math
from os import name
import os
from bs4 import BeautifulSoup
import requests
import re
import json
from parkinglot import ParkingLot

def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    page = requests.get('https://web1.karlsruhe.de/service/Parken/')
    soup = BeautifulSoup(page.content, "html.parser")
    p = soup.find_all(class_='parkhaus')
    valueFinder = re.compile('[0-9]+')
    ps = []
    for parkhaus in p:
        totalCap = valueFinder.findall(parkhaus.text)
        totalCap = totalCap[len(totalCap) - 1]
        occupied = parkhaus.find(class_='fuellstand')
        name = parkhaus.find('a').text.strip()
        if occupied is not None:
            v = valueFinder.search(occupied.text).group()
            v = int(v)
            totalCap = int(totalCap)
            park = ParkingLot(name, v, totalCap)
            ps.append(park.__dict__)
            #(f"{name}: {v}/{totalCap} {round((v/totalCap)*100)}%")
        else:
            ps.append(ParkingLot(name, -1, -1).__dict__)
            #print(f"{name}: N/A")

    with open('data.json', 'w') as f:
                f.write(json.dumps(ps))

if(__name__ == "__main__"):
    main()