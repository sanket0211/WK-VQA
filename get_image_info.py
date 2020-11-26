f=open('phase1AnnCloseList.csv', 'r')
cnt=1
x=raw_input()
for line in f.readlines():
    if cnt>=int(x):
        print line
        exit()
    cnt=cnt+1
