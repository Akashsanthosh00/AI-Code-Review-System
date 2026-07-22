from flask import Flask, render_template, request, jsonify
from web_review import analyze_code_to_text

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review_code():
    data = request.get_json()
    code = data.get("code", "")

    report = analyze_code_to_text(code)

    return jsonify({"report": report})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)