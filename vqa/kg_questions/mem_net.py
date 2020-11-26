import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

from keras.layers import Input
from keras.layers.core import Activation, Dense, Dropout, Permute
from keras.layers.embeddings import Embedding
from keras.layers.merge import add, concatenate, dot, multiply
from keras.layers.recurrent import LSTM,GRU
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import collections
import itertools
import nltk
import numpy as np
import matplotlib.pyplot as plt
import os
from keras.utils import plot_model
import keras.backend as K
import tensorflow as tf
import time

def get_data(file):
    stories, questions, answers = [],[],[]
    story_text = []
    question,answer=[],[]
    with open(file) as f:
        for line in f:
            line=line[:-1]
            line_no, text = line.split('\t',1)
            if '\t' in text:
                question, answer, _ = text.split('\t')
                questions.append(question)
                answers.append(answer)
                stories.append(story_text)
                story_text = []
            else:
                story_text.append(text)
            #print question
            #print answer
            #print story_text
    f.close()

    return stories, questions, answers

def build_vocab(train_data, test_data):
    counter = collections.Counter()
    for stories, questions, answers in [train_data, test_data]:
        for story in stories:
            for sent in story:
                for word in nltk.word_tokenize(sent):
                    counter[word.lower()] += 1
        for question in questions:
            for word in nltk.word_tokenize(question):
                counter[word.lower()] +=1
        for answer in answers:
            #for word in nltk.word_tokenize(answer):
            #    print word
            word=answer
            counter[word.lower()] += 1
    word2idx = {w: (i + 1) for i, (w, _) in enumerate(counter.most_common())}
    print word2idx
    word2idx['PAD'] = 0
    idx2word = {v: k for k, v in word2idx.items()}

    return word2idx, idx2word

def get_maxlens(train_data, test_data):
    story_maxlen, question_maxlen = 0, 0
    for stories, questions, _ in [train_data, test_data]:
        for story in stories:
            story_len = 0
            for sent in story:
                story_len += len(nltk.word_tokenize(sent))
            story_maxlen = max(story_len, story_maxlen)
        for question in questions:
            question_len = len(nltk.word_tokenize(question))
            question_maxlen = max(question_len, question_maxlen)

    return story_maxlen, question_maxlen

def vectorize(data, word2idx, story_maxlen, question_maxlen):
    X_story, X_question, Y = [], [], []
    stories, questions, answers = data
    for story, question, answer in zip(stories, questions, answers):
        X_s = [[word2idx[w.lower()] for w in nltk.word_tokenize(s)] for s in story]
        X_s = list(itertools.chain.from_iterable(X_s))
        X_q = [word2idx[w.lower()] for w in nltk.word_tokenize(question)]
        X_story.append(X_s)
        X_question.append(X_q)
        Y.append(word2idx[answer.lower()])

    return pad_sequences(X_story, maxlen=story_maxlen),pad_sequences(X_question, maxlen=question_maxlen), np_utils.to_categorical(Y, num_classes=len(word2idx))

