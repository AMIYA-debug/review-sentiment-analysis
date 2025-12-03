import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
import string
import tensorflow as tf
import pickle

vocabulary= pickle.load(open("vocab.pkl","rb"))

stop_words=set(stopwords.words('english'))
def clean_text(text):
    text = text.lower()

    
    text=re.sub(r"<.*?>", " ", text)

    
    text=re.sub(r"http\S+|www\S+", " ", text)

    
    text=re.sub(r"\S+@\S+", " ", text)

    
    text=re.sub(f"[{re.escape(string.punctuation)}]", " ", text)

    
    text=re.sub(r"\d+", " ", text)

    
    text=re.sub(r"\s+", " ", text).strip()

    
    words=[word for word in text.split() if word not in stop_words]
    text= " ".join(words)

    return text

tokenizer=tf.keras.layers.TextVectorization(
    max_tokens=10000,
    output_mode='int',
    output_sequence_length=200,
    vocabulary=vocabulary
    
)
model=tf.keras.models.load_model("review.keras")
snentence="This movie was fantastic! I loved it."
cleaned_sentence=clean_text(snentence)
input_data=tf.constant([cleaned_sentence])
vectorized_input=tokenizer(input_data)
prediction=model.predict(vectorized_input)
if prediction>=0.5:
    sentiment="Positive"
else:
    sentiment="Negative"

print(f"Sentiment: {sentiment} (Confidence: {prediction[0][0]:.2f})")        




