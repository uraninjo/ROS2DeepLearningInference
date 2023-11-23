import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

import sys
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String, Bool
import time

from .onnx_model_handler import OnnxInference
from .pytorch_model_handler import PytorchInference
from .tf_model_handler import TFInference


class InferenceNode(Node):
    def __init__(self):
        super().__init__("inference_node")

        self.declare_parameters(
            namespace="",
            parameters=[
                ("pytorch_inference_allowed", True),
                ("onnx_inference_allowed", True),
                ("tensorflow_inference_allowed", True),
                ("pytorch_model_path", None),
                ("onnx_model_path", None),
                ("tensorflow_model_path", None),
                ("pytorch_model_type", None),
                ("onnx_model_type", None),
                ("tensorflow_model_type", None),
            ],
        )

        # self.__goal_generator = self.__create_goal_generator()
        PYTORCH_BOOL = self.get_parameter("pytorch_inference_allowed").value
        ONNX_BOOL = self.get_parameter("onnx_inference_allowed").value
        TF_BOOL = self.get_parameter("tensorflow_inference_allowed").value

        PYTORCH_PATH = self.get_parameter("pytorch_model_path").value
        ONNX_PATH = self.get_parameter("onnx_model_path").value
        TF_PATH = self.get_parameter("tensorflow_model_path").value 
        
        PYTORCH_TYPE = self.get_parameter("pytorch_model_type").value
        ONNX_TYPE = self.get_parameter("onnx_model_type").value
        TF_TYPE = self.get_parameter("tensorflow_model_type").value 
        
        if PYTORCH_BOOL:
            self.torch_inference = PytorchInference(path=PYTORCH_PATH, model_type=PYTORCH_TYPE)
            self.torch_topic = self.create_publisher(Bool, '/pytorch_inference_result', 10)
            self.get_logger().info("PyTorch Node is activated!")
        
        if TF_BOOL:
            self.tf_inference = TFInference(path=TF_PATH, model_type=TF_TYPE)
            self.torch_topic = self.create_publisher(Bool, '/tensorflow_inference_result', 10)
            self.get_logger().info("Tensorflow Node is activated!")
        if ONNX_BOOL:
            self.onnx_inference = OnnxInference(path=ONNX_PATH, model_type=ONNX_TYPE)
            self.torch_topic = self.create_publisher(Bool, '/onnx_inference_result', 10)
            self.get_logger().info("ONNX Node is activated!")

    def main(self):
        


































        