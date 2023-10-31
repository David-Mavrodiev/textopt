import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

class SynonymWordCounterAnswerabilityChecker:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

    def preprocess(self, text):
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalnum() and word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        return set(words)

    def has_synonym_match(self, word1, word2):
        synsets1 = wordnet.synsets(word1)
        synsets2 = wordnet.synsets(word2)
        return any(s1 in synsets2 for s1 in synsets1)

    def count_matches(self, text_words, question):
        question_words = self.preprocess(question)

        exact_match_weight = 2.0
        synonym_match_weight = 1.0

        total_weights = 0
        match_score = 0

        for qw in question_words:
            if qw in text_words:
                match_score += exact_match_weight
                total_weights += exact_match_weight
            else:
                synonym_scores = [wordnet.wup_similarity(wordnet.synsets(qw)[0], tws) for tws in wordnet.synsets(qw) if any(tws in wordnet.synsets(tw) for tw in text_words)]
                if synonym_scores:
                    match_score += max(synonym_scores) * synonym_match_weight
                    total_weights += synonym_match_weight

        if total_weights == 0:
            return 0

        relevance_score = match_score / total_weights

        return relevance_score


    def check(self, text, questions):
        text_words = self.preprocess(text)
        results = []
        for question in questions:
            results.append({
                "question": question,
                "answer": self.count_matches(text_words, question) > 0.51
            })
        return results
