import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "explanation_model.pkl"


class ExplanationRetriever:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.encoder = None
        self.embeddings = None
        self.output_texts = []

        try:
            self.encoder = SentenceTransformer(
                self.model_name,
                local_files_only=False   # change to True if model already exists locally
            )
        except Exception as e:
            print(f"[AI Warning] Could not load model '{self.model_name}': {e}")
            self.encoder = None

        self._load_retrieval_data()

    def _load_retrieval_data(self):
        if not MODEL_PATH.exists():
            print(f"[AI Warning] Retrieval model file not found: {MODEL_PATH}")
            self.embeddings = None
            self.output_texts = []
            return

        try:
            with open(MODEL_PATH, "rb") as f:
                data = pickle.load(f)

            self.embeddings = np.array(data.get("embeddings", []), dtype=np.float32)
            self.output_texts = data.get("output_texts", [])

            if len(self.output_texts) == 0 or self.embeddings.size == 0:
                print("[AI Warning] Retrieval data is empty or invalid.")
                self.embeddings = None
                self.output_texts = []

        except Exception as e:
            print(f"[AI Warning] Failed to load retrieval data: {e}")
            self.embeddings = None
            self.output_texts = []

    def _convert_rule_signals_to_text(self, rule_signals):
        parts = []
        for key, value in rule_signals.items():
            parts.append(f"{key}: {value}")
        return " | ".join(parts)

    def _retrieve_from_text(self, text):
        if self.encoder is None:
            print("[AI Warning] Encoder is not available.")
            return None

        if self.embeddings is None or len(self.output_texts) == 0:
            print("[AI Warning] Retrieval data is not available.")
            return None

        try:
            query_embedding = self.encoder.encode(
                [text],
                convert_to_numpy=True,
                normalize_embeddings=True
            )[0]

            scores = np.dot(self.embeddings, query_embedding)
            best_index = int(np.argmax(scores))

            return self.output_texts[best_index]

        except Exception as e:
            print(f"[AI Warning] Retrieval failed: {e}")
            return None

    def retrieve_best_explanation(self, rule_signals):
        query_text = self._convert_rule_signals_to_text(rule_signals)
        return self._retrieve_from_text(query_text)

    def retrieve(self, input_text):
        return self._retrieve_from_text(input_text)