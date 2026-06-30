import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
import math
import sys
import tty
import termios


class KeyboardControl(Node):

    def __init__(self):
        super().__init__('keyboard_control')

        self.serial_port = '/dev/ttyUSB0'
        self.baud_rate = 115200

        self.ser = None
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.get_logger().info(f"成功连接串口: {self.serial_port}")
        except Exception as e:
            self.get_logger().error(f"无法打开串口: {e}")
            self.get_logger().warn("将在没有串口的情况下运行（仅打印调试信息）")

        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

        # 当前舵机角度，初始全部 90°（中立位）
        self.angles = {name: 90 for name in self.joint_names}

        # 当前操控的关节索引（0=joint1）
        self.current_joint_index = 0

        # 每次按键调整的步长（度）
        self.step = 5

        # 发布 /joint_states 供 RViz 同步显示
        self.pub = self.create_publisher(JointState, '/joint_states', 10)

        self.print_status()

    # ------------------------------------------------------------------
    def print_status(self):
        name = self.joint_names[self.current_joint_index]
        print("\033[2J\033[H", end="")   # 清屏
        print("==============================")
        print("  键盘控制机械臂")
        print("==============================")
        print(f"  当前关节: {name}  ({self.angles[name]}°)")
        print("------------------------------")
        for i, n in enumerate(self.joint_names):
            marker = ">>>" if i == self.current_joint_index else "   "
            print(f"  {marker} {n}: {self.angles[n]}°")
        print("------------------------------")
        print("  a  : 角度 -")
        print("  d  : 角度 +")
        print("  s  : 切换关节")
        print("  r  : 所有关节归零(0°)")
        print("  q  : 退出")
        print("==============================")

    # ------------------------------------------------------------------
    def get_key(self):
        """读取单个键盘输入（不需要回车）"""
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

    # ------------------------------------------------------------------
    def send(self):
        """将当前4个关节角度通过串口发送，同时发布到 /joint_states"""
        a = [self.angles[n] for n in self.joint_names]
        cmd = f"{a[0]} {a[1]} {a[2]} {a[3]}\n"

        if self.ser and self.ser.is_open:
            self.ser.write(cmd.encode())

        # 发布到 RViz（弧度）
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = [math.radians(self.angles[n] - 90) for n in self.joint_names]
        self.pub.publish(msg)

    # ------------------------------------------------------------------
    def run(self):
        print("节点已启动，开始监听键盘...")
        while rclpy.ok():
            key = self.get_key()

            if key == 'a':
                name = self.joint_names[self.current_joint_index]
                self.angles[name] = max(0, self.angles[name] - self.step)
                self.send()

            elif key == 'd':
                name = self.joint_names[self.current_joint_index]
                self.angles[name] = min(180, self.angles[name] + self.step)
                self.send()

            elif key == 's':
                self.current_joint_index = (self.current_joint_index + 1) % len(self.joint_names)

            elif key == 'r':
                for n in self.joint_names:
                    self.angles[n] = 0
                self.send()

            elif key == 'q':
                print("\n退出键盘控制")
                break

            self.print_status()

    # ------------------------------------------------------------------
    def destroy_node(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        super().destroy_node()


def main():
    rclpy.init()
    node = KeyboardControl()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()