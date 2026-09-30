"""Serve the Emotion Detector interface and the course's analysis route."""

from flask import Flask, Response, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)
INVALID_TEXT = "Invalid input! Try again."


@app.get("/")
def index():
    """Render the accessible text-analysis interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Validate input and return the assignment's readable emotion summary."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return Response(INVALID_TEXT, status=400, mimetype="text/plain")

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        message = (
            "Emotion analysis is unavailable. The Watson service could not "
            "analyze this text. Please try again later."
        )
        return Response(message, status=503, mimetype="text/plain")

    message = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return Response(message, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
