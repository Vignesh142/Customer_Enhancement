# app.py
from flask import Flask, request, jsonify
from faq_bot import answer_customer_query, classify_and_log_query, summarize_and_log_query

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    try:
        # Get the customer query from the request
        data = request.json
        query = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        # Get the response from the FAQ bot
        response = answer_customer_query(query, api_key=api_key)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/classify", methods=["POST"])
def classify():
    try:
        # Get the customer query from the request
        data = request.json
        query = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        if not api_key:
            return jsonify({"error": "API key is required for classification."}), 400
        
        # Classify the query and save it to the log file
        category = classify_and_log_query(query, api_key)

        return jsonify({"category": category})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        # Get the customer query from the request
        data = request.json
        query = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        if not api_key:
            return jsonify({"error": "API key is required for summarization."}), 400
        
        # Summarize the query and save it to the log file
        summary = summarize_and_log_query(query, api_key)

        return jsonify({"query": query, "summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Hello Varun!"

if __name__ == "__main__":
    app.run(debug=True)
