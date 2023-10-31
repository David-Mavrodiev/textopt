from flask import Flask, request, jsonify
from core.information_optimizer import InformationOptimizer
from core.checkers.advanced_bert_answerability_checker import AdvancedBertAnswerabilityChecker
from core.checkers.synonym_word_counter_answerability_checker import SynonymWordCounterAnswerabilityChecker

advanced_bert_checker = AdvancedBertAnswerabilityChecker()
synonym_counter_checker = SynonymWordCounterAnswerabilityChecker()

checkers = [
    advanced_bert_checker
]

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sentences = data.get('sentences', [])
    questions = data.get('questions', [])

    return jsonify(InformationOptimizer(sentences, questions, checkers).analyze())

if __name__ == '__main__':
    app.run(debug=True)