def main():
    #DATA_DIR = './data/en-10k/'
    #TRAIN_FILE = os.path.join(DATA_DIR, 'qa1_single-supporting-fact_train.txt')
    #TEST_FILE = os.path.join(DATA_DIR, 'qa1_single-supporting-fact_test.txt')
    DATA_DIR = './'
    MODEL_DIR='./'
    TRAIN_FILE = os.path.join(DATA_DIR, 'train.csv')
    TEST_FILE = os.path.join(DATA_DIR, 'test.csv')

    data_train = get_data(TRAIN_FILE)
    data_test = get_data(TEST_FILE)

    word2idx, idx2word = build_vocab(data_train, data_test)

    vocab_size = len(word2idx)

    story_maxlen, question_maxlen = get_maxlens(data_train, data_test)
    
    X_story_train, X_question_train, Y_train = vectorize(data_train, word2idx, story_maxlen, question_maxlen)
    X_story_test, X_question_test, Y_test = vectorize(data_test, word2idx, story_maxlen, question_maxlen)
    
    print X_story_train.shape, X_question_train.shape, Y_train.shape
    EMBEDDING_SIZE = story_maxlen
    LATENT_SIZE = 32

    print "Building model..."

    story_input = Input(shape=(story_maxlen,))
    question_input = Input(shape=(question_maxlen,))
    
    #####
    story_encoder = Embedding(input_dim=vocab_size,output_dim=EMBEDDING_SIZE,input_length=story_maxlen)(story_input)
    story_encoder = Dropout(0.3)(story_encoder)
    print story_encoder.shape
    story_encoder = GRU(story_maxlen, input_shape=(story_maxlen,EMBEDDING_SIZE),activation='sigmoid', return_sequences=True)(story_encoder)
    story_encoder = GRU(story_maxlen, input_shape=(story_maxlen,EMBEDDING_SIZE),activation='sigmoid', return_sequences=True, go_backwards=True)(story_encoder)
    print story_encoder.shape
    story_encoder = Permute((2,1))(story_encoder)
    print story_encoder.shape

    question_encoder = Embedding(input_dim=vocab_size, output_dim=EMBEDDING_SIZE, input_length=question_maxlen)(question_input)
    question_encoder = Dropout(0.3)(question_encoder)
    question_encoder = GRU(EMBEDDING_SIZE, input_shape=(vocab_size, EMBEDDING_SIZE),activation='sigmoid', return_sequences=True)(question_encoder)
    question_encoder = GRU(EMBEDDING_SIZE, input_shape=(vocab_size, EMBEDDING_SIZE),activation='sigmoid', return_sequences=True, go_backwards=True)(question_encoder)

    match = dot([story_encoder, question_encoder], axes=[2,2])
    match = Activation('softmax')(match)

    story_encoder_c = Embedding(input_dim=vocab_size,output_dim=question_maxlen,input_length=story_maxlen)(story_input)
    story_encoder_c = Dropout(0.3)(story_encoder_c)
    story_encoder_c = GRU(question_maxlen, input_shape=(story_maxlen,question_maxlen),activation='sigmoid', return_sequences=True)(story_encoder_c)
    story_encoder_c = GRU(question_maxlen, input_shape=(story_maxlen,question_maxlen),activation='sigmoid', return_sequences=True, go_backwards=True)(story_encoder_c)

    #response = multiply([match, story_encoder_c])
    response = add([match, story_encoder_c])
    response = Permute((2,1))(response)
    ####
    print "first done"
    story_encoder = Permute((2,1))(story_encoder)
    print story_encoder.shape
    match = dot([response, story_encoder], axes=[2,2])
    match = Activation('softmax')(match)
    print match.shape
    match = Permute((2,1))(match)
    print match.shape
    #response = multiply([match, story_encoder_c])
    response = add([match, story_encoder_c])
    print response.shape
    response = Permute((2,1))(response)
    ###
    print "first done"
    story_encoder = Permute((2,1))(story_encoder)
    print story_encoder.shape
    match = dot([response, story_encoder], axes=[2,2])
    match = Activation('softmax')(match)
    print match.shape
    match = Permute((2,1))(match)
    print match.shape
    #response = multiply([match, story_encoder_c])
    response = add([match, story_encoder_c])
    print response.shape
    response = Permute((2,1))(response)
    #match = dot([story_encoder, response], axes=[2,2])
    #response = add([match, story_encoder_c])
    ###
    #response = Permute((2,1))(response)

    

    answer = concatenate([response, question_encoder], axis=-1)
    answer = LSTM(LATENT_SIZE)(answer)
    answer = Dropout(0.3)(answer)
    answer = Dense(vocab_size)(answer)
    output = Activation('softmax')(answer)
    
    model = Model(inputs=[story_input, question_input], outputs=output)
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    BATCH_SIZE = 32
    NUM_EPOCHS = 40
    print "training..."
    inp=model.input
    outputs = [layer.output for layer in model.layers]
    functor = [K.function([inp]+ [K.learning_phase()], [out]) for out in outputs]
    test = np.random.random([vocab_size,EMBEDDING_SIZE])[np.newaxis,...]
    print functor
    checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR,"qa-memnn-best.hdf5"), verbose=1, save_best_only=True)

    history = model.fit([X_story_train, X_question_train], [Y_train],batch_size=BATCH_SIZE, epochs=NUM_EPOCHS, validation_data=([X_story_test, X_question_test], [Y_test]), callbacks=[checkpoint])

    plt.figure()
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train','validation'],loc='upper left')
    plt.savefig('accuracy.png', bbox_inches='tight')

    plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_acc'])
    plt.title('model loss')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train','validation'],loc='upper left')
    plt.savefig('loss.png', bbox_inches='tight')
   
    print "Evaluation..."
    loss, acc = model.evaluate([X_story_test, X_question_test], [Y_test], batch_size=BATCH_SIZE)
    print "Test loss/accuracy final model = %.4f, %.4f" % (loss,acc)

    model.save_weights(os.path.join(MODEL_DIR,"qa-memnn-final.hdf5"))
    with open(os.path.join(MODEL_DIR,"qa-memnn.json"),"wb") as fjson:
        fjson.write(model.to_json())
    model.load_weights(filepath=os.path.join(MODEL_DIR, "qa-memnn-best.hdf5"))
    loss, acc = model.evaluate([X_story_test, X_question_test], [Y_test], batch_size=BATCH_SIZE)
    print("Test loss/accuracy best model = %.4f, %.4f" % (loss, acc))
    print model.summary()
    plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)


if __name__=="__main__":
    main()
