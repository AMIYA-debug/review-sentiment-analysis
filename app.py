import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  

from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import threading
import nltk

# Download NLTK data on startup
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords', quiet=True)

from functions import clean_text

app = Flask(__name__)


_model = None
_tokenizer = None
_model_lock = threading.Lock()

def get_model():
    """Lazy load the model on first use"""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                print("Loading model...")
                _model = tf.keras.models.load_model("review.keras")
                print("Model loaded successfully")
    return _model

def get_tokenizer():
    """Lazy load the tokenizer on first use"""
    global _tokenizer
    if _tokenizer is None:
        with _model_lock:
            if _tokenizer is None:
                print("Loading tokenizer...")
                import pickle
                vocabulary = pickle.load(open("vocab.pkl", "rb"))
                _tokenizer = tf.keras.layers.TextVectorization(
                    max_tokens=10000,
                    output_mode='int',
                    output_sequence_length=200,
                    vocabulary=vocabulary
                )
                print("Tokenizer loaded successfully")
    return _tokenizer

def predict_sentiment(review_text):
    """
    Predict sentiment for a given review text
    """
    try:
        cleaned_text = clean_text(review_text)
        input_data = tf.constant([cleaned_text])
        tokenizer = get_tokenizer()
        model = get_model()
        vectorized_input = tokenizer(input_data)
        prediction = model.predict(vectorized_input, verbose=0)
        confidence = float(prediction[0][0])
        
        if confidence >= 0.5:
            sentiment = "Positive"
            rating = min(10, int((confidence * 2) * 10) / 10)
        else:
            sentiment = "Negative"
            rating = max(1, int((1 - confidence) * 10 - 3))
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "rating": round(rating, 1)
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    review_text = data.get('review', '').strip()
    
    if not review_text or len(review_text) < 10:
        return jsonify({"error": "Review must be at least 10 characters long"}), 400
    
    result = predict_sentiment(review_text)
    
    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

