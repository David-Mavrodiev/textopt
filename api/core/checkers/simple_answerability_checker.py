import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

class SimpleAnswerabilityChecker:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

    def preprocess(self, text):
        # Tokenize the text
        words = word_tokenize(text.lower())

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalnum() and word not in stop_words]

        # Perform Lemmatization
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]

        return set(words)

    def simple_ner_and_score(self, text):
        words_with_scores = {}
        sentences = sent_tokenize(text)

        for sentence in sentences:
            words = word_tokenize(sentence)
            tagged_words = pos_tag(words)  # Perform POS tagging

            for word, tag in tagged_words:
                if word.isalnum():
                    # Assign higher scores to proper nouns
                    score = 2 if 'NNP' in tag else 1
                    words_with_scores[word.lower()] = score

        return words_with_scores

    def check(self, text, questions):
        answerabilities = []
        for question in questions:
            question_words = self.preprocess(question)

            # Perform simple NER and score words in text
            text_words_with_scores = self.simple_ner_and_score(text)

            # Count the scores of question keywords found in the text
            matching_score = sum(text_words_with_scores.get(word, 0) for word in question_words)

            # Decide if the text potentially contains enough information to answer the question
            can_answer = matching_score >= len(question_words)

            answerabilities.append({
                "question": question,
                "answer": can_answer
            })

        return answerabilities
