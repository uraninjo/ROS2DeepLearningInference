import torch
import numpy as np
class PytorchInference:
    def __init__(self, path):
        self.path = path

    def inference_generator(self, data):#TODO: Additional changes will be made later!
        DEVICE = "cuda" if torch.cuda.is_available else "cpu"
        model = torch.load(self.path).to(DEVICE)
        data = np.transpose(data, (2, 0, 1))
        data = torch.tensor(data).unsqueeze(0).float().to(DEVICE)
        results = model(data)
        results = torch.Tensor.tolist(results)
        metadata = dict()
        metadata["classification"] = results[0]
        if len(results)>1:
            metadata["detections"] = results[1]
        return metadata

