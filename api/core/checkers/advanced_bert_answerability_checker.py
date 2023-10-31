import torch
from transformers import BertForQuestionAnswering, BertTokenizer

class AdvancedBertAnswerabilityChecker:
    def __init__(self):
        self.model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForQuestionAnswering.from_pretrained(self.model_name)

    def check(self, text, questions):
        results = []
        for question in questions:
            inputs = self.tokenizer.encode_plus(question, text, return_tensors="pt", max_length=512)
            input_ids = inputs["input_ids"].tolist()[0]

            outputs = self.model(**inputs)
            answer_start_scores = outputs.start_logits
            answer_end_scores = outputs.end_logits

            answer_start = torch.argmax(answer_start_scores)
            answer_end = torch.argmax(answer_end_scores) + 1

            confidence_threshold = 1
            if answer_start_scores.max() > confidence_threshold and answer_end_scores.max() > confidence_threshold:
                answer = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
                results.append({"question": question, "answer": True})
            else:
                results.append({"question": question, "answer": False})

        return results
