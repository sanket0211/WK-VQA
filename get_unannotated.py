f=open('phase1AnnCloseList.csv' ,'r')
f2=open('unannotated_5.csv','w')
cnt=1
for line in f.readlines():
    if cnt>int(47283):
        line=line[:-1]
        line=line.split('\t')
        print line[9]
        if (line[9]=='FIVE'):
            f2.write(str(cnt)+'\n')
    cnt=cnt+1
