import math
from os import name
import os
from sqlite3 import Date
from xmlrpc.client import DateTime
from bs4 import BeautifulSoup
import requests
import re
import json
from parkinglot import ParkingLot
import subprocess
import datetime

def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    page = requests.get('https://web1.karlsruhe.de/service/Parken/')
    soup = BeautifulSoup(page.content, "html.parser")
    p = soup.find_all(class_='parkhaus')
    valueFinder = re.compile('[0-9]+')
    data = {"date":datetime.date.today().isoformat()}
    ps = []
    for parkhaus in p:
        try:
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
        except:
            print("Something went wrong while read the HTML")
    data['data'] = ps

    with open('../maxomnia.github.io/data.json', 'w') as f:
                f.write(json.dumps(data))
    command = 'cd ../maxomnia.github.io & git add * & git commit -m "Automated Commit" & git push'
    result= subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    print(result.stdout.decode())

if(__name__ == "__main__"):
    main()