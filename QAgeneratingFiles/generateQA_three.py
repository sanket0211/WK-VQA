import sys
import csv
import pdb
import os
import random
from collections import defaultdict
import bs4
import requests
from bs4 import BeautifulSoup
import re
import urllib2


labels=[]
fracs=[]

reload(sys)
sys.setdefaultencoding('utf-8')


csvFile = '../../wikiAttributesExtr/threefaceAnn.csv'
person_token = {}


#p_token=open('person_tokens_three.csv','w+')
def checkAvail(f):
    if(os.path.isfile(f)):
      with open(f, 'r') as csvfile:
        try:
            spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        except:
            return(0)
        for token in spamreader:
            if(token[0]=="Person not found"):
                return(0)
            else:
                return(1)
        return(0)
    else:
       return(0)


def get_token_person(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile,delimiter='\t', quotechar='|')
        for token in spamreader:
          if token[0] in person_token:
            print token[0]
            continue
          else:
            person_token[token[0]]=1
            p_token.write(token[0])
            p_token.write('\n')
    return

def getYOB_complete(f):
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

def getYOD_complete(f):
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

        
  
def getYOB(f):
    count=0
    with open(f, 'r') as csvfile:
       spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
       for token in spamreader:
           count=count+1
           if(count<4):
             continue
           dob=token[1].split('-')
           return(dob[0])
           if(count>4):
              return 

