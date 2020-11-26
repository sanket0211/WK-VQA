import random

f=open('exp_data.csv','w')

for x in range(3000):
    ele=random.randint(2,6)
    temp_l=[]
    for i in range(0,ele):
        temp_l.append(random.randint(1,101))
    temp_l.sort()
    l=[]
    for i in range(0,ele):
        l.append([temp_l[i], i])
    tot_str=""
    tot_str+='timepass\t'
    tot_str+=str(ele)
    for i in l:
        tot_str+='\t'
        tot_str=tot_str+str(i[0])
    l.sort()
    if ele==2:
        f.write(tot_str + '\t'+'Who is in the left?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is in the right?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[1][1])+'?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[0][1])+'?'+'\t'+str(l[1][1])+'\n')
    if ele==3:
        f.write(tot_str + '\t'+'Who is in the left?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is in the center?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is in the right?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[1][1])+' ?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[1][1])+'?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[2][1])+'?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[0][1])+'?'+'\t'+str(l[1][1])+'\n')
    if ele==4:
        f.write(tot_str + '\t'+'Who is in the left?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is second from left?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is second from right?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is in the right?'+'\t'+str(l[3][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[1][1])+'?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[1][1])+'?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[2][1])+'?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[0][1])+'?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[2][1])+'?'+'\t'+str(l[3][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[3][1])+'?'+'\t'+str(l[2][1])+'\n')
    if ele==5:
        f.write(tot_str + '\t'+'Who is in the left?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is second from left?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is second from right?'+'\t'+str(l[3][1])+'\n')
        f.write(tot_str + '\t'+'Who is in the right?'+'\t'+str(l[4][1])+'\n')
        f.write(tot_str + '\t'+'Who is in the center?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[1][1])+'?'+'\t'+str(l[0][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[1][1])+'?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[2][1])+'?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[0][1])+'?'+'\t'+str(l[1][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[2][1])+'?'+'\t'+str(l[3][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[3][1])+'?'+'\t'+str(l[2][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the right of '+str(l[3][1])+'?'+'\t'+str(l[4][1])+'\n')
        f.write(tot_str + '\t'+'Who is to the left of '+str(l[4][1])+'?'+'\t'+str(l[3][1])+'\n')


    

