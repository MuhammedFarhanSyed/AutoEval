# ==============================================================================
# NLP & TEXT SIMILARITY MODULE
# ==============================================================================
# This module provides functions to calculate text similarity between student answers
# and reference model answers using Natural Language Processing (NLP) techniques.
# ==============================================================================

import nltk
from nltk.tokenize import word_tokenize              # Splits text into individual words/tokens
from nltk.metrics import jaccard_distance             # Measures set dissimilarity between word sets
from nltk.corpus import stopwords                    # Common English words ('is', 'the', 'and') to ignore
from sklearn.feature_extraction.text import CountVectorizer  # Converts text into word frequency vectors
from sklearn.metrics.pairwise import cosine_similarity       # Computes spatial angle/similarity between vectors


def cosine_similarity_text(text1, text2):
    """
    Calculate text similarity between two texts using Scikit-Learn's Cosine Similarity.
    
    Parameters:
        text1 (str): First text string (e.g., student answer).
        text2 (str): Second text string (e.g., reference answer).
        
    Returns:
        float: Similarity score between 0.0 (completely different) and 1.0 (identical word frequency).
    """
    # Step 1: Convert raw text strings into numerical word-frequency count vectors
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    
    # Step 2: Compute the cosine similarity between vector 0 (text1) and vector 1 (text2)
    similarity = cosine_similarity(vectorizer[0], vectorizer[1])
    
    # Step 3: Extract and return the float score from the 2D array matrix
    return similarity[0][0]


def text_similarity_nltk(answer1, answer2):
    """
    Calculate text similarity between student answer and reference model answer using NLTK Jaccard Distance.
    
    Processing Steps:
      1. Load standard English stop words ('is', 'a', 'the', etc.).
      2. Tokenize both answers into individual words.
      3. Convert tokens to lowercase and strip out stop words.
      4. Compute Jaccard Similarity Coefficient = 1 - Jaccard Distance.
      
    Parameters:
        answer1 (str): Student's answer string.
        answer2 (str): Faculty reference model answer string.
        
    Returns:
        float: Similarity coefficient score between 0.0 (no word overlap) and 1.0 (exact match).
    """
    # Step 1: Get the set of English stop words to filter out common filler words
    stop_words = set(stopwords.words("english"))

    # Step 2: Tokenize each answer string into a list of individual words
    tokenized_answers = [word_tokenize(answer) for answer in [answer1, answer2]]

    # Step 3: Convert all words to lowercase and remove any stop words
    filtered_answers = [[word for word in answer if word.lower() not in stop_words] for answer in tokenized_answers]

    # Step 4: Convert filtered token lists into sets of unique words and calculate Jaccard Similarity (1 - Jaccard Distance)
    similarity = 1 - jaccard_distance(set(filtered_answers[0]), set(filtered_answers[1]))

    # Step 5: Return the similarity score float (0.0 to 1.0)
    return similarity




