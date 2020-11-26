f=open('../phase1AnnCloseList.csv')

img_paths=[]
d={}
cnt=1
for line in f.readlines():
    line=line.split('\t')
    img_paths.append(line[0])
    d[line[0]]=cnt
    cnt=cnt+1

c=0
final_count=0
f2=open('unique_duplicate_images.csv', 'r')
f3=open('req_duplicate_images.csv','w')
f4=open('to_be_removed.csv','w')
l=[]
for line in f2.readlines():
    if line=='\n':
        for i in l:
            if i in img_paths:
                c=c+1
                if c>1:
                    f4.write(i+'\n')
                f3.write(str(d[i])+'\n')
        f3.write('\n')
        if c>1:
            final_count=final_count+c-1
        c=0
        l=[]
    else:
        l.append(line[:-1])

print final_count
    


