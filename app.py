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
import pandas as pd
from matplotlib import pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
word_index = imdb.get_word_index()
app = Flask(__name__,template_folder='templates')
max_len = 50
max_words = 5000
model_final = load_model('setiment_model.h5')
df = pd.read_csv('sentiment.csv')
tokenizer = Tokenizer(num_words=max_words, lower=True, split=' ')
tokenizer.fit_on_texts(df['clean_comment'])
@app.route('/')
def hello_world():
    return render_template("sentiment.html")
@app.route('/predict',methods=['POST','GET'])
def predict():
     sentiment_classes = ['Negative', 'Neutral', 'Positive']
     features=[x for x in request.form.values()]
     xt = tokenizer.texts_to_sequences(features)
     xt = pad_sequences(xt, padding='post', maxlen=max_len)
     print(xt)
     yt = model_final.predict(xt).argmax(axis=1)
     print(yt)
     predicts = sentiment_classes[yt[0]]
     return render_template("sentiment.html", pred= predicts)

@app.route('/csv',methods=['POST',"GET"])
def getPage():
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    data = [request.form["myinput"]]
    r = data[0].split("\n")
    headers = r[0].split(',')
    print(r[101])
    objects = []
    for i in range(1,100):
          n = r[i].split(',')
          n = n[1:]
          object = {}
          for j in range(len(n)-1):
              object[headers[j]] = n[j]
          objects.append(object)
    print(objects)
    c = request.form["column"]
    print(c)
    sentences = []
    sentiments = []
    Predicts = []
    p = {}
    if c in headers:

        for i in range(len(objects)):
            content = objects[i][c]
            sentences.append([content])
            x = tokenizer.texts_to_sequences([content])
            x = pad_sequences(x, padding='post', maxlen=max_len)
            y = model_final.predict([x]).argmax(axis=1)
            print(y)
            predicts = sentiment_classes[y[0]]
            if predicts not in p:
                p[predicts] = 1
            p[predicts]+= 1
            Predicts.append(predicts)
        values = list(p.values())
        pos = '{:.2f}'.format((values[0] / len(Predicts)) * 100)
        neg = '{:.2f}'.format((values[1] / len(Predicts)) * 100)
        neu = '{:.2f}'.format((values[2] / len(Predicts)) * 100)
        print(len(Predicts))
        print(Predicts)
        print(p)
        final = f"Positive = {pos}%   Negative= {neg}%   Neutral = {neu}%"
        return render_template("sentiment.html", preds=final)
    return render_template("sentiment.html", preds="Invalid column name")

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)