import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as network
 
def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = list()

    for sentence in article:
        sentences.append(sentence.replace("[^\W]", " ").split(" "))
    
    sentences.pop() 
    
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = list()
 
    sent1 = [word.lower() for word in sent1]
    sent2 = [word.lower() for word in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # vector rappercurser in first sentence
    for word_v in sent1:
        if word_v in stopwords:
            continue
        vector1[all_words.index(word_v)] += 1
 
    # vector rappercurser in second sentence
    for word_v in sent2:
        if word_v in stopwords:
            continue
        vector2[all_words.index(word_v)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for index_1 in range(len(sentences)):
        for index_2 in range(len(sentences)):
            if index_1 == index_2: #ignore if both are same sentences
                continue 
            similarity_matrix[index_1][index_2] = sentence_similarity(sentences[index_1], sentences[index_2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=7):
    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    summarize_text = []

    sentences =  read_article(file_name)
    sentence_martix = build_similarity_matrix(sentences, stop_words)
    sentence_similarity_graph = network.from_numpy_array(sentence_martix)
    scores = network.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[id_v],sent) for id_v,sent in enumerate(sentences)), reverse=True)    
    
    for index in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[index][1]))

    return ". ".join(summarize_text)


#if __name__ == '__main__':
#    generate_summary("new.txt", 15)
    