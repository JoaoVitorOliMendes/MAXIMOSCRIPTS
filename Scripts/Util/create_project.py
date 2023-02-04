import csv
import os

defPath = 'PATH'

def makeDir(dir):
    newpath = defPath+dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)

with open('data.CSV', mode ='r', encoding="utf8") as file:
    csvFile = csv.reader(file, delimiter=';')

    for lines in csvFile:
        directory = lines[0]
        makeDir(directory)
        with open(defPath+directory+'\\res.txt', 'w') as f:
            f.write('\n\n'.join(lines))
    file.close()
