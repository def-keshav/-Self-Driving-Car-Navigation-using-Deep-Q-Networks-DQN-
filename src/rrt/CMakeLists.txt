cmake_minimum_required(VERSION 3.5)
project(rrt)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(std_msgs REQUIRED)

# Include directories
include_directories(
  include
  ${geometry_msgs_INCLUDE_DIRS}
  ${nav_msgs_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
)

# Install launch files.
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install world files.
install(DIRECTORY
  world
  nodes
  launch
  rrt
  src
  DESTINATION share/${PROJECT_NAME}/
)

# Install Python scripts
ament_python_install_package(${PROJECT_NAME})

# Install executables
install(PROGRAMS
  nodes/task.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
    FILES
    nodes/RRT_Astar.py
    nodes/pygame_utils.py
    DESTINATION lib/${PROJECT_NAME}
)

# Declare the package
ament_package()
