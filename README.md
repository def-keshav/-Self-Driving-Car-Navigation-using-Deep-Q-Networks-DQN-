# Self-Driving Car Navigation using Deep Q-Networks (DQN)

This project implements a Deep Q-Network (DQN) to train a simulated autonomous car for lane following and obstacle avoidance in a ROS2-Gazebo environment.

## 🧠 Key Concepts
- Deep reinforcement learning with DQN
- Experience replay & target networks
- Reward shaping
- Urban and obstacle-rich environments

## ⚙️ Technologies
- ROS2 (Foxy)
- Gazebo
- Python
- PyTorch
- OpenAI Gym-style environment

## 📷 Demo
Coming soon: GIFs or demo video of car navigating autonomously

## 📁 Repo Structure
- `/models`: SDF and URDF files for the car
- `/scripts`: Python scripts for DQN training and evaluation
- `/launch`: Launch files for Gazebo simulation

## 📌 How It Works
- The agent receives image + LIDAR input
- Chooses discrete actions (left, right, accelerate, brake)
- Uses Dueling DQN and prioritized experience replay for faster convergence

## 🧠 Skills Applied
- Reinforcement learning (DQN)
- ROS2 simulation integration
- Model evaluation and reward engineering

## 🚀 Run Instructions
1. Launch Gazebo world: `ros2 launch simulation.launch.py`
2. Run training: `python train_dqn.py`
3. Evaluate using saved model

## 🔗 Related Resources
- [GitHub Repo](https://github.com/def-keshav/-Self-Driving-Car-Navigation-using-Deep-Q-Networks-DQN-)

