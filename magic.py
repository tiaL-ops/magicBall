from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import random

app = Flask(__name__)

class MagicBallGPT2:
    def __init__(self):
        self.model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.prompts = [
            "I'mma hold your hand when I tell this: ",
            "So, here is what I think: ",
            "I mean, there it is obvious that ",
            "Alright, hold on: ",
        ]
    
    def generate_response(self, user_question):
        prompt = random.choice(self.prompts) + user_question
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=50, 
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()

magic_ball = MagicBallGPT2()

@app.route('/ask', methods=['POST'])
def ask_magic_ball():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    response = magic_ball.generate_response(question)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
