#groq and tmbd api calls 

import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w342"

def get_tmdb_metadata(movie_name):
    search = requests.get(
        "https://api.themoviedb.org/3/search/movie",
        params={"api_key": TMDB_API_KEY, "query": movie_name}
    ).json()
    
    if not search['results']:
        return ""
    
    movie_id = search['results'][0]['id']
    
    details = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY}
    ).json()
    
    keywords = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/keywords",
        params={"api_key": TMDB_API_KEY}
    ).json()
    
    tagline = details.get('tagline', '')
    overview = details.get('overview', '')
    genres = ' '.join([g['name'] for g in details.get('genres', [])])
    kw = ' '.join([k['name'] for k in keywords.get('keywords', [])])
    
    return f"{tagline} {overview} {genres} {kw}"

def get_film_details(movie_name):
    """Display title, release year and poster art for a film.

    Returns an empty dict if TMDB is unreachable or has no match, so the
    caller can fall back to the slug it already has.
    """
    try:
        search = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": TMDB_API_KEY, "query": movie_name},
            timeout=8
        ).json()
    except (requests.RequestException, ValueError):
        return {}

    results = search.get('results') or []
    if not results:
        return {}

    top = results[0]
    poster_path = top.get('poster_path')
    release_date = top.get('release_date') or ''

    return {
        "title": top.get('title') or movie_name,
        "year": release_date[:4],
        "poster": f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else "",
    }

def explain_recommendation(user_phrase, movie_name, movie_metadata):
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{
            "role": "user",
            "content": f"""A user is looking for a movie that matches this vibe: "{user_phrase}"

The top recommendation is: {movie_name}

Here is a description of that movie: {movie_metadata}

In 2-3 sentences explain why this movie matches the user's vibe.
Focus ONLY on atmosphere, tone, and emotional experience.
Never reveal plot points, character details, or what happens in the film.
Don't start with 'I' or 'This movie'."""
        }]
    )
    return response.choices[0].message.content