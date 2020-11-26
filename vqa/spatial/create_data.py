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

def text_to_wordlist(text, remove_stopwords=False, stem_words=False):
    # Clean the text, with the option to remove stopwords and to stem words.
    
    # Convert words to lower case and split them
    text = text.lower().split()

    # Optionally, remove stop words
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
    
    text = " ".join(text)

    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    
    # Optionally, shorten words to their stems
    if stem_words:
        text = text.split()
        stemmer = SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)
    
    # Return a list of words
    return(text)

def get_question_answer_pairs(filename):
    f=open(filename,'r')
    qapairs=[]
    for l in f.readlines():
        l=l[:-1]
        l=l.split('\t')
        question=l[12]
        answer=l[1:6]
        f_a=[]
        f_c=[]
        for i in answer:
            if i != 'NONE':
                f_a.append(i)
        answer=f_a
        cords=l[6:11]
        for i in cords:
            if i!='dss':
                f_c.append(i)
        cords=f_c
        print answer
        print cords
        correct_answer=l[13]
        qwords = nltk.word_tokenize(question)
        awords = answer
        acords=cords
        qapairs.append((qwords, awords, acords, correct_answer))
    return qapairs

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
    

def build_vocab(stories, qapairs, testqs):
    wordcounts = collections.Counter()
    for story in stories:
        for sword in story:
            wordcounts[sword] += 1
    for qapair in qapairs:
        for qword in qapair[0]:
            wordcounts[qword] += 1
        for aword in qapair[1]:
            wordcounts[aword] += 1
        for acord in qapair[2]:
            wordcounts[acord] +=1
    for testq in testqs:
        for qword in testq[0]:
            wordcounts[qword] += 1
        for aword in testq[1]:
            wordcounts[aword] += 1
    words = [wordcount[0] for wordcount in wordcounts.most_common()]
    word2idx = {w: i+1 for i, w in enumerate(words)}  # 0 = mask
    return word2idx

def vectorize_qapairs(qapairs, word2idx, seq_maxlen,ans_vec):
    Xq, Xa, Xc, Y = [], [], [], []
    for qapair in qapairs:
        Xq.append([word2idx[qword] for qword in qapair[0]])
        Xa.append([word2idx[aword] for aword in qapair[1]])
        Xc.append([word2idx[cword] for cword in qapair[2]])
        Y.append(ans_vec[qapair[3]])
    return (pad_sequences(Xq, maxlen=seq_maxlen),
            pad_sequences(Xa, maxlen=seq_maxlen),
            pad_sequences(Xc, maxlen=seq_maxlen),
            np.array(Y))

def create_one_hot_answers(filename):
    ans_one_hot={}
    print filename
    f=open(filename,'r')
    cnt=0
    tot_answers=0
    for l in f.readlines():
        l=l[:-1]
        l=l.split('\t') 
        ans=l[-2]
        print ans
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
        ans=l[-2]
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
    return ans_one_hot
        

