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
	if line[2] in d:
		print(line[2])
		print(line[0])
		d[line[2]].append(line[0])
	else:
		d[line[2]]=[line[0]]

for line in f2.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,4):
		if line[i] in d:
			d[line[i]].append(line[0])
		else:
			d[line[i]]=[line[0]]

for line in f3.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,5):
		if line[i] in d:
			d[line[i]].append(line[0])
		else:
			d[line[i]]=[line[0]]

for line in f4.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,6):
		if line[i] in d:
			d[line[i]].append(line[0])
		else:
			d[line[i]]=[line[0]]

for line in f5.readlines():
	line=line[:-1]
	line=line.split('\t')
	for i in range(2,7):
		if line[i] in d:
			d[line[i]].append(line[0])
		else:
			d[line[i]]=[line[0]]


with open('entity_images.json', 'w') as fp:
    json.dump(d, fp)