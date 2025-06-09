#!/usr/bin/env python3

import rclpy
from RRT_Astar import *
from geometry_msgs.msg import Twist
from tf2_ros import TransformListener
from tf2_geometry_msgs import do_transform_point
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros.transform_broadcaster import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math
import time
import numpy as np
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import sys


class ControlNode:

    def __init__(self):
        self.node = rclpy.create_node('bchukkal_jkatak73')
        self.vel_pub = self.node.create_publisher(Twist, 'cmd_vel', 10)
        self.tf_buffer = Buffer()
        self.listener_tf = TransformListener(self.tf_buffer, self.node)

    # def pause(self):
    #     self.tf_buffer.wait_for_transform('odom', 'base_footprint', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=500))

    # def pause(self):
    #     try:
    #         future = self.tf_buffer.wait_for_transform_async('odom', 'base_footprint', rclpy.time.Time(), rclpy.duration.Duration(seconds=500))
    #         rclpy.spin_until_future_complete(self.node, future)
    #     except Exception as e:
    #         print('Failed to lookup transform:', str(e))

    def pause(self):
        try:
            timeout_sec = 0.5  # Set your timeout value here
            start_time = time.time()
            end_time = start_time + timeout_sec
            while time.time() < end_time:
                if self.tf_buffer.can_transform('odom', 'base_footprint', rclpy.time.Time()):
                    return  # Return if transform is available
                rclpy.spin_once(self.node)  # Spin once with timeout
            print('Timeout occurred while waiting for transform')
        except Exception as e:
            print('Failed to lookup transform:', str(e))


    def cmd_vel(self, linear_velocity, angular_velocity):
        vel_msg = Twist()
        vel_msg.linear.x = linear_velocity
        vel_msg.angular.z = angular_velocity
        self.vel_pub.publish(vel_msg)

    def transform_lookup(self):
        try:
            trans = self.tf_buffer.lookup_transform('odom', 'base_footprint', rclpy.time.Time())
            linear = trans.transform.translation
            angular = trans.transform.rotation
            x, y, z = linear.x, linear.y, linear.z
            roll, pitch, yaw = self.euler_from_quaternion(angular)
            return x, y, yaw
        except Exception as e:
            print('Failed to lookup transform:', str(e))
            return None, None, None

    @staticmethod
    def euler_from_quaternion(quaternion):
        x, y, z, w = quaternion.x, quaternion.y, quaternion.z, quaternion.w
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(t0, t1)
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)
        return roll, pitch, yaw


def main(args=None):
    rclpy.init(args=args)
    control_node = ControlNode()
    print('Press Ctrl + C to exit')

    s_x = 0.5
    s_y = 9.5
    g_x = 9
    g_y = 1
    s_t = 30
    robot_radius = 0.038

    print("ready to rock and roll")
    clearance = float(input("\nEnter obstacle clearance for robot "))

    print("received command")

    RPM1 = 10
    RPM2 = 10
    timer_start = time.time()

    c2g = math.sqrt((s_x - g_x) ** 2 + (s_y - g_y) ** 2)
    total_cost = c2g

    # Rest of your code goes here...
    start_node = Node(s_x, s_y, -1, s_t, 0, 0, 0, 0, c2g, total_cost)
    goal_node = Node(g_x, g_y, -1, 0, 0, 0, 0, c2g, 0, total_cost)

    flag, Node_List, Path_List = RRT_Astar(start_node, goal_node, RPM1, RPM2, robot_radius, clearance)

    if flag == 1:
        x_path, y_path, theta_path, RPM_Left, RPM_Right = Backtrack(goal_node)
    else:
        print("Goal node not found")
        exit(-1)

    print('\n Path found sucessfully')
    figure, axes = plt.subplots()
    axes.set(xlim=(0, 10), ylim=(0, 10))

    obstacle1 = patches.Rectangle((3, 2), 2, 2, color='blue')
    obstacle2 = patches.Rectangle((1, 6), 4, 2, color='blue')
    obstacle3 = patches.Rectangle((8, 3.5), 1, 3, color='blue')

    axes.set_aspect('equal')
    axes.add_patch(obstacle1)
    axes.add_patch(obstacle2)
    axes.add_patch(obstacle3)

    axes.set_aspect('equal')
    axes.add_patch(obstacle1)
    axes.add_patch(obstacle2)
    axes.add_patch(obstacle3)
    
    main_node()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

    plt.plot(start_node.x, start_node.y, "Dw")
    plt.plot(goal_node.x, goal_node.y, "Dg")
    plt.plot(x_path, y_path, 'pink')
    plt.show()
    print('\n Waiting to publish cmd_vel msgs')

    # rclpy.sleep(2)
    time.sleep(2)


    print('\n publishing cmd_vel msgs')
    control_node.pause()
    rate = control_node.node.create_rate(1)

    r = 0.038  # in meters
    L = 0.354  # in meters
    dt = 10
    pi = math.pi

    print (len(x_path))
    print (theta_path)

    for i in range(len(x_path)):
        UL = RPM_Left[i]
        UR = RPM_Right[i]

        theta = theta_path[i]

        pi = math.pi

        UL = UL * 2 * pi / 60
        UR = UR * 2 * pi / 60

        thetan = 3.14 * theta / 180

        theta_dot = (r / L) * (UR - UL)

        velocity_value = (r / 2) * (UL + UR)
        velocity_value = velocity_value * 10

        xn, yn, yaw = control_node.transform_lookup()
        yaw = (yaw) * 180 / np.pi
        print(theta)
        print(yaw)

        diff = ((theta - yaw) + 180) % 360 - 180

        print("velocity value: ", velocity_value, "theta_dot: ", theta_dot, "diff: ", diff)
        control_node.cmd_vel(velocity_value, theta_dot + 0.0045 * diff)
        # rate.sleep()
        time.sleep(0.2)

    control_node.cmd_vel(0.0, 0.0)
    print('successfully reached')

    rclpy.spin_once(control_node.node)
    control_node.node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
