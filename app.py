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
     yt = model_final.predict(xt).argmax(axis=1)
     predicts = sentiment_classes[yt[0]]
     return render_template("sentiment.html", pred= predicts)

@app.route('/csv',methods=['POST',"GET"])
def getPage():
     sentiment_classes = ['Negative', 'Neutral', 'Positive']
     data = request.form["myinput"]
     r = data.split("\n")
     headers = r[0].split(',')
     objects = []
     for i in range(1,1000):
           n = r[i].split(',')
           object = {}
           for j in range(len(n)-1):
               object[headers[j]] = n[j]
           objects.append(object)

     c = request.form["column"]
     sentences = []
     sentiments = []
     Predicts = []
     p = {}
     if c in headers:

         for i in range(len(objects)):
             if c in objects[i]:
                 content = objects[i][c]
                 sentences.append(content)
         x = tokenizer.texts_to_sequences(sentences)
         x = pad_sequences(x, padding='post', maxlen=max_len)
         y = model_final.predict([x]).argmax(axis=1)
         p = []
         for i in y:
             l = sentiment_classes[i]
             p.append(l)
         pos = round(((p.count("Positive")/len(sentences))*100),3)
         neg=  round(((p.count("Negative")/len(sentences))*100),3)
         neu = round(((p.count("Neutral")/len(sentences))*100),3)
         final = f"Positive = {pos}%   Negative= {neg}%   Neutral = {neu}%"
         return render_template("sentiment.html", preds=final)
     return render_template("sentiment.html", preds="Invalid column name")

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)