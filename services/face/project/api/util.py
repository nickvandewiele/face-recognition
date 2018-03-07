
import tensorflow as tf
import numpy as np
import os
import cv2

from .inception_blocks_v2 import faceRecoModel
from .fr_utils import load_weights_from_FaceNet

graph = None

def load_model():
    global graph

    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    print("Total Params:", FRmodel.count_params())

    load_weights_from_FaceNet(FRmodel)

    # save the graph in a global variable, for re-use in other threads.
    graph = tf.get_default_graph()

    return FRmodel

def img_to_encoding(image_path, model):
    img1 = cv2.imread(image_path, 1)
    return img_to_encoding2(img1, model)

def img_to_encoding2(image, model):
    img1 = image
    img = img1[...,::-1]
    img = np.around(np.transpose(img, (2,0,1))/255.0, decimals=12)
    x_train = np.array([img])

    # make use of the global graph, this function may be called from other threads.
    global graph
    with graph.as_default():
      embedding = model.predict_on_batch(x_train)
      return embedding