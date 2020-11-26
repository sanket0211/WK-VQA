import random
f=open('train.csv','w')
universities=[]
uni_f=open('universities.csv', 'r')
e_f=open('entities.csv','r')
entities=[]
c_f=open('countries.csv', 'r')
countries=[]
cnt=1
continents=['Asia','North America','South America','Australia', 'Antarctica', 'Africa', 'Europe']
ocu_f=open('occupation.csv')
occupations=[]
for line in e_f.readlines():
    line=line[:-1]
    line=line.split(" ")
    entities.append(line[0])
for line in uni_f.readlines():
    line=line[:-1]
    line=line.split(',')
    try:
        line[1]=line[1].encode("utf-8")
        universities.append(line[1])
    except:
        pass
for line in c_f.readlines():
    line=line[:-1]
    countries.append(line)

for line in ocu_f.readlines():
    line=line[:-1]
    occupations.append(line)
def create_memory():
    '''for j in range(0,loop):
        f.write('timepass'+'\t'+str(ages[j][1])+' is '+ str(ages[j][0])+' years old.'+'\n')'''
    for j in range(0,loop):
        f.write('timepass'+'\t'+str(cords[j][1])+' is at position '+ str(cords[j][0])+'\n')
    '''for j in range(0,loop):
        f.write('timepass'+'\t'+str(univ[j][1])+' studied at '+ str(univ[j][0])+'\n')
    for j in range(0,loop):
        f.write('timepass'+'\t'+str(count[j][1])+' was born at '+ str(count[j][0])+'\n')
    for j in range(0,loop):
        f.write('timepass'+'\t'+str(contin[j][1])+' was born in continent '+ str(contin[j][0])+'\n')
    for j in range(0,loop):
        f.write('timepass'+'\t'+str(ocu[j][1])+' is '+ str(ocu[j][0])+' by profession'+'\n')
    for j in range(0,loop):
        f.write('timepass'+'\t'+str(birth[j][1])+' is born in '+ str(birth[j][0])+'\n')
    for j in range(0,loop):
        f.write('timepass'+'\t'+str(birth[j][1])+' started working in '+ str(birth[j][0])+'\n')'''

def create_person_attributes():
    l=[];p=[];q=[];m=[];n=[];o=[];r=[]
    a=random.randint(1,100)
    l.append(a)
    l.append(img_ent[j])
    ages.append(l)
    a=random.randint(1,100)
    p.append(a)
    p.append(img_ent[j])
    cords.append(p)
    a=random.randint(1,len(universities)-1)
    q.append(universities[a])
    q.append(img_ent[j])
    univ.append(q)
    a=random.randint(1,len(countries)-1)
    m.append(countries[a])
    m.append(img_ent[j])
    count.append(m)
    a=random.randint(1,len(continents)-1)
    n.append(continents[a])
    n.append(img_ent[j])
    contin.append(n)
    a=random.randint(1,len(occupations)-1)
    o.append(occupations[a])
    o.append(img_ent[j])
    ocu.append(o)
    a=random.randint(11,99)
    r.append('19'+str(a))
    r.append(img_ent[j])
    birth.append(r)

