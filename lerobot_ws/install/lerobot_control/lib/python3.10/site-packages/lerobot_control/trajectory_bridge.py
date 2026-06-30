# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import JointState # 更改为 JointState 消息
# import serial
# import time
# import math

# class TrajectoryBridge(Node):

#     def __init__(self):
#         super().__init__('trajectory_bridge')

#         # --- 配置区 ---
#         # 请确保串口路径正确，如果不确定，在终端输入 ls /dev/ttyUSB* 查看
#         self.serial_port = '/dev/ttyUSB0' 
#         self.baud_rate = 115200
        
#         try:
#             self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
#             self.get_logger().info(f"成功连接串口: {self.serial_port}")
#         except Exception as e:
#             self.get_logger().error(f"无法打开串口: {e}")

#         # 订阅 /joint_states 话题
#         self.sub = self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.callback,
#             10)
        
#         # 关节名称映射（确保角度顺序永远是 joint1,2,3,4）
#         self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

#     def callback(self, msg):
#         # 创建一个临时字典，方便通过名字找位置
#         joint_map = dict(zip(msg.name, msg.position))
        
#         try:
#             # 1. 提取 4 个关节的弧度值
#             raw_positions = [joint_map[name] for name in self.joint_names]
            
#             # 2. 弧度转角度 (rad -> deg)
#             angles = [int(math.degrees(x)) for x in raw_positions]
            
#             # 3. 映射与限幅 (假设你的舵机是 0-180 度)
#             # 注意：如果你的机械臂 0 度在中间，可能需要加个偏移量，比如 a + 90
#             final_angles = [max(0, min(180, a)) for a in angles]

#             # 4. 拼接字符串并发送，格式为 "j1,j2,j3,j4\n"
#             cmd = f"{final_angles[0]},{final_angles[1]},{final_angles[2]},{final_angles[3]}\n"
            
#             self.ser.write(cmd.encode())
            
#             # 打印调试信息
#             self.get_logger().info(f"发送指令: {cmd.strip()}")

#         except KeyError as e:
#             # 如果收到的 joint_states 还不完整，先跳过
#             self.get_logger().warn(f"等待关节数据: {e}")

# def main():
#     rclpy.init()
#     node = TrajectoryBridge()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()




# import rclpy
# from rclpy.node import Node
# from moveit_msgs.msg import DisplayTrajectory
# import serial
# import time
# import math


# class TrajectoryBridge(Node):

#     def __init__(self):
#         super().__init__('trajectory_bridge')

#         self.serial_port = '/dev/ttyUSB0'
#         self.baud_rate = 115200

#         self.ser = None
#         try:
#             self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
#             self.get_logger().info(f"成功连接串口: {self.serial_port}")
#         except Exception as e:
#             self.get_logger().error(f"无法打开串口: {e}")
#             self.get_logger().warn("将在没有串口的情况下运行（仅打印调试信息）")

#         self.sub = self.create_subscription(
#             DisplayTrajectory,
#             '/display_planned_path',
#             self.callback,
#             10)

#         self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

#         # joint4 不在轨迹里时保持上次角度，初始默认 90°
#         self.last_angles = {name: 0 for name in self.joint_names}

#         self.get_logger().info("已订阅 /display_planned_path，等待轨迹...")

#     def rad_to_servo(self, rad: float) -> int:
#         """弧度 → 舵机角度，中立位 0 rad 映射到 90°，限幅 0-180°"""
#         return max(0, min(180, round(math.degrees(rad) + 90.0)))

#     def callback(self, msg: DisplayTrajectory):
#         if len(msg.trajectory) == 0:
#             return

#         traj = msg.trajectory[0].joint_trajectory
#         traj_joint_names = list(traj.joint_names)

#         # 建立名字→索引映射（只映射轨迹里有的关节）
#         index_map = {}
#         for name in self.joint_names:
#             if name in traj_joint_names:
#                 index_map[name] = traj_joint_names.index(name)

#         if not index_map:
#             self.get_logger().warn("轨迹中没有任何已知关节，跳过")
#             return

#         self.get_logger().info(f"收到轨迹，共 {len(traj.points)} 个路径点，开始执行...")

#         for point in traj.points:
#             if len(point.positions) == 0:
#                 continue

#             try:
#                 for name in self.joint_names:
#                     if name in index_map:
#                         self.last_angles[name] = self.rad_to_servo(
#                             point.positions[index_map[name]]
#                         )
#                 # 始终发送4个关节，joint4 不在轨迹时保持上次值
#                 angles = [self.last_angles[n] for n in self.joint_names]
#             except IndexError as e:
#                 self.get_logger().warn(f"路径点数据异常，跳过: {e}")
#                 continue

#             cmd = f"{angles[0]} {angles[1]} {angles[2]} {angles[3]}\n"

#             if self.ser and self.ser.is_open:
#                 self.ser.write(cmd.encode())

#             self.get_logger().info(f"发送: {cmd.strip()}")
#             time.sleep(0.08)

#     def destroy_node(self):
#         if self.ser and self.ser.is_open:
#             self.ser.close()
#         super().destroy_node()


# def main():
#     rclpy.init()
#     node = TrajectoryBridge()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()


# #!/usr/bin/env python3
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import JointState
# from std_msgs.msg import Float32MultiArray
# import math

# class MoveItBridgeNode(Node):
#     def __init__(self):
#         super().__init__('moveit_bridge_node')
        
#         # 1. 定义你需要控制的 4 个关节名称（必须与你的 URDF / MoveIt 配置中的关节名完全一致）
#         # 请根据你的实际 URDF 修改这里的名称
#         self.target_joint_names = ['joint1', 'joint2', 'joint3', 'joint4'] 
        
