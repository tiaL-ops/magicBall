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