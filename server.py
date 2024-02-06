import time

import flask
from flask import Flask, jsonify, request
import datetime
from flask_cors import CORS
import logging
import pandas as pd
import numpy as np
import os
from flask_sqlalchemy import SQLAlchemy

import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



x = datetime.datetime.now()
  
# Initializing flask app
app = Flask(__name__)

CORS(app)

handler = logging.FileHandler("test.log")  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)         # Set the log level to debug

base_name = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_name, 'test.db')
db = SQLAlchemy(app)



class JSONModelFile2(db.Model):
    __tablename__ = 'JSONModelFile2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_description = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(200), nullable=False)


class TrainingModel2(db.Model):
    __tablename__ = 'TrainingModel2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_description = db.Column(db.String(300), nullable=False)
    json_model_file_id = db.Column(db.Integer, db.ForeignKey('JSONModelFile2.id'))
    accuracy = db.Column(db.Float())  
    data_type = db.Column(db.String(100))  
    strategy = db.Column(db.String(100))  
    time_step = db.Column(db.Integer) 

    json_model = db.relationship("JSONModelFile2", backref="TrainingModel2")

with app.app_context():
    db.create_all()


class Prediction:
  def __init__(self, id, disease, percentage):
    self.id = id
    self.desease = disease
    self.percentage = percentage  
  
#Route for seeing a data
@app.route('/')
def get_models():
    models_list = TrainingModel2.query.all()
    dict_list = []
    for model in models_list:
        needed_dict = model.__dict__
        print(needed_dict)
        needed_dict.pop('_sa_instance_state')
        json_model = db.session.query(JSONModelFile2).filter(JSONModelFile2.id == model.json_model_file_id).one()
        json_model_dict = json_model.__dict__
        json_model_dict.pop('_sa_instance_state')
        needed_dict["json_model"] = json_model_dict
        dict_list.append(needed_dict)


    response = jsonify(dict_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




@app.route('/create', methods=['GET', 'POST'])
def createModel():
    if flask.request.method == 'GET':
        models_list = JSONModelFile2.query.all()
        dict_list = []
        # for model in models_list:
        #     needed_dict = model.__dict__
        #     #needed_dict.pop('_sa_instance_state')
        #     dict_list.append(needed_dict)

        response = jsonify(dict_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        print(request)
        name = request.form.get('model_name')
        description = request.form.get('model_description')
        accuracy = request.form.get('accuracy')  
        data_type = request.form.get('data_type')  
        strategy = request.form.get('strategy') 
        time_step = request.form.get('time_step')  
        model_json_name = request.form.get('json_name') 

        model_jsonF = request.files['json_model']
        model_jsonF.save(os.path.join(app.root_path, 'static', 'jsons', "model_json"))
        new_model_json = JSONModelFile2(model_name=model_json_name, model_description="model_json_descr",
                                        link="link")

        try:
            db.session.add(new_model_json)
            db.session.commit()

            app.logger.error("json " + str(new_model_json))
        except Exception as e:
            app.logger.error(e)

        json_id = new_model_json.id

        new_model = TrainingModel2(model_name=name, model_description=description,
                                   json_model_file_id=json_id,
                                   accuracy=float(accuracy) if accuracy else None,  # Convert to float
                                   data_type=data_type,
                                   strategy=strategy,
                                   time_step=int(time_step) if time_step else None)  # Convert to int

        try:
            db.session.add(new_model)
            db.session.commit()

            app.logger.error("json " + str(new_model))
            return 'Done', 201
        except Exception as e:
            app.logger.error(e)
            return 'There was an issue adding the model'
  

@app.route('/predict/', methods=['POST'])
def predictModel():
    id = request.form.get('id')
    currency = request.form.get('currency')  
    period_str = request.form.get('period')  
    num_days = int(request.form.get('period'))
    
    plt.figure(figsize=(8, 9))
    plt.plot(days, prices)  # Update this line to plot days and prices
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.title('Price Trend Over Time')
    plt.xticks(rotation=45)

    # The rest of your code remains the same for generating and sending the plot
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.read()).decode()
    buf.close()

    response = jsonify({'plot_url': plot_url})
    response.headers.add('Access-Control-Allow-Origin', '*')
    time.sleep(4)
    return response

@app.route('/predict/<id>', methods=['GET'])
def predict_model_from_id(id):

    app.logger.error("get" + str(request.args.get('id')))
    return {request.args.get('id')}


@app.route('/get-plot')
def get_plot():
    # Create a plot
    plt.figure()
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Simple Plot')

    # Save it to a temporary buffer.
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the plot in base64 and decode it to a string to be transmitted
    plot_url = base64.b64encode(buf.read()).decode()

    # Ensure the buffer is closed
    buf.close()

    return jsonify({'plot_url': plot_url})

      
# Running app
if __name__ == '__main__':
    os.environ["FLASK_APP"] = "server.py"  
    app.run(host="0.0.0.0", debug=True)