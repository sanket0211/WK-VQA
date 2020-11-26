import time

f=open('ms_cap2_entities_dexter_wikiVQA_msCap_st1_en71928.csv', 'r')
f2=open('../phase1AnnCloseList.csv','r' )
#f2=open('../../wikiAttributesExtr/twoFaceAnnotationPartA-1.0.csv','r' )
#f2=open('../../wikiAttributesExtr/fiveFace.csv','r' )
#f2=open('../../wikiAttributesExtr/threefaceAnn.csv','r' )
#f2=open('../../wikiAttributesExtr/fourFace.csv','r' )

#human_entities=[]
#ms_cap_entities=[]
'''for line in f2.readlines():
    line=line.split('\t')
    if line[9]=='ONE':
        line=line[2]
        line = line.replace("_"," ")
        human_entities.append(line)
    else:
        human_entities.append('-1')
        '''

human_entities={}
ms_cap_entities=[]
cnt=1
for line in f2.readlines():
    line=line.split('\t')
    l=[]
    if line[9]!='ONE':
        cnt=cnt+1
        continue
    if line[2]=="":
        cnt=cnt+1
        continue
    '''if line[2]=="":
        continue
    if line[3]=="":
        continue
    if line[4]=="":
        continue
    if line[5]=="":
        continue'''
    line[2]=line[2].replace("_", " ")
    l.append(line[2].upper())
    '''l.append(line[2].upper())
    l.append(line[3].upper())
    l.append(line[4].upper())
    l.append(line[5].upper())'''
    #human_entities[str(cnt)]=l
    human_entities[str(cnt)]=l
    cnt=cnt+1
#print human_entities
print len(human_entities)
cnt1=0
cnt2=0
cnt3=0
cnt4=0
cnt5=0
ms_cap_entities.append([])
for line in f.readlines():
    if line=='\n':
        continue
    line = line[:-1]
    line = line.split('\t')
    line[0]=line[0].split(';')
    #print line[0]
    if line[0]=='Nothing detected\n':
        cnt2=cnt2+1
        ms_cap_entities.append(line[0][1:])
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
type1_2=0
#f=open('1-face_ms/correct.csv', 'w')
for i in range(1,len(ms_cap_entities)+1):
    if str(i) not in human_entities:
        continue
    if len(human_entities[str(i)])<1:
        continue
    #if ms_cap_entities[i].upper()==human_entities[i].upper():
    #    f.write(str(i)+'\n')
    #    type1=type1+1
    #print ms_cap_entities[i]
    #print human_entities[str(i)]
    if ms_cap_entities[i]==[] or ms_cap_entities[i]=='Nothing detected\n':
        type3=type3+1
        continue
    #elif ms_cap_entities[i]!=human_entities[i]:
    #    print ms_cap_entities[i]
    #    print human_entities[i]
    #    type2=type2+1
    cnt=0
    for j in ms_cap_entities[i]:
        if j.upper() in human_entities[str(i)]:
            cnt+=1
    if cnt == len(human_entities[str(i)]):
        type1+=1
    elif cnt>0 and cnt<(len(human_entities[str(i)])):
        type1_2+=1
    else:
        type2+=1

print type1
print type1_2
print type2
print type3















