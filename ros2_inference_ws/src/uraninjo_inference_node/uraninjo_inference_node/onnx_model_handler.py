import onnxruntime as rt
from onnxruntime.datasets import get_example
class ONNXInference:
    def __init__(self, path, model_type):
        self.path = path
        self.requsted_model_type = model_type

        model_types = {"classification": self.classification_inference(path=self.path),
                        "object_detection": self.object_detection_inference(path=self.path),
                        "classification_object_detection": self.combined_inference(path=self.path)}
        model_types[self.requsted_model_type]

    def classification_inference(self, path):#TODO: Additional changes will be made later!
        sess = rt.InferenceSession(path, providers=rt.get_available_providers())
        return sess

    def object_detection_inference(self, path):#TODO: Additional changes will be made later!
        model = rt.InferenceSession(path, providers=rt.get_available_providers())
        return model

    def combined_inference(self, path):#TODO: Additional changes will be made later!
        model = rt.InferenceSession(path, providers=rt.get_available_providers())
        return model



#res = sess.run([output_name], {input_name: x})
