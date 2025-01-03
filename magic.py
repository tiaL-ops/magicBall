from transformers import AutoModelForCausalLM, AutoTokenizer
import random

class MagicBallGPT2:
    def __init__(self):
        # Load the GPT-2 model and tokenizer
        self.model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Seed response to start off the response
        self.prompts = [
            "I'mma hold your hand when I tell this: ",
            "So, here is what I think: ",
            "I mean, there it is obvious that ",
            "Alright, hold on: ",
        ]
    
    def generate_response(self, user_question):
        
        prompt = random.choice(self.prompts) + user_question

        # Tokenize input and generate a response
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=50, 
            num_return_sequences=1,
            temperature=0.7,  #low = less randomness
            top_p=0.9,  # Nucleus sampling
            do_sample=True
        )

        # Decode and return the response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()
    
    def enter_input(self, label):
        return input(label)
    
    def main(self):
        print("Welcome to the AI-Powered Magic Ball!")
        print('Type "q" to quit.\n')
        
        while True:
            user_question = self.enter_input("Ask a question: ")
            if user_question.lower() == "q":
                print("Goodbye! May the AI's predictions guide you!")
                break
            
            print("\nShaking the AI-powered Magic Ball...\n")
            response = self.generate_response(user_question)
            print("Magic Ball says:", response)
            print()


if __name__ == "__main__":
    magic_ball = MagicBallGPT2()
    magic_ball.main()

