import llm
from transformers import AutoModel

MAX_LENGTH = 8192


@llm.hookimpl
def register_embedding_models(register):
    pass
    for model_id in (
        "hazo",
    ):
        register(HazoEmbeddingModel(model_id))


class HazoEmbeddingModel(llm.EmbeddingModel):
    def __init__(self, model_id):
        self.model_id = model_id
        self._model = None
        self.embedded_content = []

    def embed_batch(self, texts):
        if not hasattr(self, "batch_count"):
            self.batch_count = 0
        self.batch_count += 1
        for text in texts:
            self.embedded_content.append(text)
            words = text.split()[:16]
            embedding = [len(word) * 1.0 for word in words]
            # Pad with 0 up to 16 words
            embedding += [0.0] * (16 - len(embedding))
            yield embedding