#         # 2. 创建订阅者：订阅 MoveIt 发布的关节状态
#         self.joint_state_sub = self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.joint_state_callback,
#             10
#         )
        
#         # 3. 创建发布者：发布转好的角度给 lerobot 节点
#         self.angle_pub = self.create_publisher(
#             Float32MultiArray,
#             '/arm_angle',
#             10
#         )
        
#         self.get_logger().info('MoveIt 虚实同步桥接节点已启动，监听 /joint_states 中...')

#     def joint_state_callback(self, msg: JointState):
#         # 创建用于存放 4 个关节角度的字典，方便通过名字对应
#         joint_positions_dict = {}
        
#         # 遍历接收到的数据，建立 名字 -> 弧度值 的映射
#         for name, position in zip(msg.name, msg.position):
#             joint_positions_dict[name] = position
            
#         try:
#             # 按照我们定义的 1-4 号关节顺序提取弧度，并转换为角度
#             angles_deg = []
#             for joint_name in self.target_joint_names:
#                 rad = joint_positions_dict[joint_name]
#                 deg = math.degrees(rad) # 弧度转角度
#                 angles_deg.append(deg)
                
#             # 包装成 Float32MultiArray 格式
#             output_msg = Float32MultiArray()
#             output_msg.data = angles_deg
            
#             # 发布出去，供 lerobot.py 消费
#             self.angle_pub.publish(output_msg)
            
#             # 打印日志（可选，调试完可以注释掉）
#             # self.get_logger().info(f'发布角度: {[round(d, 2) for d in angles_deg]}')
            
#         except KeyError as e:
#             # 如果 /joint_states 里还没包含你指定的全部关节名，先跳过
#             pass

# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveItBridgeNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()







#!/usr/bin/env python3

import math
import time
import serial

import rclpy
from rclpy.node import Node

from moveit_msgs.msg import DisplayTrajectory


class TrajectoryBridge(Node):

    def __init__(self):
        super().__init__("trajectory_bridge")

        # ==============================
        # 串口配置
        # ==============================
        self.serial_port = "/dev/ttyUSB0"
        self.baud_rate = 115200

        self.ser = None

        try:
            self.ser = serial.Serial(
                self.serial_port,
                self.baud_rate,
                timeout=0.1
            )

            self.get_logger().info(
                f"Serial Open : {self.serial_port}"
            )

        except Exception as e:

            self.get_logger().error(
                f"Open Serial Failed : {e}"
            )

        # ==============================
        # MoveIt关节名称
        # ==============================

        self.joint_names = [
            "joint1",
            "joint2",
            "joint3",
            "joint4"
        ]

        # ==============================
        # 舵机方向
        # 1 = 正方向
        # -1 = 反方向
        # ==============================

        self.direction = {

            "joint1": 1,
            "joint2": 1,
            "joint3": 1,
            "joint4": 1

        }

        # ==============================
        # 舵机零位
        # 后期标定修改这里即可
        # ==============================

        self.offset = {

            "joint1": 90,
            "joint2": 90,
            "joint3": 90,
            "joint4": 90

        }

        # 当前角度

        self.current = {

            "joint1": 90,
            "joint2": 90,
            "joint3": 90,
            "joint4": 90

        }

        # 最大发送频率（MG90建议50Hz）

        self.send_period = 0.02

        # ==============================

        self.create_subscription(

            DisplayTrajectory,

            "/display_planned_path",

            self.callback,

            10

        )

        self.get_logger().info(
            "Waiting MoveIt trajectory..."
        )

    ####################################################

    def rad_to_servo(self, joint_name, rad):

        deg = math.degrees(rad)

        servo = self.offset[joint_name] + \
                self.direction[joint_name] * deg

        servo = round(servo)

        if servo < 0:
            servo = 0

        if servo > 180:
            servo = 180

        return servo

    ####################################################

    def send(self):

        angles = [

            self.current["joint1"],
            self.current["joint2"],
            self.current["joint3"],
            self.current["joint4"]

        ]

        cmd = "{} {} {} {}\n".format(
            angles[0],
            angles[1],
            angles[2],
            angles[3]
        )

        if self.ser is not None:

            try:

                self.ser.write(cmd.encode())

            except Exception as e:

                self.get_logger().error(str(e))

        self.get_logger().info(
            "Send : " + cmd.strip()
        )

    ####################################################

    def callback(self, msg):

        if len(msg.trajectory) == 0:

            return

        traj = msg.trajectory[0].joint_trajectory

        if len(traj.points) == 0:

            return

        self.get_logger().info(

            "Receive trajectory : {} points".format(

                len(traj.points)

            )

        )

        # 建立索引

        index = {}

        for name in self.joint_names:

            if name in traj.joint_names:

                index[name] = traj.joint_names.index(name)

        if len(index) == 0:

            self.get_logger().warn(
                "No joint matched."
            )

            return

        last_time = 0.0

        last_send = 0.0

        #########################################

        for point in traj.points:

            now = point.time_from_start.sec + \
                  point.time_from_start.nanosec * 1e-9

            dt = now - last_time

            if dt > 0:

                time.sleep(dt)

            last_time = now

            # 限制50Hz发送

            if now - last_send < self.send_period:

                continue

            last_send = now

            for joint in index:

                pos = point.positions[index[joint]]

                self.current[joint] = self.rad_to_servo(

                    joint,

                    pos

                )

            self.send()

        #########################################

        self.get_logger().info(
            "Trajectory Finished."
        )

    ####################################################

    def destroy_node(self):

        if self.ser is not None:

            self.ser.close()

        super().destroy_node()


#############################################################


def main():

    rclpy.init()

    node = TrajectoryBridge()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":

    main()











