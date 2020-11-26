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

import data_preprocessing
import training_data

def main():

        print "sdfsdf"
        #cords=data_preprocessnig.get_x_y(line)
        #create_image_info_file()
        #create_image_ques_file()
        #exit()
        #data_spatial('left.csv', 'one')
        #data_spatial('right.csv','five')
        #data_spatial('second_left.csv','two')
        #data_spatial('second_right.csv','four')
        #data_spatial('center.csv', 'three')
        ONE_HOT_ANSWERS,tot_answers=data_preprocessing.create_one_hot_answers('exp_data.csv')
        DATA_DIR = "./"
        MODEL_DIR = "./"
        WORD2VEC_BIN = "../GoogleNews-vectors-negative300.bin"
        WORD2VEC_EMBED_SIZE = 300

        QA_TRAIN_FILE = "exp_data.csv"

        QA_EMBED_SIZE = 64
        BATCH_SIZE = 16
        NBR_EPOCHS = 10
        ENTITIES_DIMENSIONS = tot_answers
        ## extract data

        print("Loading and formatting data...")
        qapairs = training_data.get_question_answer_pairs(os.path.join(DATA_DIR, QA_TRAIN_FILE))
        question_maxlen = max([len(qapair[0]) for qapair in qapairs])
        answer_maxlen = max([len(qapair[1]) for qapair in qapairs])
        seq_maxlen = max([question_maxlen, answer_maxlen])
        word2idx = training_data.build_vocab([], qapairs, [])
        print word2idx
        vocab_size = len(word2idx) + 1 # include mask character 0
        Xq, Xa, Y = training_data.vectorize_qapairs(qapairs, word2idx, question_maxlen,answer_maxlen,ONE_HOT_ANSWERS)
        print Xq
        print Xa
        print Y
        print seq_maxlen
        print question_maxlen
        print answer_maxlen
        Xqtrain, Xqtest, Xatrain, Xatest, Ytrain, Ytest = train_test_split(Xq, Xa, Y, test_size=0.1, random_state=42)
        print(Xqtrain.shape, Xqtest.shape, Xatrain.shape, Xatest.shape,Ytrain.shape, Ytest.shape)
        print("Loading Word2Vec model and generating embedding matrix...")
        word2vec = KeyedVectors.load_word2vec_format(os.path.join(DATA_DIR, WORD2VEC_BIN), binary=True)
        embedding_weights = np.zeros((vocab_size, WORD2VEC_EMBED_SIZE))
        embedding_weights_answers = np.zeros((vocab_size, ENTITIES_DIMENSIONS))
        for word, index in word2idx.items():
            try:
                embedding_weights[index, :] = word2vec[word.lower()]
            except KeyError:
                pass  # keep as zero (not ideal, but what else can we do?)
        del word2vec
        del word2idx
                
        print("Building model...")
        #qenc = Sequential()
        qenc = Input(shape=(question_maxlen,),dtype='int32')
        embedded_question = Embedding(output_dim=WORD2VEC_EMBED_SIZE, input_dim=vocab_size,weights=[embedding_weights], mask_zero=True)(qenc)
        x1=Bidirectional(LSTM(QA_EMBED_SIZE, return_sequences=False))(embedded_question)
        #qenc.add(Dropout(0.3))
        
        aenc = Input(shape=(answer_maxlen,),dtype='int32')
        embedded_answer = Embedding(output_dim=WORD2VEC_EMBED_SIZE, input_dim=vocab_size,weights=[embedding_weights], mask_zero=True)(aenc)
        y1=Bidirectional(LSTM(QA_EMBED_SIZE, return_sequences=False))(embedded_answer)
        merged = concatenate([x1,y1])

        #merged = x1
        final = (Dense(128, activation="relu"))(merged)
        final = Dropout(0.3)(final)
        final = (Dense(64, activation="relu"))(final)
        final = Dropout(0.3)(final)
        final = (Dense(32, activation="relu"))(final)
        final = (Dense(ENTITIES_DIMENSIONS, activation="softmax"))(final)

        model = Model(inputs = [qenc,aenc],outputs = final)
        
        model.compile(optimizer="adam", loss="categorical_crossentropy",
                      metrics=["accuracy"])

        print("Training...")
        checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR, "qa-lstm-best.hdf5"),verbose=1, save_best_only=True)
        history=model.fit([Xqtrain, Xatrain], Ytrain, batch_size=BATCH_SIZE,nb_epoch=NBR_EPOCHS, validation_split=0.1,callbacks=[checkpoint])
        
        print(history.history.keys())
        #  "Accuracy"
        plt.figure()
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.savefig('accuracy.png', bbox_inches='tight')
        # "Loss"
        plt.figure()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.savefig('loss.png', bbox_inches='tight')


        print("Evaluation...")
        loss, acc = model.evaluate([Xqtest, Xatest], Ytest, batch_size=BATCH_SIZE)
        print("Test loss/accuracy final model = %.4f, %.4f" % (loss, acc))

        model.save_weights(os.path.join(MODEL_DIR, "qa-lstm-final.hdf5"))
        with open(os.path.join(MODEL_DIR, "qa-lstm.json"), "wb") as fjson:
            fjson.write(model.to_json())

        model.load_weights(filepath=os.path.join(MODEL_DIR, "qa-lstm-best.hdf5"))
        loss, acc = model.evaluate([Xqtest, Xatest], Ytest, batch_size=BATCH_SIZE)
        print("Test loss/accuracy best model = %.4f, %.4f" % (loss, acc))
        print(model.summary())
        plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)


if __name__ == "__main__":
    main()