for i in range(0,4000):
    loop=random.randint(1,5)
    ages=[];cords=[];univ=[];count=[];contin=[];ocu=[];birth=[]
    #e=random.randint(1,10)
    e=0
    img_ent=[]
    img_ent.append(entities[e]),img_ent.append(entities[e+1]),img_ent.append(entities[e+2]), img_ent.append(entities[e+3]),img_ent.append(entities[e+4])
    for j in range(0,loop):
        create_person_attributes()
    ages.sort()
    cords.sort()
    #######
    #create_memory()
    #f.write('timepass'+'\t'+'Who is the eldest of all?'+'\t'+str(ages[loop-1][1])+'\t'+'1'+'\n')
    ##############
    #create_memory()
    a=random.randint(0,loop-1)
    b=random.randint(0,loop-1)
    a=img_ent[a]
    b=img_ent[b]
    print loop
    for i in ages:
        print i
        if i[1]==a:
            one = i[0]
        if i[1]==b:
            two = i[0]
    diff = str(abs(one - two))
    #f.write('timepass'+'\t'+'What is age gap between '+str(a)+' and '+str(b)+'?'+'\t'+diff+'\t'+'1'+'\n')
    ######
    create_memory()
    f.write('timepass'+'\t'+'Who is the leftmost person?'+'\t'+str(cords[0][1])+'\t'+'1'+'\n')
    #########
    create_memory()
    f.write('timepass'+'\t'+'Who is in the right?'+'\t'+str(cords[loop-1][1])+'\t'+'1'+'\n')
    create_memory()
    if loop==3:
        create_memory()
        f.write('timepass'+'\t'+'Who is in the center?'+'\t'+str(cords[loop-2][1])+'\t'+'1'+'\n')
    if loop==4:
        create_memory()
        f.write('timepass'+'\t'+'Who is second from left?'+'\t'+str(cords[1][1])+'\t'+'1'+'\n')
        create_memory()
        f.write('timepass'+'\t'+'Who is second from right?'+'\t'+str(cords[2][1])+'\t'+'1'+'\n')
    if loop==5:
        create_memory()
        f.write('timepass'+'\t'+'Who is in the center?'+'\t'+str(cords[2][1])+'\t'+'1'+'\n')
        create_memory()
        f.write('timepass'+'\t'+'Who is second from left?'+'\t'+str(cords[1][1])+'\t'+'1'+'\n')
        create_memory()
        f.write('timepass'+'\t'+'Who is second from right?'+'\t'+str(cords[2][1])+'\t'+'1'+'\n')
    ######
    #create_memory()
    for i in univ:
        if i[1]==cords[0][1]:
            ans=str(i[0])
            break
    #f.write('timepass'+'\t'+'Which university did the leftmost person go to?'+'\t'+str(ans)+'\t'+'1'+'\n')
    #create_memory()
    for i in univ:
        if i[1]==cords[loop-1][1]:
            ans=str(i[0])
            break
    #f.write('timepass'+'\t'+'Which university did the rightmost person go to?'+'\t'+str(ans)+'\t'+'1'+'\n')


f=open('test.csv','w')

for i in range(0,400):
    loop=random.randint(1,5)
    ages=[]
    cords=[]
    count=[]
    contin=[]
    #e=random.randint(1,10)
    e=0
    img_ent=[]
    img_ent.append(entities[e]),img_ent.append(entities[e+1]),img_ent.append(entities[e+2]), img_ent.append(entities[e+3]),img_ent.append(entities[e+4])
    for j in range(0,loop):
        create_person_attributes()
    ages.sort()
    cords.sort()
    #create_memory()
    #f.write('timepass'+'\t'+'Who is the eldest of all?'+'\t'+str(ages[loop-1][1])+'\t'+'1'+'\n')
    ##########
    #create_memory()
    a=random.randint(0,loop-1)
    b=random.randint(0,loop-1)
    print a
    print b
    print loop
    for i in ages:
        print i
        if i[1]==a:
            one = i[0]
        if i[1]==b:
            two = i[0]
    diff = str(abs(one - two))
    #f.write('timepass'+'\t'+'What is age gap between '+str(a)+' and '+str(b)+'?'+'\t'+diff+'\t'+'1'+'\n')
    ##############
    create_memory()
    f.write('timepass'+'\t'+'Who is the leftmost person?'+'\t'+str(cords[0][1])+'\t'+'1'+'\n')
    ##########
    create_memory()
    f.write('timepass'+'\t'+'Who is in the right?'+'\t'+str(cords[loop-1][1])+'\t'+'1'+'\n')
    create_memory()
    f.write('timepass'+'\t'+'Who is in the right?'+'\t'+str(cords[loop-1][1])+'\t'+'1'+'\n')
    create_memory()
    if loop==3:
        create_memory()
        f.write('timepass'+'\t'+'Who is in the center?'+'\t'+str(cords[loop-2][1])+'\t'+'1'+'\n')
    if loop==4:
        create_memory()
        f.write('timepass'+'\t'+'Who is second from left?'+'\t'+str(cords[1][1])+'\t'+'1'+'\n')
        create_memory()
        f.write('timepass'+'\t'+'Who is second from right?'+'\t'+str(cords[2][1])+'\t'+'1'+'\n')
    if loop==5:
        create_memory()
        f.write('timepass'+'\t'+'Who is in the center?'+'\t'+str(cords[2][1])+'\t'+'1'+'\n')
        create_memory()
        f.write('timepass'+'\t'+'Who is second from left?'+'\t'+str(cords[1][1])+'\t'+'1'+'\n')
    ##########
    #create_memory()
    for i in univ:
        if i[1]==cords[0][1]:
            ans=str(i[0])
            break
    #f.write('timepass'+'\t'+'Which university did the leftmost person go to?'+'\t'+str(ans)+'\t'+'1'+'\n')
    #create_memory()
    for i in univ:
        if i[1]==cords[loop-1][1]:
            ans=str(i[0])
            break
    #f.write('timepass'+'\t'+'Which university did the rightmost person go to?'+'\t'+str(ans)+'\t'+'1'+'\n')
