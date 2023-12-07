from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='uraninjo_inference_node',  # Replace 'your_package_name' with the actual name of your ROS 2 package
            executable='inference',
            name='inference',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'pytorch_inference_allowed': False},
                {'onnx_inference_allowed': False},
                {'tensorflow_inference_allowed': False},
                {'pytorch_model_path': 'src/uraninjo_inference_node/uraninjo_inference_node/torch_resnet50.h5'},
                {'onnx_model_path': ""},
                {'tensorflow_model_path': 'src/uraninjo_inference_node/uraninjo_inference_node/vgg.h5'},
                {'camera_stream_topic': '/rgb_left'},
            ],
        ),
    ])
