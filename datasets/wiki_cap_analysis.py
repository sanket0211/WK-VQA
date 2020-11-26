import time

f=open('entities_dexter_wikiVQA_wikiCap_st1_en71928.csv', 'r')
f2=open('../phase1AnnCloseList.csv','r' )

human_entities=[]
ms_cap_entities=[]
for line in f2.readlines():
    line=line.split('\t')
    line=line[2]
    line = line.replace("_"," ")
    human_entities.append(line)

cnt1=0
cnt2=0
cnt3=0
cnt4=0
cnt5=0
for line in f.readlines():
    line = line.split('\t')
    if line[0]=='Nothing detected\n':
        cnt2=cnt2+1
        ms_cap_entities.append(line[0])
    elif line[0]=='\n':
        cnt4=cnt4+1
    elif line[0]=='':
        cnt1=cnt1+1
        ms_cap_entities.append(line[0])
    else:
        cnt3=cnt3+1
        line[0]=line[0][1:]
        ms_cap_entities.append(line[0])



type1=0
type2=0
type3=0
for i in range(0,len(human_entities)):
    if ms_cap_entities[i]==human_entities[i]:
        type1=type1+1
    elif ms_cap_entities[i]==''or ms_cap_entities[i]=='Nothing detected\n':
        type3=type3+1
    elif ms_cap_entities[i]!=human_entities[i]:
        type2=type2+1

print type1
print type2
print type3















