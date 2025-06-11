from flask import Flask, request, jsonify
from rag import process_prompt

app = Flask(__name__)

@app.route('/api/rag', methods=['POST'])
def api_rag():
    data = request.get_json()
    prompt = data.get("prompt", "")
    try:
        response = process_prompt(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
