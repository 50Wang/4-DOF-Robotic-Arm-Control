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

# URDF simulation模型仿真
具体仿真代码见robot.urdf  

先加载urdf：ros2 run robot_state_publisher robot_state_publisher $(ros2 pkg prefix lerobot_description)/share/lerobot_description/urdf/robot.urdf

打开另一个终端 ros2 run joint_state_publisher_gui joint_state_publisher_gui ，出现带滑动条的图形界面可直观控制机器人每一个关节的旋转角度；

再打开另一个终端输入 rviz2 ，进入rviz

点击左下角Add，选择RobotModel后点OK。接下来将Fixed Frame由map改为base_link，RobotModel中的Description Topic选择/robot_description，即可看见4轴机械臂模型。

<img width="330" height="375" alt="微信图片_20260330212110_432_14" src="https://github.com/user-attachments/assets/bdd3ac2a-bdd8-4afd-adf7-2a1229dc7da1" />

拖动图形界面的滑动条可以控制对应关节运动。

https://github.com/user-attachments/assets/2d2d651b-bc9f-4a81-8f11-6ce15b08ed78

# Moveit2 configuration配置
在终端输入 ros2 run moveit_setup_assistant moveit_setup_assistant

<img width="1089" height="906" alt="微信图片_20260331132936_435_14" src="https://github.com/user-attachments/assets/d7f94637-afb5-483b-b7c5-31e606c20e7d" />

点击Create New Moveit Configuration Package，打开Browse选择.urdf模型文件，点击Load Files加载；

Self-Collisions：点击Generate Collision Matrix自动计算生成；

Virtual Joints：Add Virtual Joint， Name->virtual_joint，Child->base_link，Parent->world，Type->Fixed；

Planning Groups：把机械臂分成“手臂”和“夹爪”两组，分别进行路径规划

Add Group， Group Name->arm，Kinematic Solver->kdl_kinematics_plugin/KDLKinematicsPlugin，Add Joints->按住 Ctrl 选入joint123，点击 > 把它们移到右侧，点击save

Group Name->gripper，Add Joints选入joint4，点击 > 箭头把它们移到右侧，点击save；

Robot Poses：预设回零动作 Add Pose， Pose Name->home，Planning Group->arm，将所有关节拖动到 0 的位置，点击save；

End Effectors：Add End Effector， End Effector Name->hand，End Effector Group->gripper，Parent Link->link2（连接末端的最后一个连杆），Parent Group->arm，点击save；

Passive Joints：跳过；

ros2_control URDF Modification：点击底部的 Add Default Hardware Interfaces；

ROS2 Controllers：点击 Auto Add FollowJointTrajectory Controllers for each Planning Group，自动生成 arm_controller 和 gripper_controller；

MoveIt Controllers：点击 Setup Controller Manager，确保 arm_controller 出现在列表中；

Perception：跳过；

Author Information：输入英文名字和邮箱；

Configuration Files：点击 Browse，在 src 目录下新建一个文件夹，命名为 lerobot_moveit_config，点击 Generate Package，提示 Package Generated Successfully! 后即可关闭窗口。





















