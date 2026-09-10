import html

import streamlit as st

from embeddings import load_metadata, embed_metadata, get_top_matches
from api import explain_recommendation, get_film_details

st.set_page_config(page_title="FilmFeel", layout="centered")

# --- look and feel -----------------------------------------------------------

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Inter:wght@300;400;450;500&display=swap');

:root {
  --ink: #12100E;
  --surface: #1A1714;
  --surface-2: #221E19;
  --line: #2C2723;
  --cream: #EFE7DA;
  --muted: #9A8F83;
  --faint: #6B635B;
  --brass: #C9A96A;
  --brass-dim: #8A7343;
  --serif: 'Cormorant Garamond', Georgia, 'Times New Roman', serif;
  --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.stApp { background: var(--ink); }

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer { display: none !important; }

.block-container,
[data-testid="stMainBlockContainer"] {
  max-width: 760px;
  padding-top: 4.5rem;
  padding-bottom: 5rem;
}

html, body, [class*="st-"] { font-family: var(--sans); }
::selection { background: var(--brass-dim); color: var(--ink); }

/* --- masthead --- */
.ff-eyebrow {
  font-size: 0.66rem;
  letter-spacing: 0.34em;
  text-transform: uppercase;
  color: var(--faint);
  text-align: center;
  margin-bottom: 1.4rem;
}
.ff-wordmark {
  font-family: var(--serif);
  font-size: 4.4rem;
  font-weight: 400;
  line-height: 1;
  letter-spacing: 0.005em;
  color: var(--cream);
  text-align: center;
  margin: 0;
}
.ff-wordmark span { color: var(--brass); }
.ff-rule {
  width: 44px;
  height: 1px;
  background: var(--brass-dim);
  margin: 1.6rem auto;
  border: 0;
}
.ff-lede {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.32rem;
  font-weight: 300;
  line-height: 1.6;
  color: var(--muted);
  text-align: center;
  margin: 0 auto 2.6rem;
  max-width: 30rem;
}

/* --- the ask --- */
.ff-label {
  font-size: 0.64rem;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--faint);
  margin-bottom: 0.55rem;
}

.stTextInput div[data-baseweb="input"] {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 2px;
  transition: border-color 160ms ease;
}
.stTextInput div[data-baseweb="input"]:focus-within { border-color: var(--brass-dim); }
.stTextInput div[data-baseweb="base-input"] { background: transparent; }
.stTextInput input {
  background: transparent;
  color: var(--cream);
  font-family: var(--sans);
  font-size: 1rem;
  font-weight: 300;
  padding: 0.95rem 1.1rem;
  caret-color: var(--brass);
}
.stTextInput input::placeholder {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.15rem;
  color: var(--faint);
}

/* --- suggestion chips --- */
.stButton > button {
  width: 100%;
  min-height: 3rem;
  background: transparent;
  color: var(--muted);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.45rem 0.7rem;
  transition: color 160ms ease, border-color 160ms ease, background 160ms ease;
}
.stButton > button p {
  font-family: var(--serif);
  font-style: italic;
  font-size: 0.95rem;
  font-weight: 400;
  line-height: 1.25;
}
.stButton > button:hover,
.stButton > button:focus:not(:active) {
  background: var(--surface);
  border-color: var(--brass-dim);
  color: var(--cream);
}

[data-testid="stSpinner"] p {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1rem;
  color: var(--muted);
}

/* --- results --- */
.ff-results-head {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 3.4rem 0 1.6rem;
}
.ff-results-head span {
  font-size: 0.64rem;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--faint);
  white-space: nowrap;
}
.ff-results-head:after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--line);
}

.ff-card {
  display: flex;
  gap: 1.6rem;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 3px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: border-color 200ms ease;
}
.ff-card:hover { border-color: #3A332C; }

.ff-poster {
  width: 104px;
  min-width: 104px;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 2px;
  border: 1px solid var(--line);
  background: var(--surface-2);
}
.ff-poster-blank {
  width: 104px;
  min-width: 104px;
  aspect-ratio: 2 / 3;
  border-radius: 2px;
  border: 1px solid var(--line);
  background: var(--surface-2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--serif);
  font-size: 1.9rem;
  color: var(--brass-dim);
  letter-spacing: 0.06em;
}

.ff-body { flex: 1; min-width: 0; }
.ff-rank {
  font-family: var(--serif);
  font-size: 0.8rem;
  letter-spacing: 0.24em;
  color: var(--brass-dim);
  margin-bottom: 0.35rem;
}
.ff-title {
  font-family: var(--serif);
  font-size: 1.9rem;
  font-weight: 500;
  line-height: 1.15;
  color: var(--cream);
  margin: 0 0 0.15rem;
}
.ff-year {
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  color: var(--faint);
  margin-bottom: 1rem;
}
.ff-why {
  font-size: 0.94rem;
  font-weight: 300;
  line-height: 1.72;
  color: #C8BEB1;
  margin: 0 0 1.15rem;
}
.ff-affinity { display: flex; align-items: center; gap: 0.7rem; }
.ff-affinity-label {
  font-size: 0.58rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--faint);
  white-space: nowrap;
}
.ff-meter { flex: 1; height: 1px; background: var(--line); position: relative; }
.ff-meter i { position: absolute; inset: 0 auto 0 0; background: var(--brass-dim); display: block; }
.ff-affinity-value {
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}

