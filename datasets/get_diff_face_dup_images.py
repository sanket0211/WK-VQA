f=open('../phase1AnnCloseList.csv','r')
f2=open('to_be_removed.csv', 'r')
f7=open('1-face_dup.csv','w')
f3=open('2-face_dup.csv','w')
f4=open('3-face_dup.csv','w')
f5=open('4-face_dup.csv','w')
f6=open('5-face_dup.csv','w')
f9=open('MORE.csv','w')
f10=open('NO.csv', 'w')
f8=open('temp.csv','w')
to_be_rem=[]
c=0
for line in f2.readlines():
    line=line[:-1]
    to_be_rem.append(line)
cnt=1
for line2 in f.readlines():
    line2=line2.split('\t')
    if line2[0] in to_be_rem:
        c=c+1
        if line2[9]=='ONE':
            f7.write(str(cnt)+'\n')
        elif line2[9]=='TWO':
            f3.write(str(cnt)+'\n')
        elif line2[9]=='THREE':
            f4.write(str(cnt)+'\n')
        elif line2[9]=='FOUR':
            f5.write(str(cnt)+'\n')
        elif line2[9]=='FIVE':
            f6.write(str(cnt)+'\n')
        elif line2[9]=='NO':
            f10.write(str(cnt)+'\n')
        elif line2[9]=='MORE':
            f9.write(str(cnt)+'\n')
    cnt+=1

print c
