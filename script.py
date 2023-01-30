#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')

def index():
    return flask.render_template('index.html')

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, -1)
    loaded_model = pickle.load(open("checkpoints/modelo.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        #print(to_predict_list)
        try:
            to_predict_list = list(map(float, to_predict_list))
            result = ValuePredictor(to_predict_list)
            if int(result)==0:
                prediction='Derrota'
            elif int(result)==1:
                prediction='Victoria'
            else:
                prediction=f'{int(result)} No-definida'
        except ValueError as e:
            prediction= f'Error en el formato de los datos \n {e}'
        finally:
            print(f'\nEl resultado fue: {result}\n')

        return render_template("result.html", prediction=prediction)


if __name__=="__main__":

    app.run(port=5001)