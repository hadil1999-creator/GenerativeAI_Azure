import os
import pandas as pd
import numpy as np
import openai
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API credentials and configuration
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY2")
openai.api_version = os.getenv("OPENAI_API_VERSION")
# Ensure the environment variable is correctly set
os.environ["AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT"] = "text-embedding-ada-002"

# Retrieve the deployment name from the environment variable
model = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")

SIMILARITIES_RESULTS_THRESHOLD = 0.75
DATASET_NAME = "C:/Users/21629/Desktop/GenAI/embedding_index_3m.json"

def load_dataset(source: str) -> pd.core.frame.DataFrame:
    # Load the video session index
    pd_vectors = pd.read_json(source)
    return pd_vectors.drop(columns=["text"], errors="ignore").fillna("")

def cosine_similarity(a, b):
    if len(a) > len(b):
        b = np.pad(b, (0, len(a) - len(b)), 'constant')
    elif len(b) > len(a):
        a = np.pad(a, (0, len(b) - len(a)), 'constant')
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_videos(
    query: str, dataset: pd.core.frame.DataFrame, rows: int
) -> pd.core.frame.DataFrame:
    # create a copy of the dataset
    video_vectors = dataset.copy()

    # get the embeddings for the query    
    query_embeddings = openai.Embedding.create(
    input=query,
    engine=model).data[0].embedding

    # create a new column with the calculated similarity for each row
    video_vectors["similarity"] = video_vectors["ada_v2"].apply(
        lambda x: cosine_similarity(np.array(query_embeddings), np.array(x))
    )

    # filter the videos by similarity
    mask = video_vectors["similarity"] >= SIMILARITIES_RESULTS_THRESHOLD
    video_vectors = video_vectors[mask].copy()

    # sort the videos by similarity
    video_vectors = video_vectors.sort_values(by="similarity", ascending=False).head(
        rows
    )

    # return the top rows
    return video_vectors.head(rows)


def display_results(videos: pd.core.frame.DataFrame, query: str):
    def _gen_yt_url(video_id: str, seconds: int) -> str:
        """convert time in format 00:00:00 to seconds"""
        return f"https://youtu.be/{video_id}?t={seconds}"

    print(f"\nVideos similar to '{query}':")
    for _, row in videos.iterrows():
        youtube_url = _gen_yt_url(row["videoId"], row["seconds"])
        print(f" - {row['title']}")
        print(f"   Summary: {' '.join(row['summary'].split()[:15])}...")
        print(f"   YouTube: {youtube_url}")
        print(f"   Similarity: {row['similarity']}")
        print(f"   Speakers: {row['speaker']}")
        
        
pd_vectors = load_dataset(DATASET_NAME)

# get user query from imput
while True:
    query = input("Enter a query: ")
    if query == "exit":
        break
    videos = get_videos(query, pd_vectors, 5)
    display_results(videos, query)        