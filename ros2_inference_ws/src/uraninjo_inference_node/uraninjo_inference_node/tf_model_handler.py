import tensorflow as tf
from tensorflow.keras.models import load_model
class TFInference():
    def __init__(self, path):
        self.path = path
    def inference_generator(self, data):#TODO: Additional changes will be made later!
        model = load_model(self.path)
        data = tf.expand_dims(data, axis = 0)
        results = model.predict(data).tolist()
        metadata = dict()
        metadata["classification"] = results[0]
        if len(results)>1:
            metadata["detections"] = results[1]
        return metadata

#TODO: Eğer weight gönderilirse bir talimat ver.