def main():
        print "sdfsdf"
        #cords=get_x_y(line)
        #create_image_info_file()
        #create_image_ques_file()
        #exit()
        #data_spatial('left.csv', 'one')
        #data_spatial('right.csv','five')
        #data_spatial('second_left.csv','two')
        #data_spatial('second_right.csv','four')
        #data_spatial('center.csv', 'three')
        ONE_HOT_ANSWERS=create_one_hot_answers('spatial_data.csv')
        DATA_DIR = "./"
        MODEL_DIR = "./"
        WORD2VEC_BIN = "GoogleNews-vectors-negative300.bin"
        WORD2VEC_EMBED_SIZE = 300

        QA_TRAIN_FILE = "spatial_data.csv"

        QA_EMBED_SIZE = 64
        BATCH_SIZE = 16
        NBR_EPOCHS = 10
        ENTITIES_DIMENSIONS = 5379
        ## extract data

        print("Loading and formatting data...")
        qapairs = get_question_answer_pairs(os.path.join(DATA_DIR, QA_TRAIN_FILE))
        question_maxlen = max([len(qapair[0]) for qapair in qapairs])
        answer_maxlen = max([len(qapair[1]) for qapair in qapairs])
        seq_maxlen = max([question_maxlen, answer_maxlen])
        word2idx = build_vocab([], qapairs, [])
        print word2idx
        vocab_size = len(word2idx) + 1 # include mask character 0
        Xq, Xa, Xc, Y = vectorize_qapairs(qapairs, word2idx, seq_maxlen,ONE_HOT_ANSWERS)
        print Xq
        print Xa
        print Y
        print seq_maxlen
        Xqtrain, Xqtest, Xatrain, Xatest, Xctrain, Xctest, Ytrain, Ytest = train_test_split(Xq, Xa, Xc, Y, test_size=0.1, random_state=42)
        print(Xqtrain.shape, Xqtest.shape, Xatrain.shape, Xatest.shape, Xctrain.shape, Xctest.shape,Ytrain.shape, Ytest.shape)
        print("Loading Word2Vec model and generating embedding matrix...")
        word2vec = KeyedVectors.load_word2vec_format(os.path.join(DATA_DIR, WORD2VEC_BIN), binary=True)
        embedding_weights = np.zeros((vocab_size, WORD2VEC_EMBED_SIZE))
        embedding_weights_answers = np.zeros((vocab_size, ENTITIES_DIMENSIONS))
        for word, index in word2idx.items():
            if word in ONE_HOT_ANSWERS: 
                embedding_weights_answers[index, : ] = ONE_HOT_ANSWERS[word]
            try:
                embedding_weights[index, :] = word2vec[word.lower()]
            except KeyError:
                pass  # keep as zero (not ideal, but what else can we do?)
        del word2vec
        del word2idx
                
        print("Building model...")
        #qenc = Sequential()
        qenc = Input(shape=(seq_maxlen,),dtype='int32')
        embedded_question = Embedding(output_dim=WORD2VEC_EMBED_SIZE, input_dim=vocab_size,weights=[embedding_weights], mask_zero=True)(qenc)
        x1=Bidirectional(LSTM(QA_EMBED_SIZE, return_sequences=False))(embedded_question)
        x1=Dropout(0.3)(x1)
        #qenc.add(Dropout(0.3))
        cenc = Input(shape=(seq_maxlen,),dtype='int32')
        embedded_cord = Embedding(output_dim=WORD2VEC_EMBED_SIZE, input_dim=vocab_size,weights=[embedding_weights], mask_zero=True)(cenc)
        c1=Bidirectional(LSTM(QA_EMBED_SIZE, return_sequences=False))(embedded_cord)
        c1=Dropout(0.3)(c1)
        
        aenc = Input(shape=(seq_maxlen,),dtype='int32')
        embedded_answer = Embedding(output_dim=ENTITIES_DIMENSIONS, input_dim=vocab_size,weights=[embedding_weights_answers], mask_zero=True)(aenc)
        y1=Bidirectional(LSTM(1500, return_sequences=False))(embedded_answer)
        y1=Dropout(0.3)(y1)
        #aenc = Sequential()
        #aenc.add(Embedding(output_dim=WORD2VEC_EMBED_SIZE, input_dim=vocab_size,weights=[embedding_weights], mask_zero=True))
        #aenc.add(LSTM(QA_EMBED_SIZE,  return_sequences=False))
        #aenc.add(Dropout(0.3))
        merged = concatenate([x1,y1])

        merged = concatenate([merged,c1])
        #merged = x1
        final = (Dense(5500, activation="relu"))(merged)
        final = (Dense(5379, activation="softmax"))(final)

        model = Model(inputs = [qenc,aenc, cenc],outputs = final)
        
        model.compile(optimizer="adam", loss="categorical_crossentropy",
                      metrics=["accuracy"])

        print("Training...")
        checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR, "qa-lstm-best.hdf5"),verbose=1, save_best_only=True)
        model.fit([Xqtrain, Xatrain, Xctrain], Ytrain, batch_size=BATCH_SIZE,nb_epoch=NBR_EPOCHS, validation_split=0.1,callbacks=[checkpoint])

        print("Evaluation...")
        loss, acc = model.evaluate([Xqtest, Xatest, Xctest], Ytest, batch_size=BATCH_SIZE)
        print("Test loss/accuracy final model = %.4f, %.4f" % (loss, acc))

        model.save_weights(os.path.join(MODEL_DIR, "qa-lstm-final.hdf5"))
        with open(os.path.join(MODEL_DIR, "qa-lstm.json"), "wb") as fjson:
            fjson.write(model.to_json())

        model.load_weights(filepath=os.path.join(MODEL_DIR, "qa-lstm-best.hdf5"))
        loss, acc = model.evaluate([Xqtest, Xatest, Xctest], Ytest, batch_size=BATCH_SIZE)
        print("Test loss/accuracy best model = %.4f, %.4f" % (loss, acc))
            

if __name__ == "__main__":
    main()
