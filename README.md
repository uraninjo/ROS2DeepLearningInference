## How to Use 

The ROS2 node has been designed to facilitate the utilization of your TensorFlow and PyTorch models separately. This package provides capabilities for inference along with model-handling features.

Support for TensorFlow and PyTorch has been incorporated, and Onnx support is planned for the next version.

To configure the node, please follow these steps:

Open the launch file located at **ros2_inference_ws/src/uraninjo_inference_node/launch/inference.launch.py**.

Specify the following inputs:

- **pytorch_inference_allowed** and **pytorch_model_path**
- **tensorflow_inference_allowed** and **tensorflow_model_path**

All options are optional, depending on the framework you intend to use.