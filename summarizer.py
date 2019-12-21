#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:19:47 2019

@author: Carlos McNulty
"""

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import networkx as nx
from networkx.exception import NetworkXError
from networkx.exception import PowerIterationFailedConvergence
import re
import sys
import logging

nltk.download('stopwords')
nltk.download('punkt')
stop_words = stopwords.words('english')

#logger = logging.getLogger(__name__)

def summarize(text, limit=4):
    # Get sentence tokens from text
    sents = sent_tokenize(text)
    if len(sents) <= limit:
        return text
    
    sent_tokens = []
    clean_sents = []
    
    for sent in sents:
        # Remove punctuation from sentence
        clean_sent = re.sub("[^\s\w_]+", "", sent.lower()).lstrip()
        # Create tokens from sentence
        tokens = word_tokenize(clean_sent)
        # Store tokens and cleaned sentence
        sent_tokens.append(tokens)
        clean_sents.append(clean_sent)
    
    similarity_matrix = np.zeros((len(clean_sents), len(clean_sents)))
    
    for i in range(len(sent_tokens)):
        for j in range(len(sent_tokens)):
            if i != j:
                # Create vocab for both sentences from their tokens
                vocab = list(set(sent_tokens[i] + sent_tokens[j]))
                # Create count vectorizer with vocab of both sentences (stopwords removed)
                vectorizer = CountVectorizer(vocabulary=vocab, stop_words=stop_words, analyzer="word")
                # Create word count vectors
                vec1 = vectorizer.fit_transform([clean_sents[i]]).toarray()[0]
                vec2 = vectorizer.fit_transform([clean_sents[j]]).toarray()[0]
                # Compute cosine distance between vectors
                similarity_matrix[i][j] = 1 - cosine_distance(vec1, vec2)
            
    # Create graph from similarity matrix
    similarity_graph = nx.from_numpy_array(similarity_matrix)
    try:
        # Rank graph
        scores = nx.pagerank(G = similarity_graph, max_iter=500)
    except (PowerIterationFailedConvergence, NetworkXError) as error:
        return text
    except:
        return text
    
    # Sort sentences by their page rank
    ranked_sents = sorted(((scores[i],sent) for i,sent in enumerate(sents)), reverse=True)   
    summary = [sent for _, sent in ranked_sents]
    # Limit the number of sentences in summary
    return " ".join(summary[:limit])


