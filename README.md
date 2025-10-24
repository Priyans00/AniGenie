# AniGenie 

AniGenie is a lightweight anime recommender that suggests titles based on your watch history using semantic embeddings and fast similarity search.

## Why?

Too many choices. AniGenie filters anime by matching metadata (title, genres, characters,summary, ratings ) to user preferences for quick, relevant suggestions.

##nHow?

- Collect anime data via `ani.py` or APIs (e.g. Jikan).
- Encode metadata with SentenceTransformers.
- Use FAISS for nearest-neighbor search.
- Rank by hybrid score: 70% semantic similarity + 30% ratings.

## Tech stack

- Python 3.x
- SentenceTransformers (`all-mpnet-base-v2`)
- FAISS, pandas, NumPy
- BeautifulSoup4 (optional scraping)

### Example output

```
Recommendations for user 1:
- Fullmetal Alchemist: Brotherhood (Similarity: 0.85, Rating: 9.1)
- Steins;Gate (Similarity: 0.78, Rating: 9.1)
- Death Note (Similarity: 0.74, Rating: 8.6)
```

## Contributing

PRs welcome: add data sources, tune scoring, or build a web UI.

---

