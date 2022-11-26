import pandas as pd
import csv
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from nltk.corpus import stopwords
from pprint import pprint
import re
import sys

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import nltk
import spacy


def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

orig_stdout = sys.stdout
f = open('wine_topic_part_2.txt', 'w')
sys.stdout = f

mallet_path = '/home/lily/Downloads/mallet-2.0.8' # update this path
#wines_path = '/home/lily/Downloads'
#wine = "Governo all'uso Toscano 2018" # Chianti 2020 
wine = "Chianti Classico 2019"
language = "en"
print("*********** ", wine, " ***********")
stop_words = stopwords.words('english')

data = pd.read_csv('/home/lily/PycharmProjects/wine/wines_part_2.csv', delimiter=";", low_memory=False) # '/home/lily/Downloads/wines.csv'
#data = pd.read_csv("Wines1.csv", delimiter=";")
#first_half = data.iloc[:20, ]
#first_half.to_csv("Wines1.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, sep = ';')
mas_notes = []
# print(type(wine))
# print(wine, sep = "\n")
for row in data.itertuples():
    # print(type(row[0]), type(row[1]), type(row[2]), type(row[3]), type(row[4]))
    # print(type(row[2]), "\t")
    # print( "number = "+ str(row[0])+"\n" + "year = " + str(row[1]) + "\n"+ "wine_name=" +row[2]+ "\nотзыв = " +row[3], "\nязык=" +row[4]+ "\n")
    #break
    if (row[2] == wine):#((str(row[2])).replace(" ","") == (str(wine)).replace(" ","")): # было row[2], в этот раз просто взяли без первого столбца
        if (row[4] == language):  # аналогично, row[2]
            mas_notes.append(row[3]) # row[3]
            # print("everything correct")
            # break
        # print("testing") #test output
        print("correct wine\n")
        continue
    break
         
       
    data_words = list(sent_to_words(mas_notes))

    '''
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

    #df = pd.read_json('https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json')
    df = pd.read_json('newsgroups.json')
    #print(df.target_names.unique())
    df.head()
    # Convert to list
    data = df.content.values.tolist()
    '''

    '''
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]
    '''

    #data_words = list(sent_to_words(data))

    #print(data_words[:1])
    #3,4
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)#4

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # See trigram example
    #print(trigram_mod[bigram_mod[data_words[0]]])
    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)


    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)
    #print(data_words_bigrams[0])

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) #en_core_web_md

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    #print(data_lemmatized[:1])
    #print(data_lemmatized[1:2])
    #print(data_lemmatized[2:3])
    # Почему эта штука удаляет нужное

    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    #print(texts) test output
    corpus = [id2word.doc2bow(text) for text in texts]
    #print(len(corpus))
    # print([[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]])
    # print(corpus[:1])

    # Build LDA model
    for topics in range(5,51, 5):#51
        print("\n---------------------------------\n")
        print("Number of topics: ", topics)
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=topics, 
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
        # ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=topics, id2word=id2word)
        # Print the Keyword in the 10 topics
        pprint(lda_model.print_topics())
        # pprint(ldamallet.show_topics(formatted=False))

        doc_lda = lda_model[corpus]
        print('\nPerplexity: ', lda_model.log_perplexity(corpus), "\n")  # a measure of how good the model is. lower the better.

    wine = row[2]
    print("*********** ", wine, " ***********")
    mas_notes = []
    # break
    
    
sys.stdout = orig_stdout
f.close()
    
'''
 
print('This message will be displayed on the screen.')

original_stdout = sys.stdout # Save a reference to the original standard output

with open('filename.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print('This message will be written to a file.')
    sys.stdout = original_stdout # Reset the standard output to its original value




orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f



sys.stdout = orig_stdout
f.close()
'''   



