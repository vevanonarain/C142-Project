from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

df=pd.read_csv("articles.csv")
df=df[df["soup"].notna()]

count=CountVectorizer(stop_words="english")
count_matrix=count.fit_transform(df["soup"])

cosine_sim2=cosine_similarity(count_matrix, count_matrix)
df=df.reset_index()
indices=pd.Series(df.index, index=df["original_title"])

def get_recommandations(title, cosine_sim):
  idx=indices[title]
  sim_scores=list(enumerate(cosine_sim[idx]))
  sim_scores=sorted(sim_scores, key=lambda x:x[1], reverse=True)
  sim_scores=sim_scores[1:11]
  article_indices=[i[0]for i in sim_scores]
  return df[["original_title", "poster_link", "vote_average", "release_date", "runtime", "overview"]].iloc[article_indices].values.tolist()