
import cPickle as pickle
import numpy as np
import tensorflow as tf
import random
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


valid_dataset=np.load('./data-processing/valdation_data.npy').astype(np.float32)
valid_reg=np.load('./data-processing/validation_reg.npy').astype(np.float32)
train_dataset=np.load('./data-processing/training_data.npy').astype(np.float32)
train_reg=np.load('./data-processing/training_reg.npy').astype(np.float32)


num_variables= train_dataset.shape[1]

depth1=16
depth2=16
depth3=16

graph = tf.Graph()

with graph.as_default():

  # Input data.
  tf_valid_dataset = tf.constant(valid_dataset)
  tf_train_dataset = tf.constant(train_dataset)
  
  tf_valid_reg = tf.constant(valid_reg)
  tf_train_reg = tf.constant(train_reg)
  
  
  
  #Fully connected layer weights
  layer1_weights = tf.Variable(tf.truncated_normal(
      [num_variables, depth1], mean=0.0, stddev=0.5))
  layer1_biases = tf.Variable(tf.constant(0.5, shape=[depth1]))
  layer2_weights = tf.Variable(tf.truncated_normal(
      [depth1, depth2], mean=0.0, stddev=0.5))
  layer2_biases = tf.Variable(tf.constant(0.5, shape=[depth2]))
  layer3_weights = tf.Variable(tf.truncated_normal(
      [depth2, depth3], mean=0.0, stddev=0.5))
  layer3_biases = tf.Variable(tf.constant(0.5, shape=[depth3]))

  
  reg_weights = tf.Variable(tf.truncated_normal(
      [depth3, 1], mean=0.0, stddev=0.1))
  reg_biases = tf.Variable(tf.constant(0.1, shape=[1]))  
 


   
  # Model.
  def model(data, keep_prob=1.0):

    # Construct a 2 layer Neural Net
    # Input size: batch x num_variables
    # 1st Layer : fully connected [num_variables, 16]
    # Relu
    # Dropout
    # 2nd Layer: fully connected [16, 16]
    # Relu
    # Dropout
    # 3rd Layer: fully connected [16, 16]
    # Relu
    # Dropout
        
    # Output layer, [16 1]
    
    layer1 = tf.matmul(data, layer1_weights)
    relu=tf.nn.relu(layer1 + layer1_biases)
    drop=tf.nn.dropout(relu, keep_prob)
    
    layer2 = tf.matmul(drop, layer2_weights)
    relu= tf.nn.relu(layer2 + layer2_biases)
    drop=tf.nn.dropout(relu, keep_prob)
    
    layer3 = tf.matmul(drop, layer3_weights)
    relu= tf.nn.relu(layer3 + layer3_biases)
    drop=tf.nn.dropout(relu, keep_prob)
        
    output = tf.matmul(relu, reg_weights + reg_biases)
    
    return output
  
  # Training computation.
  train_predictions = model(tf_train_dataset, 0.2)
  loss = tf.reduce_mean(tf.square((train_predictions - tf_train_reg)))

  # Optimizer.
  optimizer = tf.train.AdagradOptimizer(0.05).minimize(loss)
  
  #Validation Predictions
  valid_predictions = model(tf_valid_dataset)
  

num_steps = 3000

import time
start = time.time()  
with tf.device('/cpu:0'):
  with tf.Session(graph=graph) as session:
      
    saver = tf.train.Saver()
   # saver.restore(session, "tmp/saved_model_all_data2.ckpt")
    #print("Model restored.")  
    tf.global_variables_initializer().run()
    print('Initialized')


    max_acc = 0
    acc = 0
    step = 0
    for step in range(num_steps):
    #while max_acc - acc < 1.0 :
      _, l, predictions = session.run( [optimizer, loss, train_predictions])
      step += 1
      if (step % 100 == 0):
            print('Loss at step %d: %.2f' % (step, l))
            print('Training R^2-score: %.2f' %r2_score(train_reg, predictions))
            valid_preds=valid_predictions.eval()
            print('Validation R^2-score: %.2f' %r2_score(valid_reg, valid_preds))
         
    
    save_path = saver.save(session, "saved_model.ckpt") 
    print("Model saved in file: %s" % save_path)

