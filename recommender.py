"""
Quran Verse Recommender Engine
Uses TF-IDF + Cosine Similarity to find relevant verses based on user mood/input.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from quran_data import VERSES

# ── Mood to search query mapping ──────────────────────────────────────────────
MOOD_QUERIES = {
    "😔 Sad / Grieving":        "sad grief sorrow loss crying heartbroken pain suffering",
    "😰 Anxious / Stressed":    "anxiety stress worry fear nervous overwhelmed pressure",
    "😤 Angry / Frustrated":    "angry frustrated rage conflict betrayed hurt enemy",
    "🙏 Grateful / Blessed":    "grateful thankful blessed happy content joy blessing",
    "😟 Lost / Confused":       "lost confused no direction purpose meaning searching seeking",
    "💪 Need Motivation":       "motivation tired giving up keep going strength perseverance struggle",
    "😔 Lonely / Isolated":     "lonely alone isolated no one company abandoned",
    "😰 Scared / Fearful":      "scared fearful danger uncertain courage help",
    "😞 Guilty / Regret":       "guilty shame regret sin mistake forgiveness repentance",
    "🌟 Seeking Purpose":       "purpose meaning why created exist reason life direction",
    "🕊️ Want Peace / Calm":    "peace calm tranquil rest serene quiet heart",
    "🌈 Hopeless / Desperate":  "hopeless no hope desperate dark impossible relief mercy",
}

# ── Build TF-IDF corpus ────────────────────────────────────────────────────────
def _build_corpus():
    """Combine all searchable text for each verse."""
    corpus = []
    for v in VERSES:
        text = (
            v["english"] + " " +
            v["keywords"] + " " +
            " ".join(v["moods"]) + " " +
            v["reflection"]
        )
        corpus.append(text.lower())
    return corpus

CORPUS = _build_corpus()

# Fit vectorizer once on import
VECTORIZER = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
VERSE_MATRIX = VECTORIZER.fit_transform(CORPUS)


def recommend_by_query(query: str, top_n: int = 4) -> list[dict]:
    """
    Given a free-text query (mood description), return top_n most relevant verses.
    """
    query_vec = VECTORIZER.transform([query.lower()])
    scores = cosine_similarity(query_vec, VERSE_MATRIX).flatten()
    top_indices = np.argsort(scores)[::-1][:top_n]

    results = []
    for idx in top_indices:
        verse = VERSES[idx].copy()
        verse["score"] = round(float(scores[idx]), 4)
        results.append(verse)

    return results


def recommend_by_mood(mood_label: str, top_n: int = 4) -> list[dict]:
    """
    Given a mood label from MOOD_QUERIES, return top_n relevant verses.
    """
    query = MOOD_QUERIES.get(mood_label, mood_label)
    return recommend_by_query(query, top_n)


def get_mood_options() -> list[str]:
    """Return list of mood button labels."""
    return list(MOOD_QUERIES.keys())


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing recommender...\n")
    results = recommend_by_mood("😰 Anxious / Stressed", top_n=3)
    for r in results:
        print(f"[{r['surah_name']} {r['ayah']}] Score: {r['score']}")
        print(f"  {r['english']}")
        print(f"  {r['urdu']}\n")
