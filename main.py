from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.datasets import imdb
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
word_index = imdb.get_word_index()
app = Flask(__name__,template_folder='templates')
max_len = 250
model_final = load_model('setiment_model.h5')
@app.route('/')
def hello_world():
    return render_template("sentiment.html")
@app.route('/predict',methods=['POST','GET'])
def predict():
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    max_len = 50
    max_words = 5000
    features=[x for x in request.form.values()]
    tokenizer = Tokenizer(num_words=max_words, lower=True, split=' ')
    tokenizer.fit_on_texts(features[0])
    sequences = tokenizer.texts_to_sequences(["amazing"])
    print(sequences)
    xt = tokenizer.texts_to_sequences(features[0])
    print(xt)
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    yt = model_final.predict(xt).argmax(axis=1)
    predicts = sentiment_classes[yt[0]]
    print(features[0])
    print(xt)
    print(predicts)
    return render_template("sentiment.html", pred= predicts)
if __name__ == '__main__':
    app.run(debug=True)