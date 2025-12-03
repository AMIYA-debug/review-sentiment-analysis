
set -o errexit

pip install -r requirements.txt


python -c "import nltk; nltk.download('stopwords', quiet=True)"
