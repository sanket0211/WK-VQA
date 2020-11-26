import glob   
import json

outfile = 'complete_data.json'
o=open(outfile,'w+')
path = 'QA_temp1/*.csv'   
files=glob.glob(path)   
image_id_wise_dict={}
face_wise_dict={}
for file in files:     
    f=open(file, 'r')
    print file
    file = file.split('/')
    file = file[1].split('-')
    print file[0]
    lines = f.readlines()
    questions=[]
    answers=[]
    QA={}
    for line in lines:
        line = line[:-1]
        print line
        line = line.split('\t')
        q=line[0]
        a=line[1]
        questions.append(q)
        answers.append(a)
    QA['questions']=questions
    QA['answers']=answers
    image_id_wise_dict[file[0]]=QA
    f.close() 

face_wise_dict['1-face']=image_id_wise_dict

path = 'QA_temp2/*.csv'   
files=glob.glob(path)   
image_id_wise_dict={}
for file in files:     
    f=open(file, 'r')
    print file
    file = file.split('/')
    file = file[1].split('-')
    print file[0]
    lines = f.readlines()
    questions=[]
    answers=[]
    QA={}
    for line in lines:
        line = line[:-1]
        line = line.split('\t')
        q=line[0]
        a=line[1]
        questions.append(q)
        answers.append(a)
    QA['questions']=questions
    QA['answers']=answers
    image_id_wise_dict[file[0]]=QA
    f.close()


face_wise_dict['2-face']=image_id_wise_dict

path = 'QA_temp3/*.csv'   
files=glob.glob(path)   
image_id_wise_dict={}
for file in files:     
    f=open(file, 'r')
    print file
    file = file.split('/')
    file = file[1].split('-')
    print file[0]
    lines = f.readlines()
    questions=[]
    answers=[]
    QA={}
    for line in lines:
        line = line[:-1]
        line = line.split('\t')
        q=line[0]
        a=line[1]
        questions.append(q)
        answers.append(a)
    QA['questions']=questions
    QA['answers']=answers
    image_id_wise_dict[file[0]]=QA
    f.close() 
face_wise_dict['3-face']=image_id_wise_dict

path = 'QA_temp4/*.csv'   
files=glob.glob(path)   
image_id_wise_dict={}
for file in files:     
    f=open(file, 'r')
    print file
    file = file.split('/')
    file = file[1].split('-')
    print file[0]
    lines = f.readlines()
    questions=[]
    answers=[]
    QA={}
    for line in lines:
        line = line[:-1]
        line = line.split('\t')
        q=line[0]
        a=line[1]
        questions.append(q)
        answers.append(a)
    QA['questions']=questions
    QA['answers']=answers
    image_id_wise_dict[file[0]]=QA
    f.close() 
face_wise_dict['4-face']=image_id_wise_dict

path = 'QA_temp5/*.csv'   
files=glob.glob(path)   
image_id_wise_dict={}
for file in files:     
    f=open(file, 'r')
    print file
    file = file.split('/')
    file = file[1].split('-')
    print file[0]
    lines = f.readlines()
    questions=[]
    answers=[]
    QA={}
    for line in lines:
        line = line[:-1]
        line = line.split('\t')
        q=line[0]
        a=line[1]
        questions.append(q)
        answers.append(a)
    QA['questions']=questions
    QA['answers']=answers
    image_id_wise_dict[file[0]]=QA
    f.close() 

face_wise_dict['5-face']=image_id_wise_dict


o.write(json.dumps(face_wise_dict))