/* --- resting state + footer --- */
.ff-rest {
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.05rem;
  color: var(--faint);
  text-align: center;
  margin: 3.6rem 0 0;
  line-height: 1.8;
}
.ff-foot {
  margin-top: 4rem;
  padding-top: 1.4rem;
  border-top: 1px solid var(--line);
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--faint);
  text-align: center;
}

@media (max-width: 640px) {
  .ff-wordmark { font-size: 3rem; }
  .ff-lede { font-size: 1.1rem; }
  .ff-card { flex-direction: column; gap: 1.2rem; }
  .ff-poster, .ff-poster-blank { width: 88px; min-width: 88px; }
  .ff-title { font-size: 1.6rem; }
}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# --- helpers -----------------------------------------------------------------

SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "from",
               "in", "nor", "of", "on", "or", "the", "to", "with"}

NUMERALS = ["I", "II", "III", "IV", "V"]

PROMPTS = [
    "quietly devastating",
    "cozy and warm",
    "a rainy city night",
    "strange and dreamlike",
]


def prettify(slug):
    """Turn a metadata slug like '12-angry-men' into '12 Angry Men'.

    Only used when TMDB has no match. Small words stay lowercase unless they
    open or close the title, or follow something that isn't a word.
    """
    words = slug.replace('-', ' ').split()
    last = len(words) - 1
    return ' '.join(
        word
        if word in SMALL_WORDS and 0 < i < last and words[i - 1].isalpha()
        else word.capitalize()
        for i, word in enumerate(words)
    )


def affinity_width(score):
    """Map a cosine score onto a bar width, since raw scores cluster low."""
    return round(min(max((score - 0.10) / 0.55, 0.05), 1.0) * 100)


@st.cache_resource(show_spinner=False)
def load():
    metadata = load_metadata()
    return metadata, embed_metadata(metadata)


@st.cache_data(show_spinner=False)
def describe(phrase, title, metadata_text):
    return explain_recommendation(phrase, title, metadata_text)


@st.cache_data(show_spinner=False)
def details(slug):
    return get_film_details(slug.replace('-', ' '))


def render_card(rank, title, year, poster, why, score):
    initial = html.escape(title[:1].upper() or "F")
    art = (
        f'<img class="ff-poster" src="{html.escape(poster)}" alt="{html.escape(title)} poster">'
        if poster else
        f'<div class="ff-poster-blank">{initial}</div>'
    )
    year_line = f'<div class="ff-year">{html.escape(year)}</div>' if year else '<div class="ff-year"></div>'

    return (
        '<div class="ff-card">'
        f'{art}'
        '<div class="ff-body">'
        f'<div class="ff-rank">{NUMERALS[rank]}</div>'
        f'<h2 class="ff-title">{html.escape(title)}</h2>'
        f'{year_line}'
        f'<p class="ff-why">{html.escape(why)}</p>'
        '<div class="ff-affinity">'
        '<div class="ff-affinity-label">Affinity</div>'
        f'<div class="ff-meter"><i style="width:{affinity_width(score)}%"></i></div>'
        f'<div class="ff-affinity-value">{score:.2f}</div>'
        '</div></div></div>'
    )


# --- page --------------------------------------------------------------------

st.markdown('<div class="ff-eyebrow">Cinema by feeling</div>', unsafe_allow_html=True)
st.markdown('<h1 class="ff-wordmark">Film<span>Feel</span></h1>', unsafe_allow_html=True)
st.markdown('<hr class="ff-rule">', unsafe_allow_html=True)
st.markdown(
    '<p class="ff-lede">Tell us the mood you are in, not the genre you want. '
    'We will find the top 3 films that fit the vibe.</p>',
    unsafe_allow_html=True,
)

if "phrase" not in st.session_state:
    st.session_state.phrase = ""


def use_prompt(text):
    st.session_state.phrase = text


st.markdown('<div class="ff-label">What are you in the mood for</div>', unsafe_allow_html=True)
st.text_input(
    "What are you in the mood for",
    key="phrase",
    placeholder="something tender and a little sad...",
    label_visibility="collapsed",
)

for column, prompt in zip(st.columns(len(PROMPTS)), PROMPTS):
    column.button(prompt, key=f"prompt-{prompt}", on_click=use_prompt, args=(prompt,))

phrase = st.session_state.phrase.strip()

if not phrase:
    st.markdown(
        '<p class="ff-rest">Two hundred and fifty films waiting for you<br>',
        unsafe_allow_html=True,
    )
else:
    metadata, embeddings = load()

    with st.spinner("Reading the room..."):
        matches = get_top_matches(phrase, metadata, embeddings)

        cards = []
        for rank, (slug, score) in enumerate(matches):
            info = details(slug)
            title = info.get("title") or prettify(slug)
            why = describe(phrase, title, metadata[slug])
            cards.append(render_card(rank, title, info.get("year", ""), info.get("poster", ""), why, float(score)))

    st.markdown(
        '<div class="ff-results-head"><span>Three films for that feeling</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("".join(cards), unsafe_allow_html=True)

st.markdown(
    '<div class="ff-foot">250 films &nbsp;·&nbsp; Sentence embeddings &nbsp;·&nbsp; Groq LLM</div>',
    unsafe_allow_html=True,
)
