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

csvFile = '../../wikiAttributesExtr/twoFaceAnnotationPartA-1.0.csv'
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



a1=open('2-face_analysis/files_info.csv', 'w')
a2=open('2-face_analysis/questions_count.csv', 'w')
a3=open('2-face_analysis/entities_files_present.csv', 'w')
a4=open('2-face_analysis/entities_files_absent.csv', 'w')
a8=open('2-face_analysis/partially_annotated_file_info.csv', 'w')
a6=open('2-face_analysis/completely_annotated_file_info', 'w')
a7=open('2-face_analysis/complete_analysis.csv', 'w')
a5=open('2-face_analysis/ambiguous_file.csv', 'w')
a9=open('2-face_analysis/our_ambiguous_file.csv', 'w')
a10=open('2-face_analysis/same_name.csv', 'w')
a11=open('2-face_analysis/answers_count.csv', 'w')

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

dup1=open('../datasets/2-face_dup2.csv', 'r')
dups=[]
for line in dup1.readlines():
    line=line[:-1]
    dups.append(line)


with open(csvFile, 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for token in spamreader:
         actualperson1=""
         actualperson2=""
         imgId=token[0]
         if imgId in unique_images:
             continue
         if imgId in dups:
             continue
         unique_images.append(imgId)
         if(token[3]=="NOT SURE" or token[4] == "ONE"):# for twofacefile
           file_info['Ambiguous']+=1
           img_path=get_image_path(imgId)
           a5.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\n')
        # if(token[4]=="NOT SURE" or token[5] == "ONE"):
         #if(token[5]=="NOT SURE" or token[6]=="ONE"):
           continue
         #if (token[7]!="TWO"):
         #    continue
         y1=-1
         y2=-1
         person1=(token[1].lstrip()).rstrip()
         person2=(token[2].lstrip()).rstrip()
         if(person1=="" and person2==""):
             file_info['Not Annotated']+=1
             img_path=get_image_path(imgId)
             a8.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\t'+token[4]+'\n')
             continue

         if(person1=="" or person2==""):
           file_info['Ambiguous']+=1
           img_path=get_image_path(imgId)
           a5.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\n')
           continue

         person1=person1.replace(" ","_")
         person2=person2.replace(" ","_")
         if person1 in person_not_found:
             print person1
             actualperson1=final_actual_names[person1]
             person1=final_correct_names[person1]
             print person1
         if person2 in person_not_found:
             print person2
             actualperson2=final_actual_names[person2]
             person2=final_correct_names[person2]
             print person2

         f1="../../wikiAttributesExtr/%s.csv" %(person1)
         
         f2="../../wikiAttributesExtr/%s.csv" %(person2)
         flag1=checkAvail(f1)
         flag2=checkAvail(f2)

         if flag1!=1 or person1 in person_data_missing:
             if person1 not in entity_file_absent:
                 entity_file_absent.append(person1)

         if flag2!=1 or person2 in person_data_missing:
             if person2 not in entity_file_absent:
                 entity_file_absent.append(person2)
         
         if person1 in person_data_missing:
            flag1=0;
         if person2 in person_data_missing:
            flag2=0;



         if(flag1*flag2!=1):
           file_info['Ambiguous_our']+=1
           img_path=get_image_path(imgId)
           a9.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\n')
         if(flag1*flag2==1):
           if actualperson1!="":
               person1=actualperson1.replace("_"," ")
           else:
               person1=person1.replace("_"," ")
           if actualperson2!="":
               person2=actualperson2.replace("_"," ")
           else:
               person2=person2.replace("_"," ")
           if person1.upper()==person2.upper():
               file_info['same_name']+=1
               img_path=get_image_path(imgId)
               a10.write(str(imgId)+'\t'+img_path+'\t'+token[1]+'\t'+token[2]+'\n')
               continue
           print imgId
           if person1 not in entity_file_present:
               entity_file_present.append(person1)

           if person2 not in entity_file_present:
               entity_file_present.append(person2)
           file_info['Annotated']+=1
           img_path=get_image_path(imgId)
           a6.write(str(imgId)+'\t'+img_path+'\t'+person1+'\t'+person2+'\n')
           qFileName='QA_temp2/%s-QA.csv' %(imgId)
           qFile=open(qFileName,'w+')

           qFile.write("Who is in the left?\t")
           question_info["Who is in the [position]?"]+=1
           ques="Who is in the [position]?"
           qFile.write(person1)
           ans=person1
           answers_info[person1]+=1
           if ques not in qa:
               qa[ques]={}
               qa[ques] = defaultdict(lambda: 0, qa[ques])
           else:
               qa[ques][ans]+=1
           qFile.write("\n")
             
           qFile.write("Who is in the right?\t")
           question_info["Who is in the [position]?"]+=1
           ques="Who is in the [position]?"
           qFile.write(person2)
           ans = person2
           answers_info[person2]+=1
           if ques not in qa:
               qa[ques]={}
               qa[ques] = defaultdict(lambda: 0, qa[ques])
           else:
               qa[ques][ans]+=1
           qFile.write("\n")

           ques="Who is to the right of %s?\t" %(person1)
           question_info["Who is to the [position] of [person]?"]+=1
           qFile.write(ques)
           qFile.write(person2)
           ques="Who is to the [position] of [person]?"
           ans=person2
           answers_info[person2]+=1
           if ques not in qa:
               qa[ques]={}
               qa[ques] = defaultdict(lambda: 0, qa[ques])
           else:
               qa[ques][ans]+=1
           qFile.write("\n")

           ques="Who is to the left of %s?\t" %(person2)
           question_info["Who is to the [position] of [person]?"]+=1
           qFile.write(ques)
           qFile.write(person1)
           answers_info[person1]+=1
           ques="Who is to the [position] of [person]?"
           ans=person1
           if ques not in qa:
               qa[ques]={}
               qa[ques] = defaultdict(lambda: 0, qa[ques])
           else:
               qa[ques][ans]+=1
           qFile.write("\n")
           yob1,mob1,dob1=getYOB(f1)
           yob2,mob2,dob2=getYOB(f2)
           yod1,mod1,dod1=getYOD(f1)
           yod2,mod2,dod2=getYOD(f2)
           if(yob1!=-1 and yob2 != -1 and yob1!='NOT' and yob2!='NOT'):
             if yob1!=yob2:
               qFile.write("Who among the people in the image is the eldest?\t")  
               question_info["Who among the people in the image is the eldest?"]+=1
               ques="Who among the people in the image is the eldest?"
               if(yob1 > yob2):
                 qFile.write('Person in the right')
                 answers_info['Person in the right']+=1
                 ans = 'Person in the right'
               else:
                 qFile.write('Person in the left')
                 answers_info['Person in the left']+=1
                 ans = 'Person in the left'
               if ques not in qa:
                 qa[ques]={}
                 qa[ques] = defaultdict(lambda: 0, qa[ques])
               else:
                qa[ques][ans]+=1
               qFile.write("\n")    
             try:
               ques="What is the age gap between these two people in image?"
               ans=abs(int(yob1)-int(yob2))
               qFile.write(ques+'\t')  
               question_info["What is the age gap between [person1] and [person2]?"]+=1
               qFile.write(str(ans)+' years')    
               answers_info[str(ans)]+=1
               ques="What is the age gap between [person1] and [person2]?"
               if ques not in qa:
                qa[ques]={}
                qa[ques] = defaultdict(lambda: 0, qa[ques])
               else:
                qa[ques][ans]+=1
               qFile.write("\n")

             except:
               continue
             if(yod1!=-1 and yod2 != -1 and yod1!='NOT' and yod2!='NOT'):
             	qFile.write("Who among the people in the image lived longer?\t") 
                question_info["Who among the people in the image lived longer?"]+=1
                ques="Who among the people in the image lived longer?"
             	delta_mon1 = (int(yod1)*12 + int(mod1) - 1) - (int(yob1)*12 + int(mob1) - 1)
             	delta_mon2 = (int(yod2)*12 + int(mod2) - 1) - (int(yob2)*12 + int(mob2) - 1)
             	if(delta_mon1>delta_mon2):
             		qFile.write('Person in the left')
                        answers_info['Person in the left']+=1
                        ans='Person in the left'
             	else:
             		qFile.write('Person in the right')
                        answers_info['Person in the right']+=1
                        ans='Person in the right'
                if ques not in qa:
                        qa[ques]={}
                        qa[ques] = defaultdict(lambda: 0, qa[ques])
                else:
                        qa[ques][ans]+=1
             	qFile.write("\n")
             try:
                 if(yob1!=-1 and yob2!=-1 and yob2!='NO' and yob1!='NO'):
                     ques='Who among the people in the image were born after the end of World War II?'
                     if int(yob1)>1945 and int(yob2)> 1945:
                         ans = 'Both'
                     elif int(yob1)>1945:
                         ans = 'Person in the left'
                     elif int(yob2)>1945:
                         ans = 'Person in the right'
                     else:
                         ans = 'None'
                     qFile.write(ques+'\t')
                     question_info["Who among the people in the image were born after the end of World War II?"]+=1
                     qFile.write(ans+'\n')
                     ques="Who among the people in the image were born after the end of World War II?"
                     if ques not in qa:
                        qa["Who among the people in the image were born after the end of World War II?"]={}
                        qa[ques] = defaultdict(lambda: 0, qa[ques])
                     else:
                        qa["Who among the people in the image were born after the end of World War II?"][ans]+=1
                     answers_info[ans]+=1
             except:
                 x=1

           yow1=getYOW(f1)
           yow2=getYOW(f2)
           try:
            if(yow1!=-1 and yow1!='NOT'):
                if(yow1!=-1 and yow1!='NOT'):
                    qFile.write("In which year did the person on the left in the image start working?\t")
                    qFile.write(yow1)
                    ques="In which year did the person [position] in the image start working?"
                    ans=yow1
                    if ques not in qa:
                        qa[ques]={}
                        qa[ques] = defaultdict(lambda: 0, qa[ques])
                    else:
                        qa[ques][ans]+=1
                    answers_info[yow1]+=1
                    qFile.write("\n")
                    question_info["In which year did the person [position] in the image start working?"]+=1
           except:
               x=1
           try:
            if(yow2!=-1 and yow2!='NOT'):
                if(yow2!=-1 and yow2!='NOT'):
                    qFile.write("In which year did the person on the right in the image start working?\t")
                    qFile.write(yow2)
                    ques="In which year did the person [position] in the image start working?"
                    ans=yow2
                    if ques not in qa:
                        qa[ques]={}
                        qa[ques] = defaultdict(lambda: 0, qa[ques])
                    else:
                        qa[ques][ans]+=1
                    qFile.write("\n")
                    answers_info[yow2]+=1
                    question_info["In which year did the person [position] in the image start working?"]+=1
           except:
               x=1



           countryOB1=getCountyOfBirth(f1)
           countryOB2=getCountyOfBirth(f2)
           continentOB1=getContinentOfBirth(f1)
           continentOB2=getContinentOfBirth(f2)
           if(countryOB1 !='NOT-AVAILABLE' and countryOB2 != 'NOT-AVAILABLE'):
              p=random.randint(0,9)
              if(p<5):
                ques="How many people in this image were born in %s?\t" %(countryOB1)
              else:  
                ques="How many people in this image were born in %s?\t" %(countryOB2)
              if(countryOB1==countryOB2):
                ans="2"
              else:   
                ans="1"
              qFile.write(ques)
              ques="How many people in this image were born in [Country]?"
              if ques not in qa:
                qa["How many people in this image were born in [Country]?"]={}
                qa["How many people in this image were born in [Country]?"] = defaultdict(lambda: 0, qa["How many people in this image were born in [Country]?"])
              else:
                qa["How many people in this image were born in [Country]?"][ans]+=1
              question_info["How many people in this image were born in [Country]?"]+=1
              qFile.write(ans+'\n')
              answers_info[ans]+=1
            	

              ques="Are the people in the image born in the same country?\t"
              if(countryOB1==countryOB2):
                ans="Yes"
              else:
                ans="No"
              qFile.write(ques)
              question_info["Are the people in the image born in the same country?"]+=1
              ques="Are the people in the image born in the same country?"
              if ques not in qa:
                qa["Are the people in the image born in the same country?"]={}
                qa["Are the people in the image born in the same country?"] = defaultdict(lambda: 0, qa["Are the people in the image born in the same country?"])
              else:
                qa["Are the people in the image born in the same country?"][ans]+=1
              qFile.write(ans+'\n')
              answers_info[ans]+=1


           if(continentOB1!='NOT-AVAILABLE' and continentOB2 != 'NOT-AVAILABLE'):
              p=random.randint(0,9)
              if(p<5):
                ques="How many people in this image were born in %s?\t" %(continentOB1)
              else:  
                ques="How many people in this image were born in %s?\t" %(continentOB2)
              if(continentOB1==continentOB2):
                ans="2"
              else:   
                ans="1"
              qFile.write(ques)
              question_info["How many people in this image were born in [Continent]?"]+=1
              ques="How many people in this image were born in [Continent]?"
              if ques not in qa:
                qa["How many people in this image were born in [Continent]?"]={}
                qa["How many people in this image were born in [Continent]?"] = defaultdict(lambda: 0, qa["How many people in this image were born in [Continent]?"])
              else:
                qa["How many people in this image were born in [Continent]?"][ans]+=1
              qFile.write(ans+'\n')
              answers_info[ans]+=1
        
              ques="Are the people in the image born in the same continent?\t"
              if(continentOB1==continentOB2):
                  ans="Yes"
              else:
                  ans="No"
              qFile.write(ques)
              ques="Are the people in the image born in the same continent?"
              if ques not in qa:
                qa["Are the people in the image born in the same continent?"]={}
                qa["Are the people in the image born in the same continent?"] = defaultdict(lambda: 0, qa["Are the people in the image born in the same continent?"])
              else:
                qa["Are the people in the image born in the same continent?"][ans]+=1
              question_info["Are the people in the image born in the same continent?"]+=1
              qFile.write(ans+'\n')
              answers_info[ans]+=1

           ##The following questios are related to place of education

           place_of_education1=getPlaceOfEducation(f1)
           place_of_education2=getPlaceOfEducation(f2)
           if place_of_education1[0]!='NOT-AVAILABLE' and place_of_education2[0]!='NOT-AVAILABLE':

           	 place_of_education1[0]=eval(place_of_education1[0])
           	 place_of_education2[0]=eval(place_of_education2[0])

           	 total_list_edu_places = []
           	 for places in place_of_education1[0]:
           	 	total_list_edu_places.append(places)
           	 for places in place_of_education2[0]:
           	 	total_list_edu_places.append(places)
           	 total_no_of_edu_places = len(total_list_edu_places)
           	 #print total_list_edu_places
           	 edu_place = total_list_edu_places[random.randint(0, total_no_of_edu_places-1)]
           	 #print edu_place
           	 ques = 'Who among the people in the image studied at '+edu_place+'?'
           	 if edu_place in place_of_education1[0] and edu_place in place_of_education2[0]:
           	 	ans = 'Both'
           	 elif edu_place in place_of_education1[0]:
           	 	ans = 'Person in the left'
           	 else:
           	 	ans = 'Person in the right'
           	 qFile.write(ques+'\t')
                 question_info["Who among the people in the image studied at [Education Institute / University]?"]+=1
                 ques="Who among the people in the image studied at [Education Institute / University]?"
                 if ques not in qa:
                    qa["Who among the people in the image studied at [Education Institute / University]?"]={}
                    qa["Who among the people in the image studied at [Education Institute / University]?"] = defaultdict(lambda: 0, qa["Who among the people in the image studied at [Education Institute / University]?"])
                 else:
                    qa["Who among the people in the image studied at [Education Institute / University]?"][ans]+=1
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1
                 '''
           	 ques='Have people in the image ever been to the same education institute?'

           	 for edu_place in place_of_education1[0]:
           	 	if edu_place in place_of_education2[0]:
           	 		ans = "Yes"
           	 		break
           	 	else:
           	 		ans = "No"
           	 qFile.write(ques+'\t')
                 question_info["Have people in the image ever been to the same education institute?"]+=1
           	 qFile.write(ans+'\n')
                 '''
           	 ##The Following questions are related to Languages
           '''
           language1=getLanguage(f1)
           language2=getLanguage(f2)
           if language1[0]!='NOT-AVAILABLE' and language2[0]!='NOT-AVAILABLE':
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
           	 if language1[0]=='NOT-AVAILABLE':
           	 	language1[0]=[]
           	 if language2[0]=='NOT-AVAILABLE':
           	 	language2[0]=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 
           	 
           	 total_no_of_languages = len(total_list_of_languages)
           	 #print total_list_of_languages
           	 language = total_list_of_languages[random.randint(0, total_no_of_languages-1)]
           	 #print edu_place
           	 ques = 'How many people in the image speak '+language+'?'
           	 if language in language1[0] and language in language2[0]:
           	 	ans = '2'
           	 elif language in language1[0]:
           	 	ans = '1'
           	 else:
           	 	ans = '1'
           	 qFile.write(ques+'\t')
                 question_info["How many people in the image speak [Language]?"]+=1
           	 qFile.write(ans+'\n')

           	 if language1[0]!=[] and language2[0]!=[]:
           	 	
	           	 ques='Do people in the image have a common language?'
	           	 #print language1[0]
	           	 #print language2[0]
	           	 for l in language1[0]:

	           	 	if l in language2[0]:
	           	 		ans = "Yes"
	           	 		break
	           	 	else:
	           	 		ans = "No"
	           	 qFile.write(ques+'\t')
                         question_info["Do people in the image have a common language?"]+=1
	           	 qFile.write(ans+'\n')
'''
           #The following questions are related to Nick-Name

           spouse1=getSpouse(f1)
           spouse2=getSpouse(f2)
           if spouse1[0]!='NOT-AVAILABLE' or spouse2[0]!='NOT-AVAILABLE':
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
           	 if spouse1[0]=='NOT-AVAILABLE':
           	 	spouse1[0]=[]
           	 if spouse2[0]=='NOT-AVAILABLE':
           	 	spouse2[0]=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 
           	 
           	 total_no_of_spouses = len(total_list_of_spouses)
           	 #print total_list_of_spouses
           	 spouse = total_list_of_spouses[random.randint(0, total_no_of_spouses-1)]
           	 #print edu_place
           	 ques = 'Who among the people in the image ever married to '+spouse+'?'
           	 if spouse in spouse1[0]:
           	 	ans = 'Person in the left'
           	 else:
           	 	ans = 'Person in the right'
           	 qFile.write(ques+'\t')
                 question_info["Who among the people in the image ever married to [Spouse]?"]+=1
                 ques="Who among the people in the image ever married to [Spouse]?"
                 if ques not in qa:
                    qa["Who among the people in the image ever married to [Spouse]?"]={}
                    qa["Who among the people in the image ever married to [Spouse]?"] = defaultdict(lambda: 0, qa["Who among the people in the image ever married to [Spouse]?"])
                 else:
                    qa["Who among the people in the image ever married to [Spouse]?"][ans]+=1
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1


           nick1=getNickName(f1)
           nick2=getNickName(f2)
           if nick1[0]!='NOT-AVAILABLE' or nick2[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 if nick1[0]=='NOT-AVAILABLE':
           	 	nick1=[]
           	 if nick2[0]=='NOT-AVAILABLE':
           	 	nick2=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 total_list_of_nick = []
           	 for n in nick1:
           	 	total_list_of_nick.append(n)
           	 for n in nick2:
           	 	total_list_of_nick.append(n)
           	 total_no_of_nick = len(total_list_of_nick)
           	 #print total_list_of_nick
           	 #print total_list_edu_places
           	 nick = total_list_of_nick[random.randint(0, total_no_of_nick-1)]
           	 #print edu_place
           	 ques = 'Who among the people in the image is called by the nickname '+nick+'?'
           	 if nick in nick1:
           	 	ans = 'Person in the left'
           	 else:
           	 	ans = 'Person in the right'
           	 qFile.write(ques+'\t')
                 ques="Who among the people in the image is called by the nickname [NickName]?"
                 if ques not in qa:
                    qa["Who among the people in the image is called by the nickname [NickName]?"]={}
                    qa["Who among the people in the image is called by the nickname [NickName]?"] = defaultdict(lambda: 0, qa["Who among the people in the image is called by the nickname [NickName]?"])
                 else:
                    qa["Who among the people in the image is called by the nickname [NickName]?"][ans]+=1
                 question_info["Who among the people in the image is called by the nickname [NickName]?"]+=1
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1

  
  			##The Following questions are related to Political Party
           
           political_party1=getPoliticalParty(f1)
           political_party2=getPoliticalParty(f2)
           political_party_founder1 = getPoliticalPartyFounder(f1)
           political_party_founder2 = getPoliticalPartyFounder(f2)
           if political_party1[0]!='NOT-AVAILABLE' and political_party2[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 if political_party1[0]=='NOT-AVAILABLE':
           	 	political_party1=[]
           	 	
           	 elif political_party2[0]=='NOT-AVAILABLE':
           	 	political_party2=[]
           	 	political_party_founder = getPoliticalPartyFounder(f2)
           	 


           	 total_list_of_political_party = []
           	 for n in political_party1:
           	 	total_list_of_political_party.append(n)
           	 for n in political_party2:
           	 	total_list_of_political_party.append(n)
           	 total_no_of_political_party = len(total_list_of_political_party)
           	 #print total_list_of_political_party
           	 #print total_list_edu_places
           	 political_party = total_list_of_political_party[random.randint(0, total_no_of_political_party-1)]
           	 #print edu_place
           	 ques = 'How many people in the image belong to '+political_party+'?'
           	 ans = 0
           	 if political_party in political_party1:
           	 	ans = ans + 1
           	 if political_party in political_party2:
           	 	ans = ans + 1

           	 qFile.write(ques+'\t')
                 ques="How many people in the image belong to [political party]?"
                 if ques not in qa:
                    qa["How many people in the image belong to [political party]?"]={}
                    qa["How many people in the image belong to [political party]?"] = defaultdict(lambda: 0, qa["How many people in the image belong to [political party]?"])
                 else:
                    qa["How many people in the image belong to [political party]?"][ans]+=1
                 question_info["How many people in the image belong to [political party]?"]+=1
           	 qFile.write(str(ans)+'\n')
                 answers_info[str(ans)]+=1
           	 if political_party1!=[] and political_party2!=[]:
           	 	
	           	 ques='Do people in the image belong to the same political party?'
	           	 #print language1[0]
	           	 #print language2[0]
	           	 for l in political_party1:

	           	 	if l in political_party2:
	           	 		ans = "Yes"
	           	 		break
	           	 	else:
	           	 		ans = "No"
	           	 qFile.write(ques+'\t')
                         question_info["Do people in the image belong to the same political party?"]+=1
                         ques="Do people in the image belong to the same political party?"
                         if ques not in qa:
                            qa["Do people in the image belong to the same political party?"]={}
                            qa["Do people in the image belong to the same political party?"] = defaultdict(lambda: 0, qa["Do people in the image belong to the same political party?"])
                         else:
                            qa["Do people in the image belong to the same political party?"][ans]+=1
	           	 qFile.write(ans+'\n')
                         answers_info[ans]+=1

       	   if political_party_founder1!='NOT-AVAILABLE':
       	   	 #print imgId
       	   	 ques = 'Who is the founder of the Political Party person in the left belongs to?\t'
       	   	 ans = political_party_founder1
       	   	 qFile.write(ques)
                 question_info["Who is the founder of the Political Party person [position] belongs to?"]+=1
                 ques="Who is the founder of the Political Party person [position] belongs to?"
                 if ques not in qa:
                    qa["Who is the founder of the Political Party person [position] belongs to?"]={}
                    qa["Who is the founder of the Political Party person [position] belongs to?"] = defaultdict(lambda: 0, qa["Who is the founder of the Political Party person [position] belongs to?"])
                 else:
                    qa["Who is the founder of the Political Party person [position] belongs to?"][ans]+=1
       	   	 qFile.write(ans+'\n')
                 answers_info[ans]+=1

       	 	 #print political_party_founder

       	   if political_party_founder2!='NOT-AVAILABLE':
       	   	 #print imgId
       	   	 ques = 'Who is the founder of the Political Party person in the right belongs to?\t'
       	   	 ans = political_party_founder2
       	   	 qFile.write(ques)
                 question_info["Who is the founder of the Political Party person [position] belongs to?"]+=1
       	   	 qFile.write(ans+'\n')
                 ques="Who is the founder of the Political Party person [position] belongs to?"
                 if ques not in qa:
                    qa["Who is the founder of the Political Party person [position] belongs to?"]={}
                    qa["Who is the founder of the Political Party person [position] belongs to?"] = defaultdict(lambda: 0, qa["Who is the founder of the Political Party person [position] belongs to?"])
                 else:
                    qa["Who is the founder of the Political Party person [position] belongs to?"][ans]+=1
                 answers_info[ans]+=1

       	 	 #print political_party_founder2
       	 	 
           #print("**************")

           occupation1=getoccupation(f1)
           occupation2=getoccupation(f2)
           if occupation1[0]!='NOT-AVAILABLE' and occupation2[0]!='NOT-AVAILABLE':
           	 #print imgId
           	 total_list_of_occupations = []
           	 #print language1[0]
           	 #print language2[0]
           	 if occupation2[0]!='NOT-AVAILABLE':
           	 	occupation2[0]=eval(occupation2[0])
           	 	for l in occupation2[0]:
           	 		total_list_of_occupations.append(l)
           	 if occupation1[0]!='NOT-AVAILABLE':
           	 	occupation1[0]=eval(occupation1[0])
           	 	for l in occupation1[0]:
           	 		total_list_of_occupations.append(l)
           	 if occupation1[0]=='NOT-AVAILABLE':
           	 	occupation1[0]=[]
           	 if occupation2[0]=='NOT-AVAILABLE':
           	 	occupation2[0]=[]
           	 #print place_of_education2[0]
           	 #print place_of_education1[0]
           	 #print '########'
           	 
           	 
           	 total_no_of_occupations = len(total_list_of_occupations)
           	 #print total_list_of_occupations
           	 if total_no_of_occupations<=0:
           	 	continue
           	 occupation = total_list_of_occupations[random.randint(0, total_no_of_occupations-1)]
           	 #print edu_place
           	 ques = 'Who is/are '+occupation+' among the people in the image?'
           	 if occupation in occupation1[0] and occupation in occupation2[0]:
           	 	ans = 'Both'
           	 elif occupation in occupation1[0]:
           	 	ans = 'Person in the left'
           	 else:
           	 	ans = 'Person in the right'
           	 qFile.write(ques+'\t')
                 ques="Who is/are [Occupation] among the people in the image?"
                 if ques not in qa:
                    qa["Who is/are [Occupation] among the people in the image?"]={}
                    qa["Who is/are [Occupation] among the people in the image?"] = defaultdict(lambda: 0, qa["Who is/are [Occupation] among the people in the image?"])
                 else:
                    qa["Who is/are [Occupation] among the people in the image?"][ans]+=1
                 question_info["Who is/are [Occupation] among the people in the image?"]+=1
           	 qFile.write(ans+'\n')
                 answers_info[ans]+=1

           	 if occupation1[0]!=[] and occupation2[0]!=[]:
           	 	
	           	 ques='Do people in the image have a common occupation?'
	           	 #print occupation1[0]
	           	 #print occupation2[0]
	           	 for l in occupation1[0]:

	           	 	if l in occupation2[0]:
	           	 		ans = "Yes"
	           	 		break
	           	 	else:
	           	 		ans = "No"
	           	 qFile.write(ques+'\t')
	           	 qFile.write(ans+'\n')
                         ques="Do people in the image have a common occupation?"
                         answers_info[ans]+=1
                         if ques not in qa:
                            qa["Do people in the image have a common occupation?"]={}
                            qa["Do people in the image have a common occupation?"] = defaultdict(lambda: 0, qa["Do people in the image have a common occupation?"])
                         else:
                            qa["Do people in the image have a common occupation?"][ans]+=1
                         question_info["Do people in the image have a common occupation?"]+=1
                 continue

import json

with open('2-face_analysis/qa.json', 'w') as fp:
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
#plt.savefig('2-face_plots/20.png', bbox_inches='tight')

'''el = open('entity_list.csv', 'r')
el2 = open('entity_list2.csv', 'w')
total_entities=[]
for line in el.readlines():
    line = line[:-1]
    total_entities.append(line)
#print total_entities
for i in labels:
    if i not in total_entities:
        total_entities.append(i)


for i in total_entities:
    #print i
    el2.write(i+'\n')
    x=1
'''
no_of_words=0
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
    no_of_words= no_of_words + (question_info[key]*len(key.split(' ')))

a2.write("Total Questions\t"+str(total)+'\n')
a2.write("Average Question Length\t"+ str(float(no_of_words)/float(total))+'\n')


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

