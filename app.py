from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from transformers import AutoModelForCausalLM, AutoTokenizer


app= Flask(__name__)

CORS(app)

class MagicBallGPT2:
    def __init__(self):
        self.model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.prompts = [
            "Answer this question with clarity and detail: ",
            "Here's a thoughtful response: ",
            "Provide a concise and relevant answer: ",
            "Think carefully and respond to this: ",
        ]
        self.context = (
            "You are an AI assistant that provides thoughtful and helpful answers to user questions. "
            "Your responses should be clear, concise, and relevant."
        )

    def adjust_parameters(self, user_question):
        if user_question.endswith("?"):
            return {"temperature": 0.3, "top_p": 0.8}
        else:
            return {"temperature": 0.9, "top_p": 0.95}

def generate_response(self, user_question):
    try:
        prompt = self.context + "\n" + random.choice(self.prompts) + user_question
        params = self.adjust_parameters(user_question)

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=min(len(user_question.split()) * 3, 100),  # Dynamic max_length
            temperature=params["temperature"],
            top_p=params["top_p"],
            do_sample=True,
            repetition_penalty=1.2,  
            num_return_sequences=3  
        )

        
        responses = [
            self.tokenizer.decode(output, skip_special_tokens=True)
            for output in outputs
        ]
        best_response = max(responses, key=lambda r: self.score_response(r, user_question))

        return best_response[len(prompt):].strip()
    except Exception as e:
        raise ValueError(f"Error generating response: {e}")

def score_response(self, response, user_question):
    # placeholder
    return len(response) - abs(len(response) - len(user_question))




magic_ball = MagicBallGPT2()



@app.route('/ask', methods=['POST'])
def ask():

    data=request.get_json()
    question= data.get("question", "").strip()

    if not question:
        return jsonify({"error":"no quetion provided"}),400
    

    answer = magic_ball.generate_response(question)

    return jsonify({"answer": answer})

@app.route('/test',methods=['GET'] )
def test():
    return jsonify({"test":"This is a test, it is working"})


if __name__ == '__main__':
    app.run(debug=True)