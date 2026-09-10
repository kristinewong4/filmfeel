# this file loads and encodes the movie data 
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-mpnet-base-v2')

def load_metadata(path='data/tmdb_metadata.json'):
    with open(path, 'r') as f:
        return json.load(f)

def embed_metadata(metadata: dict):
    texts = list(metadata.values())
    embeddings = model.encode(texts)
    return embeddings

def get_top_matches(user_phrase, metadata, embeddings, top_n=3):
    phrase_embedding = model.encode([user_phrase])
    scores = cosine_similarity(phrase_embedding, embeddings)[0]
    
    top_indices = np.argsort(scores)[-top_n:][::-1]
    movie_list = list(metadata.keys())
    
    results = []
    for idx in top_indices:
        movie = movie_list[idx]
        score = scores[idx]
        results.append((movie, score))
    
    return results