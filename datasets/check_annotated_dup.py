f=open('3-face_dup.csv','r')
f3=open('3-face_dup2.csv', 'w')
dups=[]
for line in f.readlines():
    line=line[:-1]
    dups.append(line)

f1=open('../QAgeneratingFiles/3-face_analysis/completely_annotated_file_info', 'r')
c=0
for line in f1.readlines():
    line=line.split('\t')
    line=line[0]
    if line in dups:
        f3.write(line+'\n')
print c
