# IMDb Review Sentiment Analyzer

A Flask web application that analyzes IMDb reviews and determines if they are positive or negative using a trained RNN model.

## Features

- **Real-time Sentiment Analysis** - Instantly determine if a review is positive or negative
- **Confidence Scoring** - Get a confidence percentage for the prediction
- **Rating Scale** - Convert sentiment to a 1-10 rating scale
- **Character Counter** - Real-time character count with 10,000 character limit
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile devices
- **Interactive Results** - Beautiful visualization of results with stars and confidence bars

## Project Structure

```
RNN/
├── app.py                 # Flask application
├── functions.py          # Text preprocessing functions
├── review.keras          # Trained RNN model
├── vocab.pkl            # Vocabulary dictionary
├── IMDB-Dataset.csv     # Dataset (optional)
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # HTML template
└── static/
    ├── style.css        # CSS styling
    └── script.js        # JavaScript functionality
```

## Installation

1. **Clone/Download the project** and navigate to the directory:

```bash
cd path/to/RNN
```

2. **Install dependencies** (make sure you have Python 3.8+ installed):

```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (required for stopwords):

```python
python -c "import nltk; nltk.download('stopwords')"
```

## Usage

1. **Run the Flask app**:

```bash
python app.py
```

2. **Open your browser** and navigate to:

```
http://localhost:5000
```

3. **Paste your review** in the textarea and click "Analyze Sentiment"

4. **View the results**:
   - Sentiment (Positive/Negative)
   - Confidence percentage
   - Rating out of 10
   - Visual star rating
   - Confidence bar visualization

## How It Works

1. **Text Preprocessing** (`functions.py`):

   - Converts text to lowercase
   - Removes HTML tags
   - Removes URLs and emails
   - Removes punctuation
   - Removes numbers
   - Removes stopwords
   - Tokenizes the text

2. **Vectorization**:

   - Uses TensorFlow's TextVectorization layer
   - Converts text to integer sequences
   - Uses a 10,000-word vocabulary
   - Standardizes sequence length to 200 tokens

3. **Model Prediction**:

   - Trained RNN model processes the vectorized input
   - Returns probability score between 0 and 1
   - Score ≥ 0.5 = Positive sentiment
   - Score < 0.5 = Negative sentiment

4. **Rating Conversion**:
   - Positive: rating = min(10, confidence × 2 × 10)
   - Negative: rating = max(1, (1 - confidence) × 10 - 3)
   - Displays as 1-10 scale with star visualization

## API Endpoint

### POST /predict

**Request:**

```json
{
  "review": "Your review text here..."
}
```

**Response (Success):**

```json
{
  "sentiment": "Positive",
  "confidence": 0.95,
  "rating": 9.5
}
```

**Response (Error):**

```json
{
  "error": "Review must be at least 10 characters long"
}
```

## Requirements

- Python 3.8+
- Flask 2.3.3
- TensorFlow 2.13.0
- NLTK 3.8.1
- Numpy 1.24.3
- Pandas 2.0.3

## Keyboard Shortcuts

- **Ctrl+Enter** (or **Cmd+Enter** on Mac) - Analyze review

## File Requirements

Make sure the following files are in the RNN directory:

- `review.keras` - Trained model file
- `vocab.pkl` - Vocabulary pickle file

## Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'flask'"**

- Solution: Run `pip install -r requirements.txt`

**Issue: "No such file or directory: 'vocab.pkl' or 'review.keras'"**

- Solution: Ensure these files are in the same directory as `app.py`

**Issue: NLTK stopwords not found**

- Solution: Run `python -c "import nltk; nltk.download('stopwords')"`

**Issue: Port 5000 already in use**

- Solution: Edit `app.py` and change the port number in the last line

## Customization

You can customize the styling by editing `static/style.css`:

- Change colors in the `:root` CSS variables
- Modify layout in media queries for different screen sizes
- Adjust typography and spacing


