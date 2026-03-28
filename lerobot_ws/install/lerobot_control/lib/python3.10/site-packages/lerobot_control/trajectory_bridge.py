import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState # 更改为 JointState 消息
import serial
import time
import math

class TrajectoryBridge(Node):

    def __init__(self):
        super().__init__('trajectory_bridge')

        # --- 配置区 ---
        # 请确保串口路径正确，如果不确定，在终端输入 ls /dev/ttyUSB* 查看
        self.serial_port = '/dev/ttyUSB0' 
        self.baud_rate = 115200
        
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.get_logger().info(f"成功连接串口: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"无法打开串口: {e}")

        # 订阅 /joint_states 话题
        self.sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10)
        
        # 关节名称映射（确保角度顺序永远是 joint1,2,3,4）
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

    def callback(self, msg):
        # 创建一个临时字典，方便通过名字找位置
        joint_map = dict(zip(msg.name, msg.position))
        
        try:
            # 1. 提取 4 个关节的弧度值
            raw_positions = [joint_map[name] for name in self.joint_names]
            
            # 2. 弧度转角度 (rad -> deg)
            angles = [int(math.degrees(x)) for x in raw_positions]
            
            # 3. 映射与限幅 (假设你的舵机是 0-180 度)
            # 注意：如果你的机械臂 0 度在中间，可能需要加个偏移量，比如 a + 90
            final_angles = [max(0, min(180, a)) for a in angles]

            # 4. 拼接字符串并发送，格式为 "j1,j2,j3,j4\n"
            cmd = f"{final_angles[0]},{final_angles[1]},{final_angles[2]},{final_angles[3]}\n"
            
            self.ser.write(cmd.encode())
            
            # 打印调试信息
            self.get_logger().info(f"发送指令: {cmd.strip()}")

        except KeyError as e:
            # 如果收到的 joint_states 还不完整，先跳过
            self.get_logger().warn(f"等待关节数据: {e}")

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

if __name__ == '__main__':
    main()
