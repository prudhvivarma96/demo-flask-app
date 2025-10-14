from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<title>Vegetable Store (Demo)</title>
<h1>Welcome to Demo Vegetable Store</h1>
<p>API: <a href="/api/health">/api/health</a></p>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/api/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

