# 🕌 Quran Verse Recommender by Mood

A beautiful AI-powered app that recommends Quran verses based on your emotional state.
Built with Python, Scikit-learn (TF-IDF), and Streamlit.

---

## 📸 Features

- **12 mood buttons** — one click to get relevant verses
- **Free text search** — type your feelings in your own words
- **30 curated Quran verses** with:
  - Arabic text (right-to-left)
  - English translation
  - Urdu translation
  - Personal reflection note
- **ML-powered** — TF-IDF + Cosine Similarity finds the most relevant verses
- **Beautiful Islamic-themed UI** — dark green & gold design

---

## 🛠️ Setup Instructions

### Step 1 — Install Python
Make sure Python 3.8+ is installed.
Download from: https://python.org

### Step 2 — Install Dependencies
Open terminal/cmd in the project folder and run:

```bash
pip install -r requirements.txt
```

### Step 3 — Run the App

```bash
streamlit run app.py
```

Your browser will open automatically at: `http://localhost:8501`

---

## 📁 Project Structure

```
quran_mood_app/
│
├── app.py              ← Main Streamlit app (UI)
├── recommender.py      ← ML engine (TF-IDF + Cosine Similarity)
├── quran_data.py       ← Quran verses dataset (30 verses)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## 🤖 How the ML Works

1. **Dataset**: 30 carefully selected Quran verses with keywords, mood tags, English & Urdu translations
2. **TF-IDF Vectorizer**: Converts all verse text + keywords into numerical vectors
3. **Cosine Similarity**: Compares user's mood query against all verse vectors
4. **Top 4 results**: Returns verses with highest similarity scores

```python
# Core logic (from recommender.py)
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
verse_matrix = vectorizer.fit_transform(corpus)

query_vec = vectorizer.transform([user_query])
scores = cosine_similarity(query_vec, verse_matrix)
top_verses = argsort(scores)[-4:]  # top 4 matches
```

---

## 🚀 Deploy Online (Free)

### Option 1 — Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to share.streamlit.io
3. Connect your repo → deploy in 2 minutes
4. Get a free public URL to share!

### Option 2 — Hugging Face Spaces
1. Create account at huggingface.co
2. New Space → Streamlit → upload files
3. Free hosting with nice URL

---

## 🔧 How to Upgrade

### Add More Verses
Open `quran_data.py` and add more entries to the `VERSES` list following the same format.

### Use Sentence-BERT (More Accurate)
Replace TF-IDF with Sentence-BERT for better semantic understanding:
```bash
pip install sentence-transformers
```
Then in `recommender.py`:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(corpus)
```

### Add More Languages
Add a `hindi` or `arabic_tafsir` field to each verse in `quran_data.py`.

---

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| ML Model | TF-IDF + Cosine Similarity (scikit-learn) |
| UI Framework | Streamlit |
| Data | Custom curated Quran dataset |
| Fonts | Amiri (Arabic), Lora, Inter |
| Deployment | Streamlit Cloud / Hugging Face Spaces |

---

## 👤 Author
Built as a portfolio ML project.
Feel free to expand, improve, and share!

---

## 🤲 Dua
May this project be a source of benefit and guidance.
وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ
*"And We send down from the Quran that which is healing and mercy."* — Al-Isra 17:82
