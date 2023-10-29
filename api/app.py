from flask import Flask, request, jsonify
from core.information_optimizer import InformationOptimizer
from core.checkers.simple_answerability_checker import SimpleAnswerabilityChecker
from core.checkers.synonym_word_counter_answer_checker import SynonymWordCounterAnswerChecker
from core.checkers.cosine_similarity_answer_checker import CosineSimilarityAnswerChecker
from core.checkers.bert_answerability_checker import BertAnswerabilityChecker

checker = SimpleAnswerabilityChecker()

bert_answer_checker = BertAnswerabilityChecker()
cosine_similarity_answer_checker = CosineSimilarityAnswerChecker()
synonym_word_counter_answer_checker = SynonymWordCounterAnswerChecker()

checkers = [
    checker
]

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input text from the POST request
    data = request.get_json()
    sentences = data.get('sentences', [])
    questions = data.get('questions', [])

    return jsonify(InformationOptimizer(sentences, questions, checkers).analyze())

if __name__ == '__main__':
    app.run(debug=True)
