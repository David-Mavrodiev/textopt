from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

class CosineSimilarityAnswerChecker:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def get_embedding(self, text):
        return self.model.encode(text, convert_to_numpy=True)

    def compute_similarity_percentage(self, text, question):
        text_embedding = self.get_embedding(text)
        question_embedding = self.get_embedding(question)

        similarity = cosine_similarity([text_embedding], [question_embedding])[0][0]
        percentage = (similarity + 1) / 2
        return percentage

    def check(self, text, questions):
        results = []
        for question in questions:
            results.append({
                "question": question,
                "answer": self.compute_similarity_percentage(text, question) > 0.6
            })
        return results
