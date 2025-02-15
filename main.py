import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

anime_df = pd.read_csv('anime.csv')
anime_df['combined_text'] = anime_df['Anime_name'][0] + " " + anime_df['Characters'].fillna("") + " " + anime_df['Genres'].fillna("")

def load_data():
    model = SentenceTransformer('all-mpnet-base-v2')
    batch_size = 128
    anime_embeddings = []
    for i in range(0, len(anime_df), batch_size):
        batch = anime_df['combined_text'][i:i + batch_size].tolist()
        embeddings = model.encode(batch)
        anime_embeddings.extend(embeddings)
    anime_embeddings = np.array(anime_embeddings)

    d = anime_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(anime_embeddings)

    with open("anime_embeddings.pkl","wb") as f:
        pickle.dump(anime_embeddings,f)
    faiss.write_index(index, "anime_index.bin")

    print("Embeddings and index saved")

#retrieve data
with open("anime_embeddings.pkl","rb") as f:
    anime_embeddings = pickle.load(f)
index = faiss.read_index("anime_index.bin")

user_data = {1:{123:8,456:9,789:7},2:{987:6,654:8,321:9}}



def get_recommendations(user_id,k=5):
    if user_id not in user_data:
        return "Invalid User"
    watched_anime_ratings = user_data[user_id]
    if not watched_anime_ratings:
        return " user didnt watched any anime"

    watched_anime_ids = list(watched_anime_ratings.keys())
    
    try:
        user_watched_indices = anime_df[anime_df['No'].isin(watched_anime_ids)].index
    except KeyError:
        return "Invalid Anime Ids "
    
    if len(user_watched_indices) == 0:
        return "no anime found"
    user_watched_embeddings = anime_embeddings[user_watched_indices]

    ratings = np.array(list(watched_anime_ratings.values()))
    ratings = ratings / np.sum(ratings)

    if len(user_watched_embeddings.shape) == 1:
        query_embedding = user_watched_embeddings.reshape(1, -1) * ratings[0]
    else:
        query_embedding = np.average(user_watched_embeddings, axis=0, weights=ratings).reshape(1, -1)

    D, I = index.search(query_embedding,k=k*3)

    recommended_anime_indices = I[0]
    recommended_anime = anime_df.iloc[recommended_anime_indices].copy()

    min_rating = anime_df['Ratings'].min()
    max_rating = anime_df['Ratings'].max()
    recommended_anime['normalized_rating'] = (recommended_anime['Ratings'] - min_rating) / (max_rating - min_rating)
    recommended_anime['combined_score'] = (0.7 * (1 - D[0])) + (0.3 + recommended_anime['normalized_rating'])

    final_recommendations = recommended_anime.sort_values('combined_score', ascending = False).head(k)

    recommendations_output = f"Recommendations for user {user_id}:\n"
    for idx,row in final_recommendations.iterrows():
        similarity = 1 - D[0][list(final_recommendations.index).index(idx)]
        recommendations_output += f"- {row['Anime_name']} (Similarity: {similarity:.2f}, Avg.Rating : {row['Ratings']})\n"

    return recommendations_output

user_id = 1
recommendations = get_recommendations(user_id)
print(recommendations)