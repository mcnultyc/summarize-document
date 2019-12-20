#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:19:47 2019

@author: Carlos McNulty
"""

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import networkx as nx
import re

nltk.download('stopwords')
nltk.download('punkt')

def summarize(text, stop_words, limit=5):
    sents = sent_tokenize(text)
    
    sent_tokens = []
    clean_sents = []
    
    for sent in sents:
        clean_sent = re.sub("[^\s\w_]+", "", sent.lower()).lstrip()
        tokens = word_tokenize(clean_sent)
        sent_tokens.append(tokens)
        clean_sents.append(clean_sent)
    
    
    similarity_matrix = np.zeros((len(clean_sents), len(clean_sents)))
    
    for i in range(len(sent_tokens)):
        for j in range(len(sent_tokens)):
            if i != j:
                vocab = list(set(sent_tokens[i] + sent_tokens[j]))
                vectorizer = CountVectorizer(vocabulary=vocab, stop_words=stop_words, analyzer="word")
                vec1 = vectorizer.fit_transform([clean_sents[i]]).toarray()[0]
                vec2 = vectorizer.fit_transform([clean_sents[j]]).toarray()[0]
                similarity_matrix[i][j] = 1 - cosine_distance(vec1, vec2)
            
    
    similarity_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(similarity_graph)
    ranked_sents = sorted(((scores[i],sent) for i,sent in enumerate(sents)), reverse=True)   
    summary = [sent for _, sent in ranked_sents]
    return " ".join(summary[:limit])

