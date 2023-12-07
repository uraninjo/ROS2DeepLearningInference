import torch
class PytorchInference:
    def __init__(self, path, model_type):
        self.path = path
        self.requsted_model_type = model_type

        model_types = {"classification": self.classification_inference(path=self.path),
                        "object_detection": self.object_detection_inference(path=self.path),
                        "classification_object_detection": self.combined_inference(path=self.path)}
        model_types[self.requsted_model_type]

    def classification_inference(self, path):#TODO: Additional changes will be made later!
        model = torch.load(path)
        return model

    def object_detection_inference(self, path):#TODO: Additional changes will be made later!
        model = torch.load(path)
        return model

    def combined_inference(self, path):#TODO: Additional changes will be made later!
        model = torch.load(path)
        return model



# vgg = VGG16(include_top=False)(input_layer)

#     # Classification Model  
#     f1 = GlobalMaxPooling2D()(vgg)
#     class1 = Dense(2048, activation='relu')(f1)
#     class2 = Dense(1, activation='sigmoid')(class1)
    
#     # Bounding box model
#     f2 = GlobalMaxPooling2D()(vgg)
#     regress1 = Dense(2048, activation='relu')(f2)
#     regress2 = Dense(4, activation='sigmoid')(regress1)
    