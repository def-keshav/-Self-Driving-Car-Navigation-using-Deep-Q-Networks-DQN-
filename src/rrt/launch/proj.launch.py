import launch
import launch_ros.actions
import os

def generate_launch_description():
    world_name = launch.substitutions.LaunchConfiguration('world_name', default="$(find rrt)/world/barena.world")
    robot_name = launch.substitutions.LaunchConfiguration('robot_name', default="burger")
    init_pose = launch.substitutions.LaunchConfiguration('x', default="-x -4.5 -y -4.5 -z 0.0")
    init_pose_x = launch.substitutions.LaunchConfiguration('x', default="-4.5")
    init_pose_y = launch.substitutions.LaunchConfiguration('y', default="-4.5")
    init_pose_z = launch.substitutions.LaunchConfiguration('z', default="0.0")

    current_directory = os.getcwd() # Get the directory of the current file (the launch file)
    relative_path_to_world_file = '../world/barena.world'  # Adjust the path relative to the current directory
    gazebo_world_file = os.path.abspath(os.path.join(current_directory, relative_path_to_world_file))

    gazebo_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(os.getenv('HOME'), 'Desktop', 'year1', 'sem2', '690', 'ENPM690_HW3_kshitij2', 'ENPM690_HW3', 'src', 'turtlebot3', 'turtlebot3_simulations', 'turtlebot3_gazebo', 'launch', 'empty_world.launch.py')),

        launch_arguments={
            'world': gazebo_world_file,
            # 'world_name': world_name,
            'paused': 'false',
            'use_sim_time': 'true',
            'gui': 'true',
            'verbose': 'false',
            'debug': 'false',
            'output': 'screen'
        }.items()
    )
    


    urdf_file_name = 'r2d2.urdf.xml'
    urdf = os.path.join(os.getenv('HOME'), 'testWS2', 'src', 'turtlebot3', 'turtlebot3', 'turtlebot3_description', 'urdf', 'turtlebot3_burger.urdf')
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    param_command = "$(find xacro)/xacro --inorder $(find turtlebot3_description)/urdf/turtlebot3_burger.urdf"

    path_xacro = os.path.join(os.getenv('HOME'), 'testWS2', 'src', 'turtlebot3', 'turtlebot3', 'turtlebot3_description', 'urdf', 'turtlebot3_burger.urdf')


    robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}],
        arguments=[urdf],
        output='screen'
    )

    # task_manager = launch_ros.actions.Node(
    #     package='rrt',
    #     executable='task.py',
    #     name='task_manager',
    #     output='screen'
    # )

    return launch.LaunchDescription([
        gazebo_launch,
        launch.actions.DeclareLaunchArgument('world_name', default_value=world_name),
        launch.actions.DeclareLaunchArgument('robot_name', default_value=robot_name),
        launch.actions.DeclareLaunchArgument('init_pose', default_value=init_pose),
        # spawn_turtlebot,
        robot_state_publisher,
        # task_manager
    ])




# import launch
# import launch_ros.actions
# import os
# from ament_index_python.packages import get_package_share_directory


# def generate_launch_description():
#     world_name = launch.substitutions.LaunchConfiguration('world_name', default="$(find rrt)/world/barena.world")
#     robot_name = launch.substitutions.LaunchConfiguration('robot_name', default="burger")
#     init_pose = launch.substitutions.LaunchConfiguration('x', default="-x -4.5 -y -4.5 -z 0.0")
#     init_pose_x = launch.substitutions.LaunchConfiguration('x', default="-4.5")
#     init_pose_y = launch.substitutions.LaunchConfiguration('y', default="-4.5")
#     init_pose_z = launch.substitutions.LaunchConfiguration('z', default="0.0")

#     # current_directory = os.getcwd() # Get the directory of the current file (the launch file)
#     # relative_path_to_world_file = '../world/barena.world'  # Adjust the path relative to the current directory
#     # gazebo_world_file = os.path.abspath(os.path.join(current_directory, relative_path_to_world_file))

