import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import serial

class ArmNode(Node):

    def __init__(self):

        super().__init__('servo_arm_node')

        self.ser = serial.Serial('/dev/ttyUSB0',115200)

        self.sub = self.create_subscription(
            Float32MultiArray,
            'arm_angle',
            self.callback,
            10)

    def callback(self,msg):

        a1 = int(msg.data[0])
        a2 = int(msg.data[1])
        a3 = int(msg.data[2])
        a4 = int(msg.data[3])

        cmd = f"{a1} {a2} {a3} {a4}\n"

        self.ser.write(cmd.encode())

        self.get_logger().info(f"send: {cmd}")


def main(args=None):

    rclpy.init(args=args)

    node = ArmNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
