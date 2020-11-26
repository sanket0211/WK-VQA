'''f = open('entity_list.csv', 'r')
f2=open('entity_list1.csv', 'r')
f3=open('new_entity_list.csv','w')
temp_dict=[]
cnt =0
for line in f2.readlines():
    line = line[:-1]
    temp_dict.append(line)

for line in f.readlines():
    line=line[:-1]
    if line not in temp_dict:
        f3.write(line+'\n')
'''
'''
f=open('../../wikiAttributesExtr/fourFace.csv', 'r')

for line in f.readlines():
    line=line.split('\t')
    if line[0]=='3134':
        print line
        break
'''
'''
from os import listdir
from os.path import isfile, join

mypath='/scratche/home/sanket/kvqa/QAgeneratingFiles/QA_temp2'
files1 = [f for f in listdir(mypath) if isfile(join(mypath, f))]


mypath='/scratche/home/sanket/kvqa/QAgeneratingFiles/QA_temp2_2'
files2 = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for l in files1:
    if l not in files2:
        print l
        '''

f=open('5-face_analysis/same_name.csv', 'r')

for line in f.readlines():
    line=line.split('\t')
    print line[0]

