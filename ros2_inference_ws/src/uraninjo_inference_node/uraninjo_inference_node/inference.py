import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

import sys
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import time
import json

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

                ("camera_stream_topic", None),
            ],
        )

        self.bridge = CvBridge()

        self.PYTORCH_BOOL = self.get_parameter("pytorch_inference_allowed").value
        self.ONNX_BOOL = self.get_parameter("onnx_inference_allowed").value
        self.TF_BOOL = self.get_parameter("tensorflow_inference_allowed").value

        PYTORCH_PATH = self.get_parameter("pytorch_model_path").value
        ONNX_PATH = self.get_parameter("onnx_model_path").value
        TF_PATH = self.get_parameter("tensorflow_model_path").value 
        
        PYTORCH_TYPE = self.get_parameter("pytorch_model_type").value
        ONNX_TYPE = self.get_parameter("onnx_model_type").value
        TF_TYPE = self.get_parameter("tensorflow_model_type").value 

        IMAGE_TOPIC = self.get_parameter("camera_stream_topic").value 
        assert IMAGE_TOPIC == None
        self.image_sub = self.create_subscription(Image, IMAGE_TOPIC, self.image_sub_cb)

        if self.PYTORCH_BOOL:
            self.torch_model = PytorchInference(path=PYTORCH_PATH, model_type=PYTORCH_TYPE)
            self.torch_topic = self.create_publisher(String, '/pytorch_inference_result', 10)
            self.get_logger().info("PyTorch Node is activated!")

        if self.TF_BOOL:
            self.tf_model = TFInference(path=TF_PATH, model_type=TF_TYPE)
            self.tf_topic = self.create_publisher(String, '/tensorflow_inference_result', 10)
            self.get_logger().info("Tensorflow Node is activated!")

        if self.ONNX_BOOL:
            self.onnx_model = OnnxInference(path=ONNX_PATH, model_type=ONNX_TYPE)
            self.onnx_topic = self.create_publisher(String, '/onnx_inference_result', 10)
            self.get_logger().info("ONNX Node is activated!")

    def compute(self):
        while rclpy.ok():
            #TF
            current_Input_Image = self.Input_Image

            if self.TF_BOOL:
                tf_msg = String()
                tf_results = self.tf_model(current_Input_Image)
                if len(tf_results) > 1:
                    result_dict = {"classifications" : tf_results[0].tolist(),
                                    "bbox_informations" : tf_results[1].tolist()}
                    tf_msg.data = json.dumps(result_dict)
            #Pytorch
            #ONNX
            if self.PYTORCH_BOOL:
                pass
            if self.ONNX_BOOL:
                pass

            if self.TF_BOOL:
                self.tf_topic.publish(tf_msg)
            if self.PYTORCH_BOOL:
                self.torch_topic.publish() 
            if self.ONNX_BOOL:
                self.onnx_topic.publish() 
    
    def image_sub_cb(self, image_msg):
        self.Input_Image = self.bridge.imgmsg_to_cv2(image_msg)


































        