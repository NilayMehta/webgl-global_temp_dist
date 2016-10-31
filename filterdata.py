import json
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

lonarray = []
latarray = []
temparray = []
extemparray = []

# function to determine values of relevant information
def split_line(string):
    temporarytemparray = []
    stringarray = string.split('"')
    for i in range(len(stringarray)):
        if 'lon' in stringarray[i]:
            try:
                string1 = stringarray[i + 1]
                string1 = string1.lstrip(':')
                string1 = string1.rstrip(',')
                num = float(string1)
                lonvalue = float("{0:.1f}".format(num))
                lonarray.append(lonvalue)
                # print(lonvalue)
            except ValueError:
                print("value error exception - lon")
        if 'lat' in stringarray[i]:
            try:
                string2 = stringarray[i + 1]
                string2 = string2.lstrip(':')
                string2 = string2.rstrip(',')
                string2 = string2.rstrip('}}')
                num = float(string2)
                latvalue = float("{0:.1f}".format(num))
                latarray.append(latvalue)
                print(latvalue)
            except ValueError:
                print("value error exception - lat")
        if 'day' in stringarray[i]:
            try:
                stringd = stringarray[i + 1]
                stringd = stringd.lstrip(':')
                stringd = stringd.rstrip(',')
                num = float(stringd)
                tempvalue = float("{0:.3f}".format(num))
                temporarytemparray.append(tempvalue)
                # print(tempvalue)
            except ValueError:
                print("value error exception - temp")
    normailize_temps(temporarytemparray)
    exaggerate_temps(temporarytemparray)

def normailize_temps(array):
    t = 0
    for eachval in array:
        t = t + eachval
    t = float("{0:.4f}".format((((((t / 16) * (9/5)) - 459.67) / 100))))
    temparray.append(t)

def exaggerate_temps(array):
    t = 0
    for eachval in array:
        t = t + eachval
    t = float("{0:.4f}".format((((((((t / 16) * (9/5)) - 459.67) / 80 ) - 0.3) / 2) - 0.1 ) * 1.5))
    if t >= 0.53:
        a = t * 0.70
    if t < 0.53 and t >= 0.30:
        a = t * 0.75
    if t <= 0.30 and t >= 0.05:
        a = t * 0.85
    if  t > 0.00 and t < 0.05:
        a = t
    if t <= 0.00:
        a = abs(t)
    else:
        a = t
    a = a * 0.75
    extemparray.append(a)

def plot_data():
    mu, std = norm.fit(temparray)
    plt.hist(temparray, bins=25, normed=True, alpha=0.6, color='g')

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()

with open('originaldataset.json', 'r', encoding='utf-8') as infile:
    for line in infile:
        stringarray = split_line(line)
        # print(stringarray)

print(len(lonarray), len(latarray), len(temparray))

outputstring = '[["GlobalTempNormal",['
middlestring = ']]["GlobalTempExaggerated",['
endstring = ']]]'

for j in range(len(latarray)):
    outputstring += str(latarray[j])
    outputstring += ","
    outputstring += str(lonarray[j])
    outputstring += ","
    outputstring += str(temparray[j])
    outputstring += ","
outputstring += middlestring
for p in range(len(latarray)):
    outputstring += str(latarray[p])
    outputstring += ","
    outputstring += str(lonarray[p])
    outputstring += ","
    outputstring += str(extemparray[p])
    outputstring += ","
outputstring = outputstring.rstrip(',')
outputstring += endstring

print(outputstring)

#to make sure data is consistant and lines up, all arrays should have equal elements in array
print(len(lonarray), len(latarray), len(temparray), len(extemparray))

#used to analize data and to help with multipleirs to normalize and exagerate temp data
print(np.mean(temparray))
print(max(temparray))
print(min(temparray))

plot_data()

with open('temperaturedata.json', 'w') as outfile:
    json.dump(outputstring, outfile)