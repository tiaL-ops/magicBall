from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app= Flask(__name__)

CORS(app)

#testing purpose
MAGIC_BALL_ANSWER=[
    "Are u okay,",
    "no",
    "Bro",
    "Yes",
    "Ofc!!",
    "hie"
]


@app.route('/ask', methods=['POST'])
def ask():

    data=request.get_json()
    question= data.get("question", "").strip()

    if not question:
        return jsonify({"error":"no quetion provided"}),400
    

    answer=random.choice(MAGIC_BALL_ANSWER)

    return jsonify({"answer": answer})

@app.route('/test',methods=['GET'] )
def test():
    return jsonify({"test":"This is a test, it is working"})


if __name__ == '__main__':
    app.run(debug=True)