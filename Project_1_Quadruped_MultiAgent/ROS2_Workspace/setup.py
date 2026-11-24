from setuptools import setup
import os
from glob import glob

package_name = 'friction_aware_quadruped_nav'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Autonomous Robotics Research Scientist',
    maintainer_email='researcher@robotics-lab.org',
    description='Friction-Aware Safety-Critical Navigation for Quadruped Teams in ROS 2 Gazebo',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'braking_estimator_node = friction_aware_quadruped_nav.braking_estimator_node:main',
            'hocbf_safety_filter_node = friction_aware_quadruped_nav.hocbf_safety_filter_node:main',
            'mappo_policy_node = friction_aware_quadruped_nav.mappo_policy_node:main',
            'safety_monitor_node = friction_aware_quadruped_nav.safety_monitor_node:main',
        ],
    },
)
