"""
A Flask web application for NLP emotion detection.
"""
from flask import Flask, request, jsonify, render_template
import json
import requests

app = Flask(__name__)

def emotion_detector(text_to_analyse):
    """
    Detects emotions in the given text.

    Args:
        text_to_analyse (str): The text to analyze.

    Returns:
        dict: A dictionary with emotion scores and the dominant emotion, or an error message.
    """
    if not text_to_analyse.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=myobj, headers=header)

    if response.status_code == 200:
        formatted_response = json.loads(response.text)

        if formatted_response.get('emotionPredictions'):
            emotions = formatted_response['emotionPredictions'][0].get('emotion', {})

            anger_score = emotions.get('anger', 0.0)
            disgust_score = emotions.get('disgust', 0.0)
            fear_score = emotions.get('fear', 0.0)
            joy_score = emotions.get('joy', 0.0)
            sadness_score = emotions.get('sadness', 0.0)

            emotion_scores = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score
            }

            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            output = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': dominant_emotion
            }

            return output

        return {'error': "No emotion predictions found in the response"}

    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    return {'error': f"Failed to get a response, status code: {response.status_code}"}


@app.route('/')
def index():
    """
    Renders the index page.

    Returns:
        str: The rendered HTML of the index page.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    """
    Detects emotions for the provided text.

    Returns:
        str: The response text with emotion scores or an error message.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return jsonify({'error': 'No text provided for analysis'}), 400

    result = emotion_detector(text_to_analyze)

    if result.get('dominant_emotion') is None:
        response_text = "Invalid text! Please try again."
    elif 'error' in result:
        response_text = result['error']
    else:
        response_text = (
            f"For the given statement, the system response is 'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, 'fear': {result['fear']}, 'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
        )

    return response_text


if __name__ == '__main__':
    app.run(host='localhost', port=5000)