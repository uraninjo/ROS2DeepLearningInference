from tensorflow.keras.models import load_model
class TFInference:
    def __init__(self, path, model_type):
        self.path = path
        self.requsted_model_type = model_type

        model_types = {"classification": self.inference(path=self.path),
                        "object_detection": self.inference(path=self.path)}
        model_types[self.requsted_model_type]

    def inference(self, path):#TODO: Additional changes will be made later!
        model = load_model(path)
        return model

#TODO: Eğer weight gönderilirse bir talimat ver.



    