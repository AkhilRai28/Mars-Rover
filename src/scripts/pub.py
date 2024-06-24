#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class RoverController:
    def __init__(self):
        rospy.init_node('rover_controller', anonymous=True)
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.move_cmd = Twist()
        self.rate = rospy.Rate(10)
        rospy.loginfo("RoverController initialized")

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {e}")
            return

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([100, 25, 25])
        upper_bound = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(max_contour)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                error_x = cx - cv_image.shape[1] / 2

                self.move_cmd.linear.x = 0.1
                self.move_cmd.angular.z = -0.01 * error_x
                self.publisher.publish(self.move_cmd)

                if abs(error_x) < 20:
                    rospy.loginfo("Object centered, stopping rover")
                    self.stop_rover()

                rospy.loginfo(f"Object detected at ({cx}, {cy}), error_x: {error_x}")
            else:
                rospy.loginfo("No valid contours found")
        else:
            rospy.loginfo("No objects detected")
        
        self.display_image(cv_image)

    def stop_rover(self):
        """Stop the rover when the object is centered."""
        self.move_cmd.linear.x = 0.0
        self.move_cmd.angular.z = 0.0
        self.publisher.publish(self.move_cmd)
        rospy.loginfo("Rover stopped. Ready for manipulator control.")

    def display_image(self, image):
        """Display the image in a window."""
        cv2.imshow("Camera Feed", image)
        cv2.waitKey(1)

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        rover_controller = RoverController()
        rover_controller.spin()
    except rospy.ROSInterruptException:
        pass

# Helper functions
def init_rospy():
    """Initialize the ROS node."""
    rospy.init_node('rover_controller', anonymous=True)
    rospy.loginfo("ROS node initialized")

def create_publisher():
    """Create a ROS publisher for the cmd_vel topic."""
    return rospy.Publisher('cmd_vel', Twist, queue_size=10)

def create_subscriber(callback):
    """Create a ROS subscriber for the camera topic."""
    return rospy.Subscriber('camera/rgb/image_raw', Image, callback)

def create_cv_bridge():
    """Create a CvBridge object."""
    return CvBridge()

def image_processing(image):
    """Process the image to find the object."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([100, 25, 25])
    upper_bound = np.array([140, 255, 255])
    return cv2.inRange(hsv, lower_bound, upper_bound)

def find_contours(mask):
    """Find contours in the given mask."""
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_max_contour(contours):
    """Get the contour with the maximum area."""
    return max(contours, key=cv2.contourArea) if contours else None

def calculate_moments(contour):
    """Calculate the moments of the given contour."""
    return cv2.moments(contour)

def calculate_error(cx, width):
    """Calculate the error between the object's center and the image center."""
    return cx - width / 2

def main():
    """Main function to run the rover controller."""
    try:
        rover_controller = RoverController()
        rover_controller.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
