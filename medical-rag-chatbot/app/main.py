from flask import Flask, request, jsonify
from retriever.retriever import get_answer

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    answer = get_answer(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
