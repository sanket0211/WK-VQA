from os import listdir
from os.path import isfile, join
import glob
f2=open('person_data_missing.csv','w')

for files in glob.glob('../../../../wikiAttributesExtr/*.csv'):
    try:
        f=open(files)
    except:
        flag=1
        continue
    flag=0
    for line in f.readlines():
        if line!='Person not found':
            line=line.split('\t')
            if len(line)<2:
                flag=1
                break
            #print linei
            line[1] = line[1].strip()
            try:
                if line[1]!='NOT-AVAILABLE\n' and line[1]!='[]\n' and line[1]!='NOT-AVAILABLE' and line[1]!='[]':
                    flag=1
                    break
            except:
                continue
        else:
            flag=1
            break
    if flag==0:
        print files[31:-4]
        f2.write(files[31:-4]+'\n')
    flag=0
