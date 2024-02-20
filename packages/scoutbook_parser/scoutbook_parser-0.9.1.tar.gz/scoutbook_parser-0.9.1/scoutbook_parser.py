import csv
import pprint
import os

FILE = os.path.join("data", "bsa_roster.csv")
RANKFILE = os.path.join("data", "bsa_ranks.csv")

scouts = {}
with open(FILE, encoding='utf-8') as f:
    line = f.readline()
    reader = csv.DictReader(f)
    for scout in reader:
        scouts[f"{scout['Last Name']}, {scout['First Name']}"] = scout

with open(RANKFILE, encoding='latin_1', newline='\n') as f:
    for x in f: 
        output = [x.replace('\r\n', '').split(',') for x in f]

for x in zip(*output):
    for y in x:
        print(y + ', ', end="")
    print('')

