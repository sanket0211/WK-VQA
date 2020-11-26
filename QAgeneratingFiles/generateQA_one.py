import sys
import csv
import pdb
import os
import random
from collections import defaultdict
#plot fields
labels=[]
fracs=[]
reload(sys)
sys.setdefaultencoding('utf-8')

csvFile = '../phase1AnnCloseList.csv'
person_token = {}
#p_token=open('person_tokens.csv','w+')


def checkAvail(f):
    if(os.path.isfile(f)):
      with open(f, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
            if(token[0]=="Person not found"):
                return(0)
            else:
                return(1)
    else:
       return(0)


def get_token_person(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile,delimiter='\t', quotechar='|')
        for token in spamreader:
          if token[0] in person_token:
            #print token[0]
            continue
          else:
            person_token[token[0]]=1
            p_token.write(token[0])
            p_token.write('\n')
    return
        
  
def getYOB(f):
    count=0
    with open(f, 'r') as csvfile:
       spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
       for token in spamreader:
           count=count+1
           if(count<4):
             continue
           dob=token[1].split('-')
           if len(dob)<3:
           	return 'NOT','NOT','NOT'
           else:
           	return dob[0],dob[1], dob[2]
           if(count>4):
              return 

def getYOD(f):
    with open(f, 'r') as csvfile:
       spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
       for token in spamreader:
           if token[0]=='Date of Death':
           		dod=token[1].split('-')
           		#print("here ",dod, len(dod))
           		if len(dod)!=3:
           			return 'NOT', 'NOT', 'NOT'
           		else:	
           			return dod[0],dod[1],dod[2]
       return -1,-1,-1

def getYOW(f):
    with open(f, 'r') as csvfile:
       spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
       for token in spamreader:
           if token[0]=='Work started':
           		dod=token[1].split('-')
           		#print("here ",dod, len(dod))
           		if len(dod)!=3:
           			return 'NOT'
           		else:	
           			return dod[0]
       return -1
def getPlaceOfEducation(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='Educated at':
           		return token[1:]
    return

def getNickName(f):
	with open(f,'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for token in spamreader:
			if token[0]=='Nick Name':
				return token[1:]
	return

def getPoliticalParty(f):
	with open(f,'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for token in spamreader:
			if token[0]=='Political party':
				return token[1:]
	return

def getCountyOfBirth(f):
    count=0
    with open(f, 'r') as csvfile:
         spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
         for token in spamreader:
            count=count+1
            if(count<8):
                continue
            cob=token[1]
            return(cob)
            if(count>8):
               return

def getLanguage(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='Knows Language':
           		return token[1:]
    return

def getNativeLanguage(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='Native Languages':
           		return token[1:]
    return

def getoccupation(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='Occupation':
           		return token[1:]
    return

def getPoliticalPartyFounder(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='Founder of his party':
           		return token[1]
    return


def getContinentOfBirth(f):
    count=0
    with open(f, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
            count=count+1
            if(count<9):
              continue
            cob=token[1]
            return(cob)
            if(count>9):
               return
   
temp_dict={}

def fillplotdict(key):
	if key in temp_dict:
		temp_dict[key]+=1
	else:
		temp_dict[key]=1
	return

def normalizeplot():
	total = 0
	for i in temp_dict:
		total += temp_dict[i]
	print total
	for i in temp_dict:
		temp_dict[i] = (float(temp_dict[i])/float(total))*float(100)

def plotdetails():
	for i in temp_dict:
		labels.append(i)
		fracs.append(temp_dict[i])


def get_image_path(imgId):
    f=open('../phase1AnnCloseList.csv')
    row_no=0
    for line in f.readlines():
        row_no+=1
        if row_no!=int(imgId):
            continue
        else:
            line=line.split('\t')
            return line[0]
            break

    

a1=open('1-face_analysis/files_info.csv', 'w')
a2=open('1-face_analysis/questions_count.csv', 'w')
a3=open('1-face_analysis/entities_files_present.csv', 'w')
a4=open('1-face_analysis/entities_files_absent.csv', 'w')
a5=open('1-face_analysis/partially_annotated_file_info.csv', 'w')
a6=open('1-face_analysis/completely_annotated_file_info', 'w')
a7=open('1-face_analysis/complete_analysis.csv', 'w')
a8=open('1-face_analysis/ambiguous_our.csv', 'w')
a9=open('1-face_analysis/answers_count.csv', 'w')

answers_info={}
file_info={}
question_info={}
entities_info={}
qa={}
file_info = defaultdict(lambda: 0, file_info)
question_info = defaultdict(lambda: 0, question_info)
entities_info = defaultdict(lambda: 0, entities_info)
answers_info = defaultdict(lambda: 0, answers_info)

entity_file_present=[]
entity_file_absent=[]
unique_images=[]

person_not_found=[]
pnf=open('filtered_data_analysis/person_not_found.csv', 'r')
for line in pnf.readlines():
    line=line[:-1]
    person_not_found.append(line)
person_data_missing=[]
pnf=open('filtered_data_analysis/person_data_missing.csv', 'r')
for line in pnf.readlines():
    line=line[:-1]
    person_data_missing.append(line)

correct_names=[]
cns1=open("filtered_data_analysis/wiki_data_req_persons_url.csv", 'r')
for line in cns1.readlines():
    line=line[:-1]
    correct_names.append(line)
final_correct_names={}

for i in range(0,len(correct_names)):
    final_correct_names[person_not_found[i]]=correct_names[i]

actual_names=[]
cns1=open("filtered_data_analysis/wiki_data_req_persons_actual_names.csv", 'r')
for line in cns1.readlines():
    line=line[:-1]
    actual_names.append(line)
final_actual_names={}

for i in range(0,len(actual_names)):
    final_actual_names[person_not_found[i]]=actual_names[i]

dup1=open('../datasets/1-face_dup2.csv','r')
dups=[]
for line in dup1.readlines():
    line=line[:-1]
    dups.append(int(line))

to1=open('1-face_analysis/total_outliers.csv','r')
to=[]
for line in to1.readlines():
    line=line[:-1]
    print line
    to.append(int(line))
with open(csvFile, 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     cnt=1
     for token in spamreader:
         actualperson1=""
         if cnt>47283:
             break
         imgId=cnt
         if imgId in dups or imgId in to:
             print imgId
             cnt=cnt+1
             continue
         if imgId in unique_images:
             continue
         unique_images.append(imgId)
         cnt=cnt+1
         if(token[9]!='ONE'):
           continue
   
         y1=-1
         y2=-1
         person1=(token[2].lstrip()).rstrip()
         if(person1==""):
           file_info['Not Annotated']+=1  
           a5.write(str(imgId)+'\t'+token[0]+'\t'+person1+'\n')
           continue
         #fillplotdict(person1)
         person1=person1.replace(" ","_")
         if person1 in person_not_found:
             actualperson1=final_actual_names[person1]
             person1=final_correct_names[person1]
         f1="../../wikiAttributesExtr/%s.csv" %(person1)
         flag1=checkAvail(f1)
         if flag1!=1 or person1 in person_data_missing:
             if person1 not in entity_file_absent:
                 entity_file_absent.append(person1)
         if person1 in person_data_missing:
            flag1=0;

         if(flag1!=1):
           file_info['Ambiguous_our']+=1  
           a8.write(str(imgId)+'\t'+token[0]+'\t'+person1+'\n')
           continue
         if(flag1==1):
           if actualperson1!="":
               person1=actualperson1.replace("_"," ")   
           else:
               person1=person1.replace("_"," ")
           if person1 not in entity_file_present:
               entity_file_present.append(person1)
           file_info['Annotated']+=1
           a6.write(str(imgId)+'\t'+token[0]+'\t'+person1+'\n')
           qFileName='QA_temp1/%s-QA.csv' %(imgId)
           qFile=open(qFileName,'w+')
           qFile.write("Who is the person in the image?\t")
           question_info["Who is in the [position]"]+=1
           qFile.write(person1)
           q="Who is in the [position]?"
           a=person1
           if q not in qa:
               qa[q]={}
               qa[q]=defaultdict(lambda:0, qa[q])
           else:
               qa[q][a]+=1
           answers_info[person1]+=1
           qFile.write("\n")
          # print person1
           #get_token_person(f1)
           #get_token_person(f2)
           #continue
           yob1,mob1,dob1=getYOB(f1)
           try:
               if int(yob1)<min_date:
                   min_date=yob1
               if int(yob1)>max_date:
                   max_date=yob1
           except:
               x=1
           yod1,mod1,dod1=getYOD(f1)
           try:
            if(yob1!=-1 and yob1!='NOT'):
                if(yod1!=-1 and yod1!='NOT'):
             	    qFile.write("For how many years did the person in the image live?\t") 
             	    qFile.write(str((int(yod1)-int(yob1))))
                    answers_info[str((int(yod1)-int(yob1)))]+=1
             	    qFile.write("\n")
                    question_info['For how many years did the person in the image live?']+=1
                    q='For how many years did the person in the image live?'
                    a=str((int(yod1)-int(yob1)))
                    if q not in qa:
                        qa[q]={}
                        qa[q]=defaultdict(lambda:0, qa[q])
                    else:
                        qa[q][a]+=1
           except:
               x=1

           try:
            if(yob1!=-1 and yob1!='NOT'):
                ques='Was the person in the image born after the end of World War II?\t'
                if int(yob1)>1945 :
                    ans = 'Yes'
                else:
                    ans = 'No'
                qFile.write(ques)
                question_info["Was the person in the image born after the end of World War II?"]+=1
                qFile.write(ans+'\n')
                answers_info[ans]+=1
                q="Was the person in the image born after the end of World War II?"
                a=ans
                if q not in qa:
                    qa[q]={}
                    qa[q]=defaultdict(lambda:0, qa[q])
                else:
                    qa[q][a]+=1
           except:
               x=1

             
           yow1=getYOW(f1)
           try:
            if(yow1!=-1 and yow1!='NOT'):
                if(yow1!=-1 and yow1!='NOT'):
             	    qFile.write("In which year did the person in the image start working?\t") 
             	    qFile.write(yow1)
                    answers_info[yow1]+=1
             	    qFile.write("\n")
                    question_info["In which year did the person in the image start working?"]+=1
                    q="In which year did the person [position] in the image start working?"
                    a=yow1
                    if q not in qa:
                        qa[q]={}
                        qa[q]=defaultdict(lambda:0, qa[q])
                    else:
                        qa[q][a]+=1
           except:
               x=1


           countryOB1=getCountyOfBirth(f1)
           continentOB1=getContinentOfBirth(f1)
           if(countryOB1 !='NOT-AVAILABLE' ):
           		ques="Which country is the person in the image born in?\t"
           		ans = countryOB1
           		qFile.write(ques)
           		qFile.write(ans+'\n')
                        answers_info[ans]+=1
                        question_info["Which country is the person in the image born in?"]+=1
                        q="Which country is the person in the image born in?"
                        a=ans
                        if q not in qa:
                            qa[q]={}
                            qa[q]=defaultdict(lambda:0, qa[q])
                        else:
                            qa[q][a]+=1
            	
           if(continentOB1!='NOT-AVAILABLE'):
           		ques="Which continent is the person in the image born in?\t"
                        ans = continentOB1
           		qFile.write(ques)
           		qFile.write(ans+'\n')
                        answers_info[ans]+=1
           		question_info["Which continent is the person in the image born in?"]+=1
                        q="Which continent is the person in the image born in?"
                        a=ans
                        if q not in qa:
                            qa[q]={}
                            qa[q]=defaultdict(lambda:0, qa[q])
                        else:
                            qa[q][a]+=1
           	 ##The Following questions are related to Languages
           
           

           '''language1=getLanguage(f1)
           if language1[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 total_list_of_languages = []
           	 #print language1[0]
           	 #print language2[0]

           	 if language1[0]!='NOT-AVAILABLE':
           	 	language1[0]=eval(language1[0])
           	 	for l in language1[0]:
           	 		total_list_of_languages.append(l)
           	 
           	 temp_languages = ['English', 'German', 'Tamil', 'Telugu']
           	 ques = 'How many different languages does the person in the image speak?\t'
                 ans = len(total_list_of_languages)
                 qFile.write(ques)
                 question_info["How many different languages does the person in the image speak?"]+=1
                 qFile.write(str(ans)+'\n')
           	 p = random.randint(0,1)
           	 if(p==0):
           	 	language = total_list_of_languages[0]
           	 else:
           	 	for l in temp_languages:
           	 		if l not in total_list_of_languages:
           	 			language = l
           	 			break
           	 ques = 'Does person in the image speak '+language+'?'
           	 if language in language1[0]:
           	 	ans = 'Yes'
           	 else:
           	 	ans = 'No'
           	 qFile.write(ques+'\t')
           	 qFile.write(ans+'\n')
                 question_info['Does person in the image speak [language]?']+=1

           '''

           native_language1=getNativeLanguage(f1)
           if native_language1[0]!='NOT-AVAILABLE':
           	 native_language1[0]=eval(native_language1[0])
           	 total_list_of_languages = []
           	 ques = 'What is the native language of the person in the image?'
           	 ans = native_language1[0][0]
           	 qFile.write(ques+'\t')
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 question_info[ques]+=1
                 q=ques
                 a=ans
                 if q not in qa:
                     qa[q]={}
                     qa[q]=defaultdict(lambda:0, qa[q])
                 else:
                     qa[q][a]+=1

           
           political_party1=getPoliticalParty(f1)
           political_party_founder1 = getPoliticalPartyFounder(f1)
           if political_party1[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 total_list_of_political_party = []
           	 for n in political_party1:
           	 	total_list_of_political_party.append(n)
           	 total_no_of_political_party = len(total_list_of_political_party)
           	 ques = 'How many political parties has the person in the image been a part of?'
           	 ans = total_no_of_political_party
            
           	 qFile.write(ques+'\t')
           	 qFile.write(str(ans)+'\n')
                 answers_info[str(ans)]+=1
                 question_info[ques]+=1
                 q=ques
                 a=str(ans)
                 if q not in qa:
                     qa[q]={}
                     qa[q]=defaultdict(lambda:0, qa[q])
                 else:
                     qa[q][a]+=1

       	   if political_party_founder1!='NOT-AVAILABLE':
       	   	 #print imgId
       	   	 ques = 'Who is the founder of the Political Party person in the image belongs to?'
       	   	 ans = political_party_founder1
       	   	 qFile.write(ques+'\t')
       	   	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 question_info["Who is the founder of the Political Party person [position] belongs to?"]+=1
                 q="Who is the founder of the Political Party person [position] belongs to?"
                 a=ans
                 if q not in qa:
                     qa[q]={}
                     qa[q]=defaultdict(lambda:0, qa[q])
                 else:
                     qa[q][a]+=1

           occupation1=getoccupation(f1)
           if occupation1[0]!='NOT-AVAILABLE' or occupation1[0]!='':
           	 total_list_of_occupations = []
           	 #print language1[0]
           	 #print language2[0]
           	 if occupation1[0]!='NOT-AVAILABLE':
           	 	occupation1[0]=eval(occupation1[0])
           	 	for l in occupation1[0]:
           	 		total_list_of_occupations.append(l)
           	 temp_occupations = ['actor', 'politician','sprinter','diplomat']

           	 total_no_of_occupations = len(total_list_of_occupations)
           	 p=random.randint(0,1)
                 if total_no_of_occupations == 0:
                     p=1
           	 if p==0:
           	 	occupation = total_list_of_occupations[0]
           	 else:
           	 	for l in temp_occupations:
           	 		if l not in total_list_of_occupations:
           	 			occupation=l
           	 			break
           	 ques = 'Is the person in the image '+ occupation +'?'
           	 if occupation in total_list_of_occupations:
           	 	ans = "Yes"
           	 else:
           	 	ans = "No"
           	 qFile.write(ques+'\t')
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 question_info["Is the person in the image [Occupation]?"]+=1
                 q="Is the person in the image [Occupation]?"
                 a=ans
                 if q not in qa:
                     qa[q]={}
                     qa[q]=defaultdict(lambda:0, qa[q])
                 else:
                     qa[q][a]+=1


import json

with open('1-face_analysis/qa.json', 'w') as fp:
    json.dump(qa, fp)

#print(temp_dict)
#normalizeplot()
#plotdetails()
#print min_date
#print max_date
#print(len(labels))
#print(labels)
#print(fracs)
#the_grid = GridSpec(1, 1)
#plt.subplot(the_grid[0, 0], aspect=1)
#plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)      
#plt.show()
#plt.savefig('1-face_plots/1.png', bbox_inches='tight')

'''el = open('entity_list.csv', 'r')
total_entities=[]
for line in el.readlines():
    line = line[:-1]
    total_entities.append(line)

for i in labels:
    if i not in total_entities:
        total_entities.append(i)


for i in total_entities:
    print i
'''
no_of_words=0
for i in entity_file_present:
    a3.write(i+'\n')
for i in entity_file_absent:
    a4.write(i+'\n')
for key in file_info:
    a1.write(key+'\t'+str(file_info[key])+'\n')
total=0
for key in question_info:
    total+=question_info[key]
    a2.write(key+'\t'+str(question_info[key])+'\n')
    no_of_words= no_of_words + (question_info[key]*len(key.split(' ')))

a2.write("Total Questions\t"+str(total)+'\n')
a2.write("Average Question Length\t"+ str(float(no_of_words)/float(total))+'\n')


total2=0
no_of_words=0
for key in answers_info:
    total2+=answers_info[key]
    a9.write(key+'\t'+str(answers_info[key])+'\n')
    no_of_words= no_of_words + (answers_info[key]*len(key.split(' ')))

a9.write("Total unique Answers\t"+str(len(answers_info))+'\n')
a9.write("Average Answers Length\t"+ str(float(no_of_words)/float(total2))+'\n')

total_files = file_info['Not Annotated']+file_info['Annotated']
total_questions = total
total_entities=len(entity_file_present)+len(entity_file_absent)

a7.write("Total Files\t"+ str(total_files)+'\n')
a7.write("Total Annotated Files\t"+ str(file_info['Annotated'])+'\n')
a7.write("Total Partially Annotated Files\t"+ str(file_info['Not Annotated'])+'\n')
a7.write("Total Question\t"+ str(total_questions)+'\n')
a7.write("Total Entities\t"+ str(total_entities)+'\n')
a7.write("Entity File Present\t"+str(len(entity_file_present))+'\n')
a7.write("Entity File Absent\t"+str(len(entity_file_absent))+'\n')
a7.write("Total unique answers\t"+str(len(answers_info)))

