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
        print(sentences)
        print(coefficients)
        print(sum(coefficients) / len(self.checkers))
        print("\n")
        return sum(coefficients) / len(self.checkers)

    def get_relevant_sentences(self, not_relevant_indexes, current_index):
        sentences = []
        for index, sentence in enumerate(self.sentences):
            if not index in not_relevant_indexes and current_index != index:
                sentences.append(sentence)
        return sentences

    def analyze(self):
        relevant_sentences = []
        not_relevant_indexes = set()
        for i, sentence in enumerate(self.sentences):
            if self.calculate_s_score(self.get_relevant_sentences(not_relevant_indexes, i)) < self.s_score:
                relevant_sentences.append(sentence)
            else:
                not_relevant_indexes.add(i)

        return relevant_sentences