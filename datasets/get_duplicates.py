f=open("duplicate_images.txt", 'r')
f1=open("unique_duplicate_images", 'w')

l=[]
cnt=0
for line in f.readlines():
    if line=='\n':
        for i in l:
            if i[-4:]=='json':
                print i
                l=[]
                break
            else:
                cnt=cnt+ len(l)-1
                for k in l:
                    f1.write(k+'\n')
                f1.write('\n')
                l=[]
                break
    else:
        line=line[:-1]
        l.append(line)

print cnt
