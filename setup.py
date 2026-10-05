from setuptools import setup, find_packages
from glob import glob
setup(name='autonomous_turtlebot_ai',version='0.1.0',packages=find_packages(),
    data_files=[('share/ament_index/resource_index/packages',['resource/autonomous_turtlebot_ai']),
                ('share/autonomous_turtlebot_ai',['package.xml']),
                ('share/autonomous_turtlebot_ai/launch',glob('launch/*.launch.py')),
                ('share/autonomous_turtlebot_ai/config',glob('config/*.yaml')),
                ('share/autonomous_turtlebot_ai/checkpoints',glob('checkpoints/*'))],
    install_requires=['setuptools'],zip_safe=True,license='MIT',
    description='New TurtleBot3 simulation and vision reconstruction',
    entry_points={'console_scripts':['supervisor = autonomous_turtlebot_ai.supervisor:main',
                                    'detector = autonomous_turtlebot_ai.detector:main']})
