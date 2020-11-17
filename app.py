# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sB2iyN6V-zEaTn__FghXMEcJ78SDi6T5

This is my code for the app. The model is my Boston Housing data model. To run that section, just uncomment the code there. To run dash, uncomment the jupyter_dash lines and comment out the dash.Dash line at the bottom. Since this is a jupyter notebook, you need to run jupyter dash. My app is available at
"""

import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo
from datetime import date
import dash
#from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#Model dependencies
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Commented out IPython magic to ensure Python compatibility.
# Python ≥3.5 is required
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

try:
    # %tensorflow_version only exists in Colab.
#     %tensorflow_version 2.x
    !pip install -q -U tfx==0.21.2
    print("You can safely ignore the package incompatibility errors.")
except Exception:
    pass

# TensorFlow ≥2.0 is required
import tensorflow as tf
from tensorflow import keras
assert tf.__version__ >= "2.0"

# Common imports
import numpy as np
import os
import pandas as pd 
# to make this notebook's output stable across runs
np.random.seed(49)
tf.random.set_seed(49)

'''from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

housing = load_boston()

X_train_full, X_test, y_train_full, y_test = train_test_split(
    housing.data, housing.target, test_size=.1, random_state=49)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full,test_size=.1, random_state=49)


scaler = StandardScaler()
scaler.fit(X_train)
X_mean = scaler.mean_
X_std = scaler.scale_
X_train.shape'''

'''def save_to_multiple_csv_files(data, name_prefix, header=None, n_parts=10):
    housing_dir = os.path.join("datasets", "housing")
    os.makedirs(housing_dir, exist_ok=True)
    path_format = os.path.join(housing_dir, "my_{}_{:02d}.csv")

    filepaths = []
    m = len(data)
    for file_idx, row_indices in enumerate(np.array_split(np.arange(m), n_parts)):
        part_csv = path_format.format(name_prefix, file_idx)
        filepaths.append(part_csv)
        with open(part_csv, "wt", encoding="utf-8") as f:
            if header is not None:
                f.write(header)
                f.write("\n")
            for row_idx in row_indices:
                f.write(",".join([repr(col) for col in data[row_idx]]))
                f.write("\n")
    return filepaths'''

'''train_data = np.c_[X_train, y_train]
valid_data = np.c_[X_valid, y_valid]
test_data = np.c_[X_test, y_test]
#header_cols = housing.feature_names + ["MedianHouseValue"]
header_cols = housing.feature_names
header = ",".join(header_cols)

train_filepaths = save_to_multiple_csv_files(train_data, "train", header, n_parts=20)
valid_filepaths = save_to_multiple_csv_files(valid_data, "valid", header, n_parts=10)
test_filepaths = save_to_multiple_csv_files(test_data, "test", header, n_parts=10)
header_cols
# train_data.shape'''

'''pd.read_csv(train_filepaths[0]).head(20)'''

'''X_train.shape[-1]'''

'''n_inputs = 13

@tf.function
def preprocess(line):
    defs = [0.] * n_inputs + [tf.constant([], dtype=tf.float32)]
    fields = tf.io.decode_csv(line, record_defaults=defs)
    x = tf.stack(fields[:-1])
    y = tf.stack(fields[-1:])
    return (x - X_mean) / X_std, y'''

'''def csv_reader_dataset(filepaths, repeat=1, n_readers=5,
                       n_read_threads=None, shuffle_buffer_size=10000,
                       n_parse_threads=5, batch_size=32):
    dataset = tf.data.Dataset.list_files(filepaths).repeat(repeat)
    dataset = dataset.interleave(
        lambda filepath: tf.data.TextLineDataset(filepath).skip(1),
        cycle_length=n_readers, num_parallel_calls=n_read_threads)
    dataset = dataset.shuffle(shuffle_buffer_size)
    dataset = dataset.map(preprocess, num_parallel_calls=n_parse_threads)
    dataset = dataset.batch(batch_size)
    return dataset.prefetch(1)'''

'''train_set = csv_reader_dataset(train_filepaths, repeat=None)
valid_set = csv_reader_dataset(valid_filepaths)
test_set = csv_reader_dataset(test_filepaths)'''

'''
keras.backend.clear_session()

model = keras.models.Sequential([
    keras.layers.Dense(100, activation="relu", input_shape=X_train.shape[1:]),
    keras.layers.Dense(50, activation="relu"),
    keras.layers.Dense(25, activation="relu"),
    keras.layers.Dense(1, activation="linear")


    
])
def rmse(y_true, y_pred):
        return K.sqrt(K.mean(K.square(y_pred - y_true))) 
model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=1e-3))
batch_size = 32
print (len(X_train))
model.fit(train_set, steps_per_epoch=len(X_train) // batch_size, epochs=100,
          validation_data=valid_set)
          '''

'''np.sqrt(model.evaluate(test_set, steps=len(X_test) // batch_size))'''

#model_version = "0001"
#model_name = "boston_model"
#model_path = os.path.join(model_name, model_version)
#model_path

#model.save('boston_model')

model = keras.models.load_model('boston_model')

input_data = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1]])

preds = model.predict(input_data)

print(preds)

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
#app = JupyterDash(__name__,external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1("Boston Housing Data price prediction Neural Net"),
    html.H3("Enter the CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT "),
    dcc.Markdown(''' Just type your desired value into each box and the model will calculate the predicted value
    The model is my model in the Boston Housing Data assignment. For an example, just input 1 into every box. All data must be positive numbers.'''),
    html.Div(["Input CRIM: ",
              dcc.Input(id='crim', value=1)]),
    html.Br(),
    html.Div(["Input ZN: ",
              dcc.Input(id='zn', value=1)]),
    html.Br(),
    html.Div(["Input INDUS: ",
              dcc.Input(id='indus', value=1)]),
    html.Br(),
    html.Div(["Input CHAS: ",
              dcc.Input(id='chas', value=1)]),
    html.Br(),
    html.Div(["Input NOX: ",
              dcc.Input(id='nox', value=1)]),
    html.Br(),
    html.Div(["Input RM: ",
              dcc.Input(id='rm', value=1)]),
    html.Br(),
    html.Div(["Input AGE: ",
              dcc.Input(id='age', value=1)]),
    html.Br(),
    html.Div(["Input DIS: ",
              dcc.Input(id='dis', value=1)]),
    html.Br(),
    html.Div(["Input RAD: ",
              dcc.Input(id='rad', value=1)]),
    html.Br(),
    html.Div(["Input TAX: ",
              dcc.Input(id='tax', value=1)]),
    html.Br(),
    html.Div(["Input PTRATIO: ",
              dcc.Input(id='ptratio', value=1)]),
    html.Br(),
    html.Div(["Input B: ",
              dcc.Input(id='b', value=1)]),
    html.Br(),
    html.Div(["Input LSAT: ",
              dcc.Input(id='lsat', value=1)]),
    html.Br(),

    html.Div(id='my-output'),


])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input('crim', 'value'),
     Input('zn', 'value'),
     Input('indus', 'value'),
     Input('chas', 'value'),
     Input('nox', 'value'),
     Input('rm', 'value'),
     Input('age', 'value'),
     Input('dis', 'value'),
     Input('rad', 'value'),
     Input('tax', 'value'),
     Input('ptratio', 'value'),
     Input('b', 'value'),
     Input('lsat', 'value'),])
def update_output_div(crim,zn,indus,chas,nox,rm,age,dis,rad,tax,ptratio,b,lsat):
    input_data = np.array([[crim,zn,indus,chas,nox,rm,age,dis,rad,tax,ptratio,b,lsat]])


    return 'Output: {}'.format(model.predict(input_data))


if __name__ == '__main__':
    app.run_server(debug=True)