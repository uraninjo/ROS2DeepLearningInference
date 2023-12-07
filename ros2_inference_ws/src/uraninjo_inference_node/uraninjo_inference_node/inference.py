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

# from .onnx_model_handler import OnnxInference
from .pytorch_model_handler import PytorchInference
from .tf_model_handler import TFInference
import torch
class InferenceNode(Node):
    def __init__(self):
        super().__init__("inference_node")

        self.declare_parameters(
            namespace="",
            parameters=[
                ("pytorch_inference_allowed", False),
                ("onnx_inference_allowed", False),
                ("tensorflow_inference_allowed", False),
                ("pytorch_model_path", "src/uraninjo_inference_node/uraninjo_inference_node/torch_resnet50.h5"),
                ("onnx_model_path", None),
                ("tensorflow_model_path", "src/uraninjo_inference_node/uraninjo_inference_node/vgg.h5"),
                ("camera_stream_topic", "/rgb_left"),
            ],
        )
        self.Input_Image = None

        self.bridge = CvBridge()

        self.PYTORCH_BOOL = self.get_parameter("pytorch_inference_allowed").value
        self.ONNX_BOOL = self.get_parameter("onnx_inference_allowed").value
        self.TF_BOOL = self.get_parameter("tensorflow_inference_allowed").value

        PYTORCH_PATH = self.get_parameter("pytorch_model_path").value
        ONNX_PATH = self.get_parameter("onnx_model_path").value
        TF_PATH = self.get_parameter("tensorflow_model_path").value 

        IMAGE_TOPIC = self.get_parameter("camera_stream_topic").value 
        print("IMAGE: ", IMAGE_TOPIC)
        assert IMAGE_TOPIC is not None
        
        self.image_sub = self.create_subscription(Image, IMAGE_TOPIC, self.image_sub_cb, 10)

        if self.PYTORCH_BOOL:
            self.torch_model = PytorchInference(path=PYTORCH_PATH)
            self.torch_topic = self.create_publisher(String, '/pytorch_inference_result', 10)
            self.get_logger().info("PyTorch Node is activated!")

        if self.TF_BOOL:
            self.tf_model = TFInference(path=TF_PATH)
            self.tf_topic = self.create_publisher(String, '/tensorflow_inference_result', 10)
            self.get_logger().info("Tensorflow Node is activated!")

        # if self.ONNX_BOOL:
        #     self.onnx_model = OnnxInference(path=ONNX_PATH)
        #     self.onnx_topic = self.create_publisher(String, '/onnx_inference_result', 10)
        #     self.get_logger().info("ONNX Node is activated!")
        if self.PYTORCH_BOOL + self.TF_BOOL + self.ONNX_BOOL > 0:
            self.timer = self.create_timer(3, self.compute)
        else:
            self.get_logger().info("Nothing is activated. Exiting!")
            sys.exit()

    def compute(self):
        if not self.Input_Image is None:
            print("llooop")
            
            current_Input_Image = self.Input_Image
            #TF
            if self.TF_BOOL:
                tf_msg = String()
                print("asdasdsa")
                tf_metadata = self.tf_model.inference_generator(current_Input_Image)
                tf_msg.data = json.dumps(tf_metadata)
            #Pytorch
            if self.PYTORCH_BOOL:
                
                torch_msg = String()
                
                torch_metadata = self.torch_model.inference_generator(current_Input_Image)
                torch_msg.data = json.dumps(torch_metadata)
            #ONNX
            if self.ONNX_BOOL:
                pass

            if self.TF_BOOL:
                self.tf_topic.publish(tf_msg)
            if self.PYTORCH_BOOL:
                self.torch_topic.publish(torch_msg) 
            if self.ONNX_BOOL:
                self.onnx_topic.publish() 

    
    def image_sub_cb(self, image_msg):
        self.Input_Image = self.bridge.imgmsg_to_cv2(image_msg)
        #print("Got the Image!\n\n")

def main():
    rclpy.init()
    node = InferenceNode()
    rclpy.spin(node)
    rclpy.shutdown()



        