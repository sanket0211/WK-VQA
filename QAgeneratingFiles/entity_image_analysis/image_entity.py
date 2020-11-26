import json

f1=open('../1-face_analysis/completely_annotated_file_info','r')
f2=open('../2-face_analysis/completely_annotated_file_info','r')
f3=open('../3-face_analysis/completely_annotated_file_info','r')
f4=open('../4-face_analysis/completely_annotated_file_info','r')
f5=open('../5-face_analysis/completely_annotated_file_info','r')

d={}
for line in f1.readlines():
	line=line[:-1]
	line=line.split('\t')
	if line[0] in d:
		d[line[0]].append(line[2])
	else:
		d[line[0]]=[line[2]]

for line in f2.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,4):
		line[i]=line[i]
		if line[0] in d:
			d[line[0]].append(line[i])
		else:
			d[line[0]]=[line[i]]

for line in f3.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,5):
		if line[0] in d:
			d[line[0]].append(line[i])
		else:
			d[line[0]]=[line[i]]

for line in f4.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,6):
		if line[0] in d:
			d[line[0]].append(line[i])
		else:
			d[line[0]]=[line[i]]

for line in f5.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,7):
		if line[0] in d:
			d[line[0]].append(line[i])
		else:
			d[line[0]]=[line[i]]


with open('image_entity.json', 'w') as fp:
    json.dump(d, fp)