#importing libraries
import os
import numpy as np
import pandas as pd
import flask
import pickle
from flask import Flask, render_template, request

#creating instance of the class
application=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@application.route('/')
@application.route('/index')
def index():
    return flask.render_template('DiamondPrice.html')
    #return "Hello World"

#prediction function
def ValuePredictor(to_predict_df):
    loaded_model = pickle.load(open("model.pkl","rb"))
    result = loaded_model.predict(to_predict_df)
    return result[0]


@application.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        request_dict = request.form.to_dict()
        request_list=list(request_dict.values())
        to_predict_list = request_list
        to_predict_list[0] = float(request_list[0])
        to_predict_list[5] = float(request_list[5])
        to_predict_list[7] = float(request_list[7])
        to_predict_list[10] = float(request_list[10])
        to_predict_df = pd.DataFrame([to_predict_list], columns = ['carat','clarity','color','culet','cut','depth','fluorescence','lxwRatio','polish','symmetry','table'])
        result = ValuePredictor(to_predict_df)
        prediction= np.exp(result)
        return (render_template("result.html",prediction=prediction))
if __name__ == "__main__":
	application.run(debug=True)
