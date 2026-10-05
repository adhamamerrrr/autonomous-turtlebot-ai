"""TurtleBot3 Waffle Pi, SLAM Toolbox, Nav2 and a separate velocity gate."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction, AppendEnvironmentVariable, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetRemap


def generate_launch_description():
    tb3 = get_package_share_directory('turtlebot3_gazebo')
    nav2 = get_package_share_directory('nav2_bringup')
    own = get_package_share_directory('autonomous_turtlebot_ai')
    def include(package, file, arguments):
        return IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(package,'launch',file)),
            launch_arguments=arguments.items())
    return LaunchDescription([
        DeclareLaunchArgument('smoke_model',default_value=os.path.join(own,'checkpoints','smoke.pt')),
        DeclareLaunchArgument('violence_model',default_value=''),
        SetEnvironmentVariable('TURTLEBOT3_MODEL','waffle_pi'),
        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH',os.path.join(tb3,'models')),
        include(get_package_share_directory('ros_gz_sim'),'gz_sim.launch.py',
                {'gz_args':['-r -s --headless-rendering ',os.path.join(tb3,'worlds','turtlebot3_world.world')]}),
        include(tb3,'robot_state_publisher.launch.py',{'use_sim_time':'true'}),
        include(tb3,'spawn_turtlebot3.launch.py',{'x_pose':'-2.0','y_pose':'-0.5'}),
        include(get_package_share_directory('slam_toolbox'),'online_async_launch.py',
                {'use_sim_time':'true','slam_params_file':os.path.join(own,'config','slam.yaml')}),
        # Only navigation processes are remapped. No bypassing the supervisor output.
        GroupAction([
            SetRemap(src='/cmd_vel',dst='/cmd_vel_nav'),
            include(nav2,'navigation_launch.py',{'use_sim_time':'true','autostart':'true',
                'use_composition':'False','params_file':os.path.join(own,'config','nav2.yaml')})]),
        Node(package='autonomous_turtlebot_ai',executable='supervisor',output='screen',
             parameters=[{'use_sim_time':True,'stamped_input':True}]),
        Node(package='autonomous_turtlebot_ai',executable='detector',output='screen',
             parameters=[{'use_sim_time':True,'smoke_model':LaunchConfiguration('smoke_model'),
                          'violence_model':LaunchConfiguration('violence_model')}]),
    ])
