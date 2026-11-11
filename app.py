"""
Behavioral Bias Detector - Flask Web Application
Detects behavioral economics biases in any product's pricing structure
"""

from flask import Flask, render_template, request, jsonify
from bias_detector import BiasMatcher, EXAMPLES
import json

app = Flask(__name__)
matcher = BiasMatcher()


@app.route("/")
def index():
    """Render main page with examples"""
    return render_template("index.html", examples=list(EXAMPLES.keys()))


@app.route("/api/examples", methods=["GET"])
def get_examples():
    """Return all pre-loaded examples"""
    return jsonify(EXAMPLES)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Analyze pricing structure for behavioral biases.

    Expected JSON:
    {
        "product_name": "Product Name",
        "pricing_text": "Description of pricing..."
    }
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not isinstance(data.get("pricing_text"), str):
        return jsonify({"error": "pricing_text must be a string"}), 400

    product_name = data.get("product_name", "Unknown Product")
    pricing_text = data.get("pricing_text", "").strip()

    if not pricing_text:
        return jsonify({"error": "Pricing text cannot be empty"}), 400

    # Analyze pricing
    bias_scores, overall_score = matcher.analyze_pricing(pricing_text)

    # Format response
    result = {
        "product_name": product_name,
        "overall_score": round(overall_score, 1),
        "summary": matcher.get_summary(overall_score),
        "biases": [
            {
                "name": bias.name,
                "score": round(bias.score, 1),
                "confidence": round(bias.confidence, 2),
                "indicators": bias.indicators,
                "explanation": bias.explanation,
            }
            for bias in bias_scores
        ],
    }

    return jsonify(result)


@app.route("/api/example", methods=["POST"])
def load_example():
    """Load a pre-defined example"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("example_name"), str):
        return jsonify({"error": "example_name must be a string"}), 400
    example_name = data.get("example_name")

    if example_name not in EXAMPLES:
        return jsonify({"error": f"Unknown example: {example_name}"}), 404

    example = EXAMPLES[example_name]
    return jsonify(example)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
