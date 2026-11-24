"""
Launch file: safety_filtered_navigation.launch.py
Launches the full decentralized stack: Braking Estimator, HOCBF Safety Filter, MAPPO Guidance, and Safety Monitor.
"""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Estimator node: publishes certified lower-bound deceleration a_safe
        Node(
            package='friction_aware_quadruped_nav',
            executable='braking_estimator_node',
            name='braking_estimator_node',
            output='screen',
            parameters=[{'window_size': 20, 'k_conservative': 3.0, 'a_min_phys': 1.2}]
        ),
        # MAPPO guidance policy: generates nominal acceleration u_nom
        Node(
            package='friction_aware_quadruped_nav',
            executable='mappo_policy_node',
            name='mappo_policy_node',
            output='screen'
        ),
        # HOCBF-QP safety filter: solves quadratic program to ensure forward invariance
        Node(
            package='friction_aware_quadruped_nav',
            executable='hocbf_safety_filter_node',
            name='hocbf_safety_filter_node',
            output='screen',
            parameters=[{'gamma1': 1.8, 'gamma2': 2.2, 't_latency': 0.04}]
        ),
        # Safety monitor: triggers friction-matched emergency deceleration on high slack
        Node(
            package='friction_aware_quadruped_nav',
            executable='safety_monitor_node',
            name='safety_monitor_node',
            output='screen'
        )
    ])
