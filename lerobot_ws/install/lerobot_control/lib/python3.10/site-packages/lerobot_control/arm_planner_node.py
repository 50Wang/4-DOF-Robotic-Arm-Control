import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import numpy as np
import math
import time

class ArmPlanner(Node):

    def __init__(self):
        super().__init__('arm_planner')

        self.pub = self.create_publisher(
            Float32MultiArray,
            '/arm_angle',
            10)

        # 当前关节角（初始90度）
        self.current = np.array([90.0, 90.0, 90.0, 90.0])

        # 机械臂参数（根据你实际改！！）
        self.L1 = 0.10
        self.L2 = 0.10
        self.L3 = 0.10
        self.L4 = 0.05

    # ================== 逆运动学 ==================
    def inverse_kinematics(self, x, y, z):

        # 1. 底座角
        theta1 = math.atan2(y, x)

        # 2. 投影到平面
        r = math.sqrt(x**2 + y**2)

        # 减去末端长度
        z = z - self.L1
        r = r - self.L4

        # 3. 余弦定理
        D = (r**2 + z**2 - self.L2**2 - self.L3**2) / (2*self.L2*self.L3)

        if abs(D) > 1:
            self.get_logger().error("目标不可达")
            return None

        theta3 = math.acos(D)

        # 4. 肩关节
        theta2 = math.atan2(z, r) - math.atan2(self.L3*math.sin(theta3),
                                               self.L2 + self.L3*math.cos(theta3))

        # 5. 末端角度（简单保持水平）
        theta4 = -theta2 - theta3

        # 转换为角度
        q1 = math.degrees(theta1)
        q2 = math.degrees(theta2)
        q3 = math.degrees(theta3)
        q4 = math.degrees(theta4)

        return np.array([q1, q2, q3, q4])

    # ================== 插值 ==================
    def interpolate(self, q0, q1, steps=50):

        traj = []

        for i in range(steps):
            alpha = i / steps
            q = (1-alpha)*q0 + alpha*q1
            traj.append(q)

        return traj

    # ================== 发送角度 ==================
    def send_joint(self, q):

        msg = Float32MultiArray()
        msg.data = q.tolist()
        self.pub.publish(msg)

    # ================== 运动函数 ==================
    def move_to(self, x, y, z):

        target = self.inverse_kinematics(x, y, z)

        if target is None:
            return

        self.get_logger().info(f"目标角度: {target}")

        traj = self.interpolate(self.current, target)

        for q in traj:
            self.send_joint(q)
            time.sleep(0.02)

        self.current = target

    # ================== 抓取动作 ==================
    def pick(self, x, y, z):

        self.get_logger().info("开始抓取")

        # 1 上方
        self.move_to(x, y, z + 0.05)

        # 2 下降
        self.move_to(x, y, z)

        # 3 模拟夹爪（这里用第四关节代替）
        q = self.current.copy()
        q[3] += 20
        self.send_joint(q)
        time.sleep(1)

        # 4 抬起
        self.move_to(x, y, z + 0.05)


def main():

    rclpy.init()

    node = ArmPlanner()

    # 示例目标点（你可以改）
    time.sleep(2)

    node.pick(0.0, 0.0, 0.2)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()