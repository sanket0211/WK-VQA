import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

import time
import json
import random

import os
import re
import csv
import codecs
import numpy as np
import pandas as pd
import nltk
import collections

#from __future__ import division, print_function
from gensim.models import Word2Vec
from keras.models import model_from_json

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from string import punctuation
from sklearn.cross_validation import train_test_split

from keras.utils import plot_model
from gensim.models import KeyedVectors
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, Bidirectional
from keras.layers.merge import concatenate
from keras.layers import add
from keras.layers import *
from keras.layers.merge import concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Sequential

import sys
reload(sys)
sys.setdefaultencoding('utf-8')





def data_spatial(filename,answer):
    f=open(filename,'r')
    f2=open('spatial_data.csv', 'a+')
    for l in f.readlines():
        l=l[:-1]
        l=l.split('\t')
        l2=l[:-2]
        l2.append(l[-1])
        for i in l2:
            f2.write(i+'\t')
        f2.write('\n')

def get_x_y(image_id):
    f=open('phase1AnnCloseList.csv','r')
    cnt=1
    print "inside func"
    print image_id
    for line in f.readlines():
        print cnt
        line=line[:-1]
        line=line.split('\t')
        if image_id==str(cnt):
            print "inside if"
            print line[6]
            f=0
            x_c=[]
            for c in line[6]:
                if c==']':
                    f=0
                    print cords
                    time.sleep(5)
                    cords=cords.split(',')
                    x_c.append(cords[0])
                if f==1:
                    cords+=c
                if c=='[':
                    cords=""
                    f=1
            print x_c
            return x_c
        cnt+=1


def create_image_info_file():
    ent_image=open('image_entity.json', 'r')
    data=json.load(ent_image)
    f=open('training.csv','w')
    f2=open('train_data.csv', 'r')
    for line in f2.readlines():
        line=line[:-1]
        ppl = data[line]
        if len(ppl)==2:
            ppl=[]
            ppl=[str(random.randint(1,10)),str(random.randint(11,20))]
            f.write(line+'\t'+ppl[0]+'\t'+'0'+'\t'+'0'+'\t'+'0'+'\t'+ppl[1]+'\n')
        if len(ppl)==3:
            ppl=[]
            ppl=[str(random.randint(1,10)),str(random.randint(11,20)), str(random.randint(20,30))]
            f.write(line+'\t'+ppl[0]+'\t'+'0'+'\t'+ppl[1]+'\t'+'0'+'\t'+ppl[2]+'\n')
        if len(ppl)==4:
            ppl=[]
            ppl=[str(random.randint(1,10)),str(random.randint(11,20)), str(random.randint(20,30)),str(random.randint(30,40))]
            f.write(line+'\t'+ppl[0]+'\t'+ppl[1]+'\t'+'0'+'\t'+ppl[2]+'\t'+ppl[3]+'\n')
        if len(ppl)==5:
            ppl=[]
            ppl=[str(random.randint(1,10)),str(random.randint(11,20)), str(random.randint(20,30)),str(random.randint(30,40)), str(random.randint(40,50))]
            f.write(line+'\t'+ppl[0]+'\t'+ppl[1]+'\t'+ppl[2]+'\t'+ppl[3]+'\t'+ppl[4]+'\n')

def create_image_ques_file():
    com_data=open('complete_data.json','r')
    data=json.load(com_data)
    img_ent=open('image_entity.json', 'r')
    img_ent_data=json.load(img_ent)
    uni_ans={}
    uni_ques={}
    f=open('answer_id.csv', 'w')
    f2=open('question_id.csv', 'w')
    f3=open('train_data.csv', 'r')
    f4=open('image_ques_ans_id.csv','w')
    questions=[]
    answers=[]
    question_id={}
    answer_id={}
    ans_ch='A'
    ques_ch='Q'
    question_cnt=1
    ans_cnt=1
    for line in f3.readlines():
        line=line[:-1]
        ppl=img_ent_data[line]
        no_of_faces=len(ppl)
        ppl_str=""
        cord_str=""
        cord=[]
        ext=0
        for i in ppl:
            cord.append(random.randint(1,10)+ext)
            ext+=10
        while len(ppl)<5:
            ppl.append('NONE')
        while len(cord)<5:
            cord.append('dss')
        for i in ppl:
            ppl_str=ppl_str + i + '\t'
        for i in cord:
            cord_str=cord_str + str(i) + '\t'
        if line in data["1-face"]:
            questions=data["1-face"][line]['questions']
            answers=data["1-face"][line]['answers']
        elif line in data["2-face"]:
            questions=data["2-face"][line]['questions']
            answers=data["2-face"][line]['answers']
        elif line in data["3-face"]:
            questions=data["3-face"][line]['questions']
            answers=data["3-face"][line]['answers']
        elif line in data["4-face"]:
            questions=data["4-face"][line]['questions']
            answers=data["4-face"][line]['answers']
        elif line in data["5-face"]:
            questions=data["5-face"][line]['questions']
            answers=data["5-face"][line]['answers']
        print questions
        print answers
        for i in questions:
            if i not in question_id:
                question_id[i]=ques_ch+str(question_cnt)
                question_cnt+=1
        for i in answers:
            if i not in answer_id:
                answer_id[i]=ans_ch+str(ans_cnt)
                ans_cnt+=1
        for i in range(0,len(questions)):
            f4.write(line+'\t'+ppl_str+cord_str+str(question_id[questions[i]])+'\t'+str(questions[i].encode('utf8'))+'\t'+str(answer_id[answers[i]])+'\t'+str(answers[i].encode('utf8'))+'\n')
    print question_id
    for i in question_id:
        f2.write(str(i.encode('utf8')) + '\t'+ str(question_id[i])+'\n')
    for i in answer_id:
        f.write(str(i.encode('utf8'))+'\t'+str(answer_id[i])+'\n')

def create_one_hot_answers(filename):
    ans_one_hot={}
    print filename
    f=open(filename,'r')
    cnt=0
    tot_answers=0
    for l in f.readlines():
        l=l[:-1]
        l=l.split('\t') 
        ans=l[-1]
        #print ans
        if ans not in ans_one_hot:
            ans_one_hot[ans]=0
        else:
            ans_one_hot[ans]+=1
    tot_answers=len(ans_one_hot)
    f.close()
    f=open(filename,'r')
    print tot_answers
   
    enc=[]
    ans_one_hot={}
    cnt=0
    for l in f.readlines():
        l=l[:-1]
        l=l.split('\t')
        ans=l[-1]
        if ans not in ans_one_hot:
            enc=[]
            for i in range(0,tot_answers):
                if cnt==i:
                    enc.append(1)
                else:
                    enc.append(0)
            ans_one_hot[ans]=enc
            cnt=cnt+1
        else:
            continue
    #print enc
    #print len(enc)
    return ans_one_hot,tot_answers
 