def getPlaceOfEducation(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='Educated at':
           		return token[1:]
    return

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
def getSpouse(f):
    with open(f,'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for token in spamreader:
           if token[0]=='SpouseName':
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



a1=open('3-face_analysis/files_info.csv', 'w')
a2=open('3-face_analysis/questions_count.csv', 'w')
a3=open('3-face_analysis/entities_files_present.csv', 'w')
a4=open('3-face_analysis/entities_files_absent.csv', 'w')
a8=open('3-face_analysis/partially_annotated_file_info.csv', 'w')
a6=open('3-face_analysis/completely_annotated_file_info', 'w')
a7=open('3-face_analysis/complete_analysis.csv', 'w')
a5=open('3-face_analysis/ambiguous_file.csv', 'w')
a9=open('3-face_analysis/our_ambiguous_file.csv', 'w')
a10=open('3-face_analysis/same_name.csv', 'w')
a11=open('3-face_analysis/answers_count.csv', 'w')

answers_info={}
file_info={}
question_info={}
entities_info={}
file_info = defaultdict(lambda: 0, file_info)
question_info = defaultdict(lambda: 0, question_info)
entities_info = defaultdict(lambda: 0, entities_info)
answers_info = defaultdict(lambda: 0, answers_info)
qa={}
entity_file_present=[]
entity_file_absent=[]
                                                                    
unique_images=[]
sc=0

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

dup1=open('../datasets/3-face_dup2.csv', 'r')
dups=[]
for line in dup1.readlines():
    line=line[:-1]
    dups.append(line)


def qa_gen(ques, ans):
    if ques not in qa:
        qa[ques]={}
        qa[ques]=defaultdict(lambda: 0, qa[ques])
    else:
        qa[ques][ans]+=1

with open(csvFile, 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for token in spamreader:
         actualperson1=""
         actualperson2=""
         actualperson3=""
         persons=[]
         imgId=token[0]
         if imgId in dups:
             continue
         if imgId in unique_images:
             continue
         unique_images.append(imgId)
         if(token[4]=="NOT SURE" or token[5] == "ONE" or token[6]=="TWO" or token[7]=="FOUR" or token[8]=="FIVE" or token[9]=="MORE" or token[10]=="NO"):
             file_info['Ambiguous']+=1
             img_path=get_image_path(imgId)
             a5.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\n')

             continue
   
         y1=-1
         y2=-1
         person1=(token[1].lstrip()).rstrip()
         person2=(token[2].lstrip()).rstrip()
         person3=(token[3].lstrip()).rstrip()

         if(person1=="" and person2=="" and person3==""):
             file_info['Not Annotated']+=1
             img_path=get_image_path(imgId)
             a8.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\t'+token[4]+'\n')
             continue


         if(person1=="" or person2=="" or person3==""):
             file_info['Ambiguous']+=1
             img_path=get_image_path(imgId)
             a5.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\n')
             continue
         
         person1=person1.replace(" ","_")
         person2=person2.replace(" ","_")
         person3=person3.replace(" ","_")
         
         if person1 in person_not_found:
             actualperson1=final_actual_names[person1]
             person1=final_correct_names[person1]
         if person2 in person_not_found:
             actualperson2=final_actual_names[person2]
             person2=final_correct_names[person2]
         if person3 in person_not_found:
             actualperson3=final_actual_names[person3]
             person3=final_correct_names[person3]


         f1="../../wikiAttributesExtr/%s.csv" %(person1)
         
         f2="../../wikiAttributesExtr/%s.csv" %(person2)

         f3="../../wikiAttributesExtr/%s.csv" %(person3)
         flag1=checkAvail(f1)
         flag2=checkAvail(f2)
         flag3=checkAvail(f3)
         if flag1!=1 or person1 in person_data_missing:
             if person1 not in entity_file_absent:
                 entity_file_absent.append(person1)
         if flag2!=1 or person2 in person_data_missing:
             if person2 not in entity_file_absent:
                 entity_file_absent.append(person2)

         if flag3!=1 or person3 in person_data_missing:
             if person3 not in entity_file_absent:
                 entity_file_absent.append(person3)
         
         if person1 in person_data_missing:
            flag1=0;
         if person2 in person_data_missing:
            flag2=0;
         if person3 in person_data_missing:
            flag3=0;



         if(flag1*flag2*flag3!=1):
             file_info['Ambiguous_our']+=1
             img_path=get_image_path(imgId)
             a9.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\n')
         if(flag1*flag2*flag3==1):
           if actualperson1!="":
               person1=actualperson1.replace("_"," ")
           else:
               person1=person1.replace("_"," ")
           if actualperson2!="":
               person2=actualperson2.replace("_"," ")
           else:
               person2=person2.replace("_"," ")
           if actualperson3!="":
               person3=actualperson3.replace("_"," ")
           else:
               person3=person3.replace("_"," ")
           if person1 not in entity_file_present:
               entity_file_present.append(person1)
           if person2 not in entity_file_present:
               entity_file_present.append(person2)
           if person3 not in entity_file_present:
               entity_file_present.append(person3)
           #print person1+ " "+person2+" "+person3
           persons=[]
           persons.append(person1)
           persons.append(person2)
           persons.append(person3)
           persons_temp=persons
           persons = list(set(persons))
           if len(persons)<3:
               file_info['same_name']+=1
               img_path=get_image_path(imgId)
               a10.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\n')
               continue
           print imgId 
           file_info['Annotated']+=1
           persons=persons_temp
           img_path=get_image_path(imgId)
           a6.write(str(imgId)+'\t'+img_path+'\t'+person1+'\t'+person2+'\t'+person3+'\n')
           qFileName='QA_temp3/%s-QA.csv' %(imgId)
           qFile=open(qFileName,'w+')

           qFile.write("Who is in the left?\t")
           question_info["Who is in the [position]?"]+=1
           qFile.write(person1)
           answers_info[person1]+=1
           qFile.write("\n")
           sc=sc+4
           q="Who is in the [position]?"
           a=person1
           qa_gen(q,a)

           qFile.write("Who is in the right?\t")
           question_info["Who is in the [position]?"]+=1
           qFile.write(person3)
           answers_info[person3]+=1
           qFile.write("\n")
           sc=sc+4
           q="Who is in the [position]?"
           a=person3
           qa_gen(q,a)

           qFile.write("Who is in the centre?\t")
           question_info["Who is in the [position]"]+=1
           qFile.write(person2)
           answers_info[person2]+=1
           qFile.write("\n")
           sc=sc+4
           q="Who is in the [position]?"
           a=person2
           qa_gen(q,a)

           ques="Who is to the right of %s?\t" %(person2)
           question_info["Who is to the [position] of [person]?"]+=1
           qFile.write(ques)
           qFile.write(person3)
           answers_info[person3]+=1
           qFile.write("\n")
           sc=sc+4
           q="Who is to the [position] of [person]?"
           a=person3
           qa_gen(q,a)


           ques="Who is to the left of %s?\t" %(person2)
           question_info["Who is to the [position] of [person]?"]+=1
           qFile.write(ques)
           qFile.write(person1)
           answers_info[person1]+=1
           qFile.write("\n")
           sc=sc+8
           q="Who is to the [position] of [person]?"
           a=person1
           qa_gen(q,a)
             
           #get_token_person(f1)
           #get_token_person(f2)
           #get_token_person(f3)

           #continue
           y1=getYOB(f1)
           y2=getYOB(f2)
           y3=getYOB(f3)
            
           yob1,mob1,dob1=getYOB_complete(f1)
           yob2,mob2,dob2=getYOB_complete(f2)
           yob3,mob3,dob3=getYOB_complete(f3)
           yod1,mod1,dod1=getYOD_complete(f1)
           yod2,mod2,dod2=getYOD_complete(f2)
           yod3,mod3,dod3=getYOD_complete(f3)
           if(y1!=-1 and y2 != -1 and y3 != -1 and y1!='NOT' and y2!='NOT' and y3!='NOT' ):
             
             if(y1!=y2 and y2!=y3 and y1!=y3):
               qFile.write("Who among the people in the image is the eldest?\t") 
               sc+=11
               question_info["Who among the people in the image is the eldest?"]+=1
               if(y1 < y2 and y1<y3):
                 qFile.write("Person in the left")
                 answers_info["Person in the left"]+=1
                 a="Person in the left"
               elif(y2<y1 and y2<y3):
                 qFile.write("Person in the center")
                 answers_info["Person in the center"]+=1
                 a="Person in the center"
               else:
                 qFile.write("Person in the right")
                 answers_info["Person in the right"]+=1
                 a="Person in the right"
               qFile.write("\n")    
               q="Who among the people in the image is the eldest?"
               qa_gen(q,a)

             x1 = random.randint(0,2)
             x2 = random.randint(0,2)
             while x2==x1:
              x2=random.randint(0,3)

             if (x1+x2)==1:
              ques="What is the age gap between the leftmost and the centre person?\t"
              try:
                ans=abs(int(y1)-int(y2))
                qFile.write(ques)  
                qFile.write(str(ans)+' years')         
                question_info["What is the age gap between [person1] and [person2]?"]+=1
                qFile.write("\n")
                answers_info[str(ans)]+=1
                sc=sc+12
                q="What is the age gap between [person1] and [person2]?"
                a=str(ans)
                qa_gen(q,a)
              except:
                  pass
             if (x1+x2)==3:
              ques="What is the age gap between the centre and the rightmost person?\t"
              try:
                ans=abs(int(y2)-int(y3))
                qFile.write(ques)  
                qFile.write(str(ans)+ ' years')         
                answers_info[str(ans)]+=1
                qFile.write("\n")
                sc=sc+12
                question_info["What is the age gap between [person1] and [person2]?"]+=1
                q="What is the age gap between [person1] and [person2]?"
                a=str(ans)
                qa_gen(q,a)
              except:
                pass
             if (x1+x2)==2:
              ques="What is the age gap between the leftmost and the rigtmost person?\t"
              try:
                ans=abs(int(y1)-int(y3))
                qFile.write(ques)  
                qFile.write(str(ans)+ ' years')         
                answers_info[str(ans)]+=1
                qFile.write("\n")
                sc=sc+12
                question_info["What is the age gap between [person1] and [person2]?"]+=1
                q="What is the age gap between [person1] and [person2]?"
                a=str(ans)
                qa_gen(q,a)
              except:
                  pass
              if(yod1!=-1 and yod2 != -1 and yod1!='NOT' and yod2!='NOT' and yod3!=-1 and yod3!='NOT'):
              	qFile.write("Who among the people in the image lived longer?\t") 
              	delta_mon1 = (int(yod1)*12 + int(mod1) - 1) - (int(yob1)*12 + int(mob1) - 1)
              	delta_mon2 = (int(yod2)*12 + int(mod2) - 1) - (int(yob2)*12 + int(mob2) - 1)
              	delta_mon3 = (int(yod3)*12 + int(mod3) - 1) - (int(yob3)*12 + int(mob3) - 1)
              	if(delta_mon1>delta_mon2 and delta_mon1>delta_mon3):
              		qFile.write('Person in the left')
                        answers_info['Person in the left']+=1
                        ans='Person in the left'
              	elif (delta_mon2>delta_mon1 and delta_mon2>delta_mon3):
              		qFile.write('Person in the center')
                        answers_info['Person in the center']+=1
                        ans='Person in the center'
              	else:
              		qFile.write('Person in the right')
                        answers_info['Person in the right']+=1
                        ans='Person in the right'
                question_info["Who among the people in the image lived longer?"]+=1
              	qFile.write("\n")
                q="Who among the people in the image lived longer?"
                a=ans
                qa_gen(q,a)
                sc=sc+9
             try:
                 if(yob1!=-1 and yob2!=-1 and yob2!='NO' and yob1!='NO'and yob3!=-1 and yob3!='NO'):
                     ans=0
                     ques='How many people in the image were born after the end of World War II?'
                     if int(yob1)>1945:
                         ans = ans+1
                     if int(yob2)>1945:
                         ans = ans+1
                     if int(yob3)>1945:
                         ans = ans +1
                     qFile.write(ques+'\t')
                     question_info["How many people in the image were born after the end of World War II?"]+=1
                     qFile.write(str(ans)+'\n')
                     answers_info[str(ans)]+=1
                     q="How many people in the image were born after the end of World War II?"
                     a=str(ans)
                     qa_gen(q,a)
             except:
                 x=1
 
           
           yow1=getYOW(f1)
           yow2=getYOW(f2)
           yow3=getYOW(f3)
           try:
            if(yow1!=-1 and yow1!='NOT'):
                if(yow1!=-1 and yow1!='NOT'):
                    qFile.write("In which year did the person on the left in the image start working?\t")
                    qFile.write(yow1)
                    answers_info[yow1]+=1
                    qFile.write("\n")
                    question_info["In which year did the person [position] in the image start working?"]+=1
                    sc+=14
                    q="In which year did the person [position] in the image start working?"
                    a=yow1
                    qa_gen(q,a)
           except:
               x=1
           try:
            if(yow2!=-1 and yow2!='NOT'):
                if(yow2!=-1 and yow2!='NOT'):
                    qFile.write("In which year did the person on the right in the image start working?\t")
                    qFile.write(yow2)
                    answers_info[yow2]+=1
                    qFile.write("\n")
                    question_info["In which year did the person [position] in the image start working?"]+=1
                    sc+=14
                    q="In which year did the person [position] in the image start working?"
                    a=yow2
                    qa_gen(q,a)
           except:
               x=1
           try:
            if(yow3!=-1 and yow3!='NOT'):
                if(yow3!=-1 and yow3!='NOT'):
                    qFile.write("In which year did the person in the center in the image start working?\t")
                    qFile.write(yow3)
                    answers_info[yow3]+=1
                    qFile.write("\n")
                    question_info["In which year did the person [position] in the image start working?"]+=1
                    sc+=14
                    q="In which year did the person [position] in the image start working?"
                    a=yow3
                    qa_gen(q,a)
           except:
               x=1



           countryOB=[]
           continentOB=[]
           countryOB.append(getCountyOfBirth(f1))
           countryOB.append(getCountyOfBirth(f2))
           countryOB.append(getCountyOfBirth(f3)) 
           continentOB.append(getContinentOfBirth(f1))
           continentOB.append(getContinentOfBirth(f2))
           continentOB.append(getContinentOfBirth(f3))
           if(countryOB[0] !='NOT-AVAILABLE' and countryOB[1]!= 'NOT-AVAILABLE' and countryOB[2]!='NOT-AVAILABLE'):
              p=random.randint(0,2)
              ques="How many people in this image were born in %s?\t" %(countryOB[p])
              ans = 0
              for i in countryOB:
                if i == countryOB[p]:
                  ans = ans + 1
              qFile.write(ques)
              question_info["How many people in this image were born in [Country]?"]+=1
              qFile.write(str(ans)+'\n')
              answers_info[str(ans)]+=1
              q="How many people in this image were born in [Country]?"
              a=str(ans)
              qa_gen(q,a)
              sc+=10
              ques="Are the people in the image born in the same country?\t"
              if(countryOB[0]==countryOB[1] and countryOB[1]==countryOB[2]):
                ans="Yes"
              else:
                ans="No"
              qFile.write(ques)
              sc+=11
              qFile.write(ans+'\n')   
              answers_info[ans]+=1
              question_info["Are the people in the image born in the same country?"]+=1
              q="Are the people in the image born in the same country?"
              a=ans
              qa_gen(q,a)

           if(continentOB[0]!='NOT-AVAILABLE' and continentOB[1] != 'NOT-AVAILABLE' and continentOB[2]!= 'NOT-AVAILABLE'):
              p=random.randint(0,2)
              ques="How many people in this image were born in %s?\t" %(continentOB[p])
              ans = 0
              for i in continentOB:
                if i == continentOB[p]:
                  ans = ans + 1
              qFile.write(ques)
              sc=sc+10
              qFile.write(str(ans)+'\n')
              answers_info[str(ans)]+=1
              q="How many people in this image were born in [Continent]?"
              a=ans
              qa_gen(q,a)
              question_info["How many people in this image were born in [Continent]?"]+=1
              ques="Are the people in the image born in the same continent?\t"
              if(continentOB[0]==continentOB[1] and continentOB[1]==continentOB[2]):
                ans="Yes"
              else:
                ans="No"
              qFile.write(ques)
              sc=sc+11
              qFile.write(ans+'\n')   
              answers_info[ans]+=1
              question_info["Are the people in the image born in the same continent?"]+=1
              q="Are the people in the image born in the same continent?"
              a=ans
              qa_gen(q,a)

           ##The following questios are related to place of education

           place_of_education1=getPlaceOfEducation(f1)
           place_of_education2=getPlaceOfEducation(f2)
           place_of_education3=getPlaceOfEducation(f3)
           if place_of_education1[0]!='NOT-AVAILABLE' and place_of_education2[0]!='NOT-AVAILABLE' and place_of_education3[0]!='NOT-AVAILABLE':
             place_of_education1[0]=eval(place_of_education1[0])
             place_of_education2[0]=eval(place_of_education2[0])
             place_of_education3[0]=eval(place_of_education3[0])
             total_list_edu_places = []
             for places in place_of_education1[0]:
              total_list_edu_places.append(places)
             for places in place_of_education2[0]:
              total_list_edu_places.append(places)
             for places in place_of_education3[0]:
              total_list_edu_places.append(places)
             total_no_of_edu_places = len(total_list_edu_places)
           	 #print total_list_edu_places
             edu_place = total_list_edu_places[random.randint(0, total_no_of_edu_places-1)]
           	 #print edu_place
             ques=""
             ans=""
             if edu_place in place_of_education1[0] and edu_place not in place_of_education2[0] and edu_place not in place_of_education3[0]:
              ques = 'Who among the people in the image studied at '+edu_place+'?'
              ans = 'Person in the left'
             elif edu_place in place_of_education2[0] and edu_place not in place_of_education1[0] and edu_place not in place_of_education3[0]:
              ques = 'Who among the people in the image studied at '+edu_place+'?'
              ans = 'Person in the center'
             elif edu_place in place_of_education3[0] and edu_place not in place_of_education1[0] and edu_place not in place_of_education2[0]:
              ques = 'Who among the people in the image studied at '+edu_place+'?'
              ans = 'Person in the right'
             if ans!="" and ques!="":
              qFile.write(ques+'\t')
              sc+=11
              qFile.write(str(ans)+'\n')
              answers_info[str(ans)]+=1
              question_info["Who among the people in the image studied at [Education Institute / University]?"]+=1
              q="Who among the people in the image studied at [Education Institute / University]?"
              a=str(ans)
              qa_gen(q,a)
             '''ques='Have people in the image ever been to the same education institute?'
             for edu_place in place_of_education1[0]:
              if edu_place in place_of_education2[0] and edu_place in place_of_education3[0]:
                ans = "Yes\n"
                break
              else:
                ans = "No\n"
             qFile.write(ques+'\t')
             qFile.write(ans)
             sc+=1
             question_info["Have people in the image ever been to the same education institute?"]+=1
           	 ##The Following questions are related to Languages
             '''
           '''
           language1=getLanguage(f1)
           language2=getLanguage(f2)
           language3=getLanguage(f3)
           if language1[0]!='NOT-AVAILABLE' and language2[0]!='NOT-AVAILABLE' and language3[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 total_list_of_languages = []
           	 #print language1[0]
           	 #print language2[0]
           	 if language2[0]!='NOT-AVAILABLE':
           	 	language2[0]=eval(language2[0])
           	 	for l in language2[0]:
           	 		total_list_of_languages.append(l)
           	 if language1[0]!='NOT-AVAILABLE':
           	 	language1[0]=eval(language1[0])
           	 	for l in language1[0]:
           	 		total_list_of_languages.append(l)
           	 if language3[0]!='NOT-AVAILABLE':
           	 	language3[0]=eval(language3[0])
           	 	for l in language3[0]:
           	 		total_list_of_languages.append(l)
           	 if language1[0]=='NOT-AVAILABLE':
           	 	language1[0]=[]
           	 if language2[0]=='NOT-AVAILABLE':
           	 	language2[0]=[]
           	 if language3[0]=='NOT-AVAILABLE':
           	 	language3[0]=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 total_no_of_languages = len(total_list_of_languages)
           	 #print total_list_of_languages
           	 language = total_list_of_languages[random.randint(0, total_no_of_languages-1)]
           	 #print edu_place
           	 ques = 'How many people in the image speak '+language+'?'
           	 ans = 0
           	 if language in language1[0]:
           	 	ans = ans + 1
           	 if language in language2[0]:
           	 	ans = ans + 1
           	 if language in language3[0]:
           	 	ans = ans + 1
           	 qFile.write(ques+'\t')
                 sc+=1
           	 qFile.write(str(ans)+'\n')
                 question_info["How many people in the image speak [Language]?"]+=1
           	 if language1[0]!=[] and language2[0]!=[] and language3!=[0]:
           	 	ques='Do people in the image have a common language?'
	           	 #print language1[0]
	           	 #print language2[0]
	           	for l in language1[0]:
	           	 	if l in language2[0] and l in language3[0]:
	           	 		ans = "Yes\n"
	           	 		break
	           	 	else:
	           	 		ans = "No\n"
	           	qFile.write(ques+'\t')
	           	qFile.write(ans)
                        sc+=1
                        question_info["Do people in the image have a common language?"]+=1
           '''
	           
           
           spouse1=getSpouse(f1)
           spouse2=getSpouse(f2)
           spouse3=getSpouse(f3)
           if spouse1[0]!='NOT-AVAILABLE' or spouse2[0]!='NOT-AVAILABLE' or spouse3[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 total_list_of_spouses = []
           	 #print spouse1[0]
           	 #print spouse2[0]
           	 if spouse2[0]!='NOT-AVAILABLE':
           	 	spouse2[0]=eval(spouse2[0])
           	 	for l in spouse2[0]:
           	 		total_list_of_spouses.append(l)
           	 if spouse1[0]!='NOT-AVAILABLE':
           	 	spouse1[0]=eval(spouse1[0])
           	 	for l in spouse1[0]:
           	 		total_list_of_spouses.append(l)
           	 if spouse3[0]!='NOT-AVAILABLE':
           	 	spouse3[0]=eval(spouse3[0])
           	 	for l in spouse3[0]:
           	 		total_list_of_spouses.append(l)
           	 if spouse1[0]=='NOT-AVAILABLE':
           	 	spouse1[0]=[]
           	 if spouse2[0]=='NOT-AVAILABLE':
           	 	spouse2[0]=[]
           	 if spouse3[0]=='NOT-AVAILABLE':
           	 	spouse3[0]=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 total_no_of_spouses = len(total_list_of_spouses)
           	 #print total_list_of_spouses
           	 spouse = total_list_of_spouses[random.randint(0, total_no_of_spouses-1)]
           	 #print edu_place
           	 ques = 'Who among the people in the image ever married to '+spouse+'?'
           	 ans = 0
           	 if spouse in spouse1[0]:
           	 	ans = "Person in the left"
           	 if spouse in spouse2[0]:
           	 	ans = "Person in the center"
           	 if spouse in spouse3[0]:
           	 	ans = "Person in the right"
           	 qFile.write(ques+'\t')
                 sc+=10
           	 qFile.write(str(ans)+'\n')
                 answers_info[str(ans)]+=1
                 question_info["Who among the people in the image ever married to [Spouse]?"]+=1
                 q="Who among the people in the image ever married to [Spouse]?"
                 a=str(ans)
                 qa_gen(q,a)
           
           
           #The following questions are related to Nick-Name
           nick1=getNickName(f1)
           nick2=getNickName(f2)
           nick3=getNickName(f3)
           if nick1[0]!='NOT-AVAILABLE' or nick2[0]!='NOT-AVAILABLE' or nick3[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 if nick1[0]=='NOT-AVAILABLE':
           	 	nick1=[]
           	 if nick2[0]=='NOT-AVAILABLE':
           	 	nick2=[]
           	 if nick3[0]=='NOT-AVAILABLE':
           	 	nick3=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 total_list_of_nick = []
           	 for n in nick1:
           	 	total_list_of_nick.append(n)
           	 for n in nick2:
           	 	total_list_of_nick.append(n)
           	 for n in nick3:
           	 	total_list_of_nick.append(n)
           	 total_no_of_nick = len(total_list_of_nick)
           	 #print total_list_of_nick
           	 #print total_list_edu_places
           	 nick = total_list_of_nick[random.randint(0, total_no_of_nick-1)]
           	 #print edu_place
           	 ques = 'Who among the people in the image is called by the nickname '+nick+'?'
           	 if nick in nick1:
           	 	ans = 'Person in the left'
           	 elif nick in nick2:
           	 	ans = 'Person in the center'
           	 else:
           	 	ans = 'Person in the right'
           	 qFile.write(ques+'\t')
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 sc+=13
                 question_info["Who among the people in the image is called by the nickname [NickName]?"]+=1
                 q="Who among the people in the image is called by the nickname [NickName]?"
                 a=ans
                 qa_gen(q,a)
  			##The Following questions are related to Political Party
           political_party1=getPoliticalParty(f1)
           political_party2=getPoliticalParty(f2)
           political_party3=getPoliticalParty(f3)
           political_party_founder1 = getPoliticalPartyFounder(f1)
           political_party_founder2 = getPoliticalPartyFounder(f2)
           political_party_founder3 = getPoliticalPartyFounder(f3)
           if political_party1[0]!='NOT-AVAILABLE' and political_party2[0]!='NOT-AVAILABLE' and political_party3[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 if political_party1[0]=='NOT-AVAILABLE':
           	 	political_party1=[]
           	 if political_party2[0]=='NOT-AVAILABLE':
           	 	political_party2=[]
           	 if political_party3[0]=='NOT-AVAILABLE':
           	 	political_party3=[]

           	 total_list_of_political_party = []
           	 for n in political_party1:
           	 	total_list_of_political_party.append(n)
           	 for n in political_party2:
           	 	total_list_of_political_party.append(n)
           	 for n in political_party3:
           	 	total_list_of_political_party.append(n)
           	 total_no_of_political_party = len(total_list_of_political_party)
           	 political_party = total_list_of_political_party[random.randint(0, total_no_of_political_party-1)]
           	 ques = 'How many people in the image belong to '+political_party+'?'
           	 ans = 0
           	 if political_party in political_party1:
           	 	ans = ans + 1
           	 if political_party in political_party2:
           	 	ans = ans + 1
           	 if political_party in political_party3:
           	 	ans = ans + 1
           	 qFile.write(ques+'\t')
                 sc+=9
           	 qFile.write(str(ans)+'\n')
                 answers_info[str(ans)]+=1
                 question_info['How many people in the image belong to [political party]?']+=1
                 q='How many people in the image belong to [political party]?'
                 a=str(ans)
                 qa_gen(q,a)
           	 if political_party1!=[] and political_party2!=[] and political_party3!=[]:
           	 	
	           	 ques='Do people in the image belong to the same political party?'
	           	 #print language1[0]
	           	 #print language2[0]
	           	 for l in political_party1:

	           	 	if l in political_party2 and l in political_party3:
	           	 		ans = "Yes"
	           	 		break
	           	 	else:
	           	 		ans = "No"
	           	 qFile.write(ques+'\t')
	           	 qFile.write(ans+'\n')
                         answers_info[ans]+=1
                         sc+=11
                         question_info["Do people in the image belong to the same political party?"]+=1
                         q="Do people in the image belong to the same political party?"
                         a=ans
                         qa_gen(q,a)

       	   if political_party_founder1!='NOT-AVAILABLE':
       	   	 #print imgId
       	   	 ques = 'Who is the founder of the Political Party person in the left belongs to?\t'
       	   	 ans = political_party_founder1
       	   	 qFile.write(ques)
       	   	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 sc+=14
                 question_info["Who is the founder of the Political Party person [position] belongs to?"]+=1
       	         q="Who is the founder of the Political Party person [position] belongs to?"
                 a=ans
                 qa_gen(q,a)
                 #print political_party_founder

       	   if political_party_founder2!='NOT-AVAILABLE':
       	   	 #print imgId
       	   	 ques = 'Who is the founder of the Political Party person in the center belongs to?\t'
       	   	 ans = political_party_founder2
       	   	 qFile.write(ques)
       	   	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 sc+=14
                 question_info["Who is the founder of the Political Party person [position] belongs to?"]+=1
                 
       	         q="Who is the founder of the Political Party person [position] belongs to?"
                 a=ans
                 qa_gen(q,a)
       	 	 #print political_party_founder2
       	   if political_party_founder3!='NOT-AVAILABLE':
                 ques = 'Who is the founder of the Political Party person in the right belongs to?\t'
                 ans = political_party_founder3
                 qFile.write(ques)
                 qFile.write(ans+'\n')    
                 answers_info[ans]+=1
                 sc+=14
                 question_info["Who is the founder of the Political Party person [position] belongs to?"]+=1
       	         q="Who is the founder of the Political Party person [position] belongs to?"
                 a=ans
                 qa_gen(q,a)

         
           occupation1=getoccupation(f1)
           occupation2=getoccupation(f2)
           occupation3=getoccupation(f3)
           if occupation1[0]!='NOT-AVAILABLE' and occupation2[0]!='NOT-AVAILABLE' and occupation3[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 total_list_of_occupations = []
           	 #print language1[0]
           	 #print language2[0]
           	 occupation1[0]=str(occupation1[0])
           	 #print occupation2[0]
           	 #print occupation3[0]
           	 if occupation2[0]!='NOT-AVAILABLE':
           	 	occupation2[0]=eval(occupation2[0])
           	 	for l in occupation2[0]:
           	 		total_list_of_occupations.append(l)
           	 if occupation1[0]!='NOT-AVAILABLE':
           	 	occupation1[0]=eval(occupation1[0])
           	 	for l in occupation1[0]:
           	 		total_list_of_occupations.append(l)
           	 if occupation3[0]!='NOT-AVAILABLE':
           	 	occupation3[0]=eval(occupation3[0])
           	 	for l in occupation3[0]:
           	 		total_list_of_occupations.append(l)
           	 if occupation1[0]=='NOT-AVAILABLE':
           	 	occupation1[0]=[]
           	 if occupation2[0]=='NOT-AVAILABLE':
           	 	occupation2[0]=[]
           	 if occupation3[0]=='NOT-AVAILABLE':
           	 	occupation3[0]=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 
           	 
           	 total_no_of_occupations = len(total_list_of_occupations)
           	 #print total_list_of_occupations
           	 if total_no_of_occupations<=0:
           	 	continue
           	 occupation = total_list_of_occupations[random.randint(0, total_no_of_occupations-1)]
           	 #print edu_place
           	 ques = 'How many is/are '+occupation+' among the people in the image?'
           	 ans = 0
           	 if occupation in occupation1[0]:
           	 	ans = ans + 1
           	 if occupation in occupation2[0]:
           	 	ans = ans + 1
           	 if occupation in occupation3[0]:
           	 	ans = ans + 1
           	 qFile.write(ques+'\t')
           	 qFile.write(str(ans)+'\n')
                 answers_info[str(ans)]+=1
                 sc+=10
                 question_info["How many is/are [Occupation] among the people in the image?"]+=1
                 q="How many is/are [Occupation] among the people in the image?"
                 a=str(ans)
                 qa_gen(q,a)
           	 if occupation1[0]!=[] and occupation2[0]!=[] and occupation3[0]!=[]:
           	 	
	           	 ques='Do people in the image have a common occupation?'
	           	 #print occupation1[0]
	           	 #print occupation2[0]
	           	 for l in occupation1[0]:

	           	 	if l in occupation2[0] and l in occupation3[0]:
	           	 		ans = "Yes"
	           	 		break
	           	 	else:
	           	 		ans = "No"
	           	 qFile.write(ques+'\t')
	           	 qFile.write(ans+'\n')
                         answers_info[ans]+=1
                         sc+=9
                         question_info["Do people in the image have a common occupation?"]+=1
                         q="Do people in the image have a common occupation?"
                         a=ans
                         qa_gen(q,a)
	         continue

print sc

import json

with open('3-face_analysis/qa.json', 'w') as fp:
    json.dump(qa, fp)
#print(temp_dict)
#normalizeplot()
#plotdetails()
#print(len(labels))
#print(labels)
#print(fracs)
#the_grid = GridSpec(1, 1)
#plt.subplot(the_grid[0, 0], aspect=1)
#plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
#plt.show()
#plt.savefig('3-face_plots/20.png', bbox_inches='tight')


'''el = open('entity_list.csv', 'r')
el2 = open('entity_list2.csv', 'w')
total_entities=[]
for line in el.readlines():
#    print line
    line = line[:-1]
#    print line
    total_entities.append(line)

for i in labels:
    if i not in total_entities:
        total_entities.append(i)

for i in total_entities:
    #print i
    el2.write(i+'\n')
#    x=1
'''

for i in entity_file_present:
    a3.write(i+'\n')
for i in entity_file_absent:
    try:
        a4.write(i+'\n')
    except:
        continue
for key in file_info:
    a1.write(key+'\t'+str(file_info[key])+'\n')
total=0
for key in question_info:
    total+=question_info[key]
    a2.write(key+'\t'+str(question_info[key])+'\n')

a2.write("Total Questions\t"+str(total)+'\n')
a2.write("Average Question Length\t"+ str(float(sc)/float(total))+'\n')

total2=0
no_of_words=0
for key in answers_info:
    total2+=answers_info[key]
    a11.write(key+'\t'+str(answers_info[key])+'\n')
    no_of_words= no_of_words + (answers_info[key]*len(key.split(' ')))

a11.write("Total unique Answers\t"+str(len(answers_info))+'\n')
a11.write("Average Answers Length\t"+ str(float(no_of_words)/float(total2))+'\n')


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


