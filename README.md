# 4-DOF-Robotic-Arm-Control
4轴机械臂的关节控制、动作规划、模型仿真和Moveit2配置/Joint control, motion planning, model simulation and Moveit2 configuration of 4-axis robotic arm.

# Software软件系统
Keil MDK5, Ubuntu22.04 ROS2-Humble

# Hardware硬件准备
4轴机械臂(mg90系列舵机4个)、stm32f103c8t6控制板、面包板5/3.3V电源模块、USB转TTL模块、ST-LINK烧录器/4-axis robotic arm (with 4 servo motors of mg90 series), STM32F103C8T6 control board, breadboard with 5/3.3V power module, USB to TTL module, ST-LINK Programmer

![微信图片_20260329114157_420_14](https://github.com/user-attachments/assets/fb6517bf-6bf9-47b7-ae4e-cc6bc82d8776)

![微信图片_20260329114212_421_14](https://github.com/user-attachments/assets/89d4ddaa-acd1-4e4e-bd43-7c2d9e93203a)

# Circuit connection电路连线
将电源模块插到面包板上，跳线帽拨至5V。（！！注意后续连线5V和GND时，杜邦线端头要插到离电源模块较近的位置，以免无法供电）

图2由下到上分别为关节舵机1-4 (PWM1-4)

<img width="1128" height="426" alt="微信图片_20260329153403_424_14" src="https://github.com/user-attachments/assets/788669f9-1bba-46e6-b9ae-ca3d7d9eb36c" />

# RobotArm
该程序通过串口中断实时解析上位机发送的角度指令，并同步驱动四个PWM通道来实现对四自由度机械臂关节姿态的控制。

连接stm32和stlink，在Keil中打开RobotArm文件夹，先后点击左上角的Rebuild和LOAD，将程序烧录进stm32，按下板上的RESET即可运行。

# Joint control关节控制
将USB转TTL模块连接电脑，打开虚拟机，在终端输入 ls /dev/tty* 查看是否有新的串口名称出现，sudo chmod 777 /dev/新串口名 赋予权限。 

lerobot.py：ROS2串口通信驱动节点，通过订阅 arm_angle 话题获取机械臂的目标角度，并将ROS2的标准消息格式（Float32MultiArray）转换为Keil代码中定义的字符串格式

先 ros2 run lerobot_control lerobot

再打开另一个终端，输入：ros2 topic pub /arm_angle std_msgs/msg/Float32MultiArray "data: [20,20,20,20]" ，即手动发布一条包含关节角度的消息到订阅的话题中。

https://github.com/user-attachments/assets/7c2b7e9f-0413-4353-8b65-9795d6ad3d6e

# Point-to-point control点对点控制 
arm_planner_node.py：通过逆运动学算法将目标三维坐标(x,y,z)实时解算为关节角度(theta1-theta4)，控制机械臂末端到达指定三维坐标

！！逆运动学部分大家可以结合网上资料手动推导一下

先 ros2 run lerobot_control lerobot

打开另一个终端 ros2 run lerobot_control arm_planner

https://github.com/user-attachments/assets/782b53f8-2bb5-40c7-a1e2-805091b85c0b

# urdf simulation模型仿真
具体仿真代码见robot.urdf  

先加载urdf：ros2 run robot_state_publisher robot_state_publisher $(ros2 pkg prefix lerobot_description)/share/lerobot_description/urdf/robot.urdf

打开另一个终端 ros2 run joint_state_publisher_gui joint_state_publisher_gui ，调出带滑动条的图形界面直观地控制机器人每一个关节的旋转角度；

再打开另一个终端输入 rviz2 ，进入rviz



<img width="330" height="375" alt="微信图片_20260330212110_432_14" src="https://github.com/user-attachments/assets/bdd3ac2a-bdd8-4afd-adf7-2a1229dc7da1" />









