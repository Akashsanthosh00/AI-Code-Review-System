import json
import pickle
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset.json"
MODEL_PATH = BASE_DIR / "explanation_model.pkl"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def prepare_training_data(data):
    input_texts = []
    output_texts = []

    for item in data:
        if "input_text" not in item or "output_text" not in item:
            continue

        input_text = str(item["input_text"]).strip()
        output_text = str(item["output_text"]).strip()

        if not input_text or not output_text:
            continue

        input_texts.append(input_text)
        output_texts.append(output_text)

    return input_texts, output_texts

def build_retrieval_index(input_texts, output_texts):
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    embeddings = model.encode(
        input_texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    retrieval_bundle = {
        "model_name": EMBEDDING_MODEL_NAME,
        "input_texts": input_texts,
        "output_texts": output_texts,
        "embeddings": embeddings
    }

    return retrieval_bundle

def save_model(retrieval_bundle):
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(retrieval_bundle, f)

def main():
    print("Loading dataset...")
    data = load_dataset()

    print("Preparing training data...")
    input_texts, output_texts = prepare_training_data(data)

    if not input_texts:
        raise ValueError("No valid training rows found in dataset.json")

    print(f"Building retrieval index for {len(input_texts)} examples...")
    retrieval_bundle = build_retrieval_index(input_texts, output_texts)

    print("Saving model...")
    save_model(retrieval_bundle)

    print(f"Retriever model saved successfully at: {MODEL_PATH}")

if __name__ == "__main__":
    main()