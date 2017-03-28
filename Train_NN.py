


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
depth2=32
depth3=64
depth4=32
depth5=16


graph = tf.Graph()

with graph.as_default():

  # Input data.
  tf_valid_dataset = tf.constant(valid_dataset)
  tf_train_dataset = tf.constant(train_dataset)
  
  tf_valid_reg = tf.constant(valid_reg)
  tf_train_reg = tf.constant(train_reg)
  
  


  
  #Fully connected layer weights
  layer1_weights = tf.Variable(tf.truncated_normal(
      [num_variables, depth1], mean=0.0, stddev=0.1))
  
  layer1_biases = tf.Variable(tf.constant(0.1, shape=[depth1]))
  
  layer2_weights = tf.Variable(tf.truncated_normal(
      [depth1, depth2], mean=0.0, stddev=0.1))
  
  layer2_biases = tf.Variable(tf.constant(0.1, shape=[depth2]))
  
  layer3_weights = tf.Variable(tf.truncated_normal(
      [depth2, depth3], mean=0.0, stddev=0.1))
  
  layer3_biases = tf.Variable(tf.constant(0.1, shape=[depth3]))

  layer4_weights = tf.Variable(tf.truncated_normal(
      [depth3, depth4], mean=0.0, stddev=0.1))
  
  layer4_biases = tf.Variable(tf.constant(0.1, shape=[depth4]))  
  
  layer5_weights = tf.Variable(tf.truncated_normal(
      [depth4, depth5], mean=0.0, stddev=0.1))
  
  layer5_biases = tf.Variable(tf.constant(0.1, shape=[depth5]))  


  
  reg_weights = tf.Variable(tf.truncated_normal(
      [depth5, 1], mean=0.0, stddev=0.1))
  reg_biases = tf.Variable(tf.constant(0.1, shape=[1]))  
 


   
  # Model.
  def model(data, drop_rate=1.0):

    # Construct a 2 layer Neural Net
    # Input size: batch x num_variables
    # 1st Layer : fully connected [num_variables, 16]
    # Relu
    # 2nd Layer: fully connected [16, 32]
    # Relu
    
    # Output layer, [32 1]
    
    layer1 = tf.matmul(data, layer1_weights)
    relu=tf.nn.relu(layer1 + layer1_biases)
    layer2 = tf.matmul(relu, layer2_weights)
    relu= tf.nn.relu(layer2 + layer2_biases)
    layer3 = tf.matmul(relu, layer3_weights)
    relu= tf.nn.relu(layer3 + layer3_biases)
    layer4 = tf.matmul(relu, layer4_weights)
    relu= tf.nn.relu(layer4 + layer4_biases)
    layer5 = tf.matmul(relu, layer5_weights)
    relu= tf.nn.relu(layer5 + layer5_biases)

    
    output = tf.matmul(relu, reg_weights + reg_biases)
    
    return output
  
  # Training computation.
  train_predictions = model(tf_train_dataset, 1.0)
  loss = tf.reduce_mean(tf.square((train_predictions - tf_train_reg)))

  # Optimizer.
  optimizer = tf.train.AdagradOptimizer(0.025).minimize(loss)
  
  #global_step = tf.Variable(0)
  #learning_rate = tf.train.exponential_decay(0.05, global_step, 2000, 0.95)
  #optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(loss, global_step=global_step)
  
  
  #Validation Predictions
  valid_predictions = model(tf_valid_dataset)
  


    
    


num_steps = 10000

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
      if (step % 500 == 0):
            print('Loss at step %d: %f' % (step, l))
            print('Training R^2-score: %.1f%%' %r2_score(train_reg, predictions))
            print('Validation R^2-score: %.1f%%' %r2_score(valid_reg, valid_predictions.eval()))
         
    

    save_path = saver.save(session, "saved_model.ckpt") 
    print("Model saved in file: %s" % save_path)