#     # gazebo_launch = launch.actions.IncludeLaunchDescription(
#     #     launch.launch_description_sources.PythonLaunchDescriptionSource(
#     #         os.path.join(os.getenv('HOME'), 'Desktop', 'year1', 'sem2', '690', 'ENPM690_HW3_kshitij2', 'ENPM690_HW3', 'src', 'turtlebot3', 'turtlebot3_simulations', 'turtlebot3_gazebo', 'launch', 'empty_world.launch.py')),

#     #     launch_arguments={
#     #         'world': gazebo_world_file,
#     #         # 'world_name': world_name,
#     #         'paused': 'false',
#     #         'use_sim_time': 'true',
#     #         'gui': 'true',
#     #         'verbose': 'false',
#     #         'debug': 'false',
#     #         'output': 'screen'
#     #     }.items()
#     # )

#     # Get Gazebo ROS interface package
#     pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
#     turtlebt_dir = get_package_share_directory('turtlebot3')

#     # Get the location for empty world
#     world = os.path.join(
#         get_package_share_directory('rrt'),
#         'world', 'barena.world'
#     )

#     burger_sdf = os.path.join(turtlebt_dir, 'turtlebot3', 'turtlebot3_description', 'urdf', 'turtlebot3_burger.urdf')

#     # Launch Description to run Gazebo Server
#     gzserver_cmd = launch.actions.IncludeLaunchDescription(
#         launch.launch_description_sources.PythonLaunchDescriptionSource(
#             os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
#         ),
#         launch_arguments={'world': world}.items()
#     )

#         # Launch Description to run Gazebo Client
#     gzclient_cmd = launch.actions.IncludeLaunchDescription(
#         launch.launch_description_sources.PythonLaunchDescriptionSource(
#             os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
#         )
#     )


#     urdf = os.path.join(os.getenv('HOME'), 'testWS2', 'src', 'turtlebot3', 'turtlebot3', 'turtlebot3_description', 'urdf', 'turtlebot3_burger.urdf')
#     with open(urdf, 'r') as infp:
#         robot_desc = infp.read()

    
#     xml = open(urdf, 'r').read()
#     xml = xml.replace('"', '\\"')
#     swpan_args = '{name: \"burger\", xml: \"' + xml + '\" }'

#     param_command = "$(find xacro)/xacro --inorder $(find turtlebot3_description)/urdf/turtlebot3_burger.urdf"

#     path_xacro = os.path.join(os.getenv('HOME'), 'testWS2', 'src', 'turtlebot3', 'turtlebot3', 'turtlebot3_description', 'urdf', 'turtlebot3_burger.urdf')

#     spawn_turtlebot = launch_ros.actions.Node(
#         package='gazebo_ros',
#         executable='spawn_entity.py',
#         name='spawn_turtlebot',
#         arguments=['-x', init_pose_x, '-y', init_pose_y, '-z', init_pose_z, '-topic', robot_desc, '-entity', robot_name],
#         output='screen'
#     )

#     robot_state_publisher = launch_ros.actions.Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         name='robot_state_publisher',
#         parameters=[{'robot_description': robot_desc}],
#         arguments=[urdf],
#         output='screen'
#     )

#     # task_manager = launch_ros.actions.Node(
#     #     package='rrt',
#     #     executable='task.py',
#     #     name='task_manager',
#     #     output='screen'
#     # )

#     return launch.LaunchDescription([
#         # gazebo_launch,
        
#         gzserver_cmd,
#         gzclient_cmd,
        
#         launch.actions.DeclareLaunchArgument('world_name', default_value=world_name),
#         launch.actions.DeclareLaunchArgument('robot_name', default_value=robot_name),
#         launch.actions.DeclareLaunchArgument('init_pose', default_value=init_pose),
        
#         spawn_turtlebot,
        
#         # launch.actions.ExecuteProcess(
#         #     cmd=['ros2', 'service', 'call', '/spawn_entity',
#         #         'gazebo_msgs/SpawnEntity', swpan_args],
#         #     output='screen'),
        
#         robot_state_publisher,
        
#         # task_manager
#     ])

