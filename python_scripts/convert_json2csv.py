import json
import csv

with open('G:\Akhil\jsonoutput.json') as jf:
    jd = json.load(jf)

df = open('G:\Akhil\jsonoutput.csv', 'w', newline='')
cw = csv.writer(df)

c = 0
for data in jd:
    if c == 0:
        header = data.keys()
        cw.writerow(header)
        c += 1
    cw.writerow(data.values())

df.close()