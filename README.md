# Mars-Rover

## Electronics Subsystem

### Power Management
The rover is powered by Lithium Polymer batteries, which provide energy to all onboard components and propulsion systems through a network of voltage converters (both buck and boost converters). Safety mechanisms are in place to protect against overvoltage, undervoltage, reverse polarity, and overcurrent situations. These include protection circuits and Miniature Circuit Breakers (MCBs). In extreme conditions, a kill switch can completely cut off the power supply.

### Motor Drivers
Cytron motor drivers are employed to control the various motors used in the rover. These drivers are crucial for the precise movement and operation of the rover's components.

### Control and Integration
The computational framework of the rover is built on a combination of Raspberry Pi and Arduino microcontrollers. This setup integrates various sensors and cameras, enabling comprehensive control and data acquisition. The Arduino MEGA handles the interfacing of multiple sensors.

### Camera Systems
Three cameras are mounted on the rover, each serving a specific function:
1. **Navigation Camera**: With a 45-degree field of view, it assists in navigation by providing visual feedback to the base station.
2. **Manipulator Camera**: Mounted at the end effector of the manipulator, it aids in precise handling and operation of the manipulator.
3. **Soil Analysis Camera**: Installed in the soil analysis module, it provides visual data for the analysis of collected soil samples.

The live video streams from these cameras are transmitted to the base station, where they can be viewed and processed. Panoramic views are created by stitching images from the navigation camera.

### Communication Subsystem
The primary processor of the rover, a Raspberry Pi, runs on a Linux operating system stored on an SD card. The Robot Operating System (ROS) is integrated into the Raspberry Pi, enabling the base station to send commands to the rover over a Wi-Fi network. The system uses a 5 GHz frequency band for wireless communication, which offers a range of approximately 950 meters. The communication setup includes Wi-Fi routers connected to the base station and the Raspberry Pi, ensuring robust and reliable data transmission.

## Software Subsystem

### System Architecture
The software subsystem is designed for both autonomous and command-based control, visualization, and task-specific algorithm implementation. The core framework is based on the Robot Operating System (ROS), which facilitates seamless integration with the rover's processor, database management, and command execution from the base station.

### Simulation and Visualization
- **Rviz**: Used for real-time visualization and simulation of the rover's state and environment.
- **Gazebo**: Employed to simulate the rover's motion and interaction with the environment, providing a realistic 3D model.

### Video Processing and Machine Learning
The rover's cameras continuously transmit an MPIG-4 based video feed. The images are processed to create panoramic views, which are essential for tasks like arrow detection. The system leverages trained models using OpenCV and TensorFlow for advanced image processing and recognition tasks.

### Web-GUI
A Web-GUI, developed using npm-based Node.js and HTML-5 frameworks, allows for continuous visualization of sensor data, power calculations, task switching, and video feed monitoring. The Web-GUI server connects through WebSocket, enabling simultaneous task simulation and real-time control. A web server, utilizing MJPG-4 streaming, supports the video feed integration.

### Operation Modes
- **Manual Operation**: The rover is teleoperated from the base station.
- **Autonomous Mode**: For tasks requiring autonomous navigation and operation, the rover switches to an autonomous mode.
- **Manipulator Mode**: When precise manipulator control is needed, the system can switch from manual to manipulator mode seamlessly.

### Autonomous Expedition
For autonomous navigation, the rover employs a combination of sensors and algorithms to avoid obstacles and navigate rough terrain. The power system ensures all components are adequately powered, and DC motors, controlled by Cytron MDD10A motor drivers interfaced with Arduino-UNO, provide necessary torque. 

#### Sensors
- **Ultrasonic Sensors (HCSR05)**: Measure the distance to nearby objects, essential for obstacle avoidance.
- **IMU (MPU9250)**: Measures roll, pitch, and yaw to determine the rover's orientation and position.
- **GPS**: Tracks the rover's location, assisting in navigation and path planning.
- **Wheel Encoders**: Provide data on wheel rotation, helping in precise movement control.

### Path Planning Algorithm
The rover's processor runs a path planning algorithm, utilizing sensor data to navigate towards the target location with minimal damage and optimal efficiency. This algorithm integrates data from ultrasonic sensors, IMU, GPS, and wheel encoders to make informed decisions about the rover's movements.
