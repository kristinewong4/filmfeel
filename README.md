# FilmFeel

FilmFeel recommends movies by *feeling* instead of genre or keyword. Describe
a mood — "a rainy city night," "quietly devastating," "strange and
dreamlike" — and it returns the films that match that atmosphere, each with a
short, spoiler-free explanation of why it fits.

## How it works

1. **Retrieval** — 250 films' TMDB metadata (tagline, overview, genres,
   keywords) are embedded with a sentence-transformer
   (`all-mpnet-base-v2`). The user's phrase is embedded the same way, and the
   top matches are found via cosine similarity.
2. **Explanation** — for each match, an LLM (via the Groq API) is prompted to
   explain, in 2-3 sentences, why the film matches the vibe — focused purely
   on tone and atmosphere, never plot or character details.
3. **Presentation** — a Streamlit UI displays the poster, title, year, and
   explanation for each recommendation.

## Tech stack

- **Python / Streamlit** — UI and app logic
- **sentence-transformers** (`all-mpnet-base-v2`) + **scikit-learn** — semantic
  search over movie metadata
- **Groq API** — LLM-generated explanations
- **TMDB API** — film metadata, posters, and release info

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key
TMDB_API_KEY=your_tmdb_key
```

Run the app:

```bash
streamlit run app.py
```

## Running tests

```bash
pytest tests/
```

## Project structure

```
app.py          # Streamlit UI and app flow
embeddings.py   # loads movie metadata, generates/compares embeddings
api.py          # Groq (explanations) and TMDB (metadata/posters) calls
data/           # cached TMDB metadata for 250 films
tests/          # unit tests for embeddings.py and api.py
```
