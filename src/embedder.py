import os
from sentence_transformers import SentenceTransformer

MODEL_PATH = os.path.join("models", "embedding_model")


def load_model():

    try:
        if os.path.exists(MODEL_PATH):
            model = SentenceTransformer(MODEL_PATH)
            print(f"Model Loaded!")
        else:
            model = SentenceTransformer("all-MiniLM-L6-v2")
            model.save(MODEL_PATH)
            print("Model Saving done.")

        return model

    except Exception as e:
        raise RuntimeError("Unable to load the model") from e
    

## initialize the model

model = load_model()


# get embedding

def get_embedding(text):
    try:
        embedding = model.encode(text)

        return embedding
    except Exception as e:
        raise RuntimeError(f"{e} occurred") from e
