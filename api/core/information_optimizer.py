class InformationOptimizer:
    def __init__(self, sentences, questions, checkers):
        self.sentences = sentences
        self.checkers = checkers
        self.questions = questions
        self.s_score = self.calculate_s_score(sentences)

    def calculate_s_score(self, sentences):
        coefficients = []
        for checker in self.checkers:
            x = [result['answer'] for result in checker.check(''.join(sentences), self.questions)]
            coefficients.append(sum(x) / len(self.questions))
        return sum(coefficients) / len(self.checkers)

    def analyze(self):
        relevant_sentences = []
        not_relevant_indexes = set()
        for i, sentence in enumerate(self.sentences):
            #if self.calculate_s_score(self.get_relevant_sentences(not_relevant_indexes, i)) < self.s_score:
            if self.calculate_s_score(sentence) > 0:
                relevant_sentences.append(sentence)
            else:
                not_relevant_indexes.add(i)

        return relevant_sentences