from os import listdir
from os.path import isfile, join

f1=open('person_not_found_phase5.csv', 'w')

for files in listdir('../../phase5'):
    try:
        f=open('../../phase5/'+files,'r')
    except:
        continue
    for line in f.readlines():
        if line=='Person not found':
            f1.write(files[:-4]+'\n')



