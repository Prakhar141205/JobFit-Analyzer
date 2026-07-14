import os
from sentence_transformers import SentenceTransformer
import streamlit as st

MODEL_PATH = os.path.join("models", "embedding_model")


@st.cache_resource
def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            model = SentenceTransformer(MODEL_PATH)
        else:
            model = SentenceTransformer("all-MiniLM-L6-v2")
            model.save(MODEL_PATH)

        return model

    except Exception as e:
        raise RuntimeError("Unable to load the model") from e


# get embedding

def get_embedding(text):
    try:
        model = load_model()
        embedding = model.encode(text)

        return embedding
    except Exception as e:
        raise RuntimeError(f"{e} occurred") from e
