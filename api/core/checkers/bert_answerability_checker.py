import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

class BertAnswerabilityChecker:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
        self.model = AutoModelForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")

    def check(self, text, questions):
        answerabilities = []
        for question in questions:
            inputs = self.tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
            input_ids = inputs["input_ids"].tolist()[0]
            text_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)

            outputs = self.model(**inputs)
            answer_start_scores = outputs.start_logits
            answer_end_scores = outputs.end_logits

            answer_start_index = torch.argmax(answer_start_scores)
            answer_end_index = torch.argmax(answer_end_scores)

            answer = self.tokenizer.convert_tokens_to_string(text_tokens[answer_start_index:answer_end_index+1])

            answerabilities.append({
                "question": question,
                "answer": 1 if answer.strip() != '[CLS]' else 0
            })

        return answerabilities
