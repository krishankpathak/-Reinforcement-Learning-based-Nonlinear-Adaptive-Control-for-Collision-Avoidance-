"""
Launch file: multi_quadruped_gazebo.launch.py
Launches Gazebo Harmonic simulation with variable-friction corridor world and spawns two quadruped robots.
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = os.path.dirname(os.path.abspath(__file__))
    world_file = os.path.join(pkg_share, '..', 'worlds', 'variable_friction_corridor.sdf')
    urdf_file = os.path.join(pkg_share, '..', 'urdf', 'transformable_quadruped.urdf.xacro')

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world_file,
            description='Path to Gazebo world SDF'
        ),
        # Spawn Quadruped 1 (Ego Agent at [-8.0, 0.0, 0.22])
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'quadruped_1',
                '-file', urdf_file,
                '-x', '-8.0', '-y', '0.0', '-z', '0.22'
            ],
            output='screen'
        ),
        # Spawn Quadruped 2 (Opposing Peer Agent at [8.0, 0.2, 0.22])
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'quadruped_2',
                '-file', urdf_file,
                '-x', '8.0', '-y', '0.2', '-z', '0.22'
            ],
            output='screen'
        ),
        # ROS-GZ Clock and TF Bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            ],
            output='screen'
        )
    ])
