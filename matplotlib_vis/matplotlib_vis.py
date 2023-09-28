import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt 


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Odometry, '/rtk/odom', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning        
        self.x_cord = []
        self.y_cord = []
        
        self.declare_parameter('color', "red")
        self.delta_threshold = self.get_parameter('color').value
        self._parameter_callback = self.create_timer(1.0, self.parameter_callback)

    def parameter_callback(self):
        new_value = self.get_parameter('color').value
        if new_value != self.delta_threshold:
            self.get_logger().info(f"color changed from {self.delta_threshold} to {new_value}")
            self.delta_threshold = new_value

    def listener_callback(self, msg):
        global x_cord 
        global y_cord
        self.get_logger().info('I heard: "%s"' % msg)
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.x_cord.append(x)
        self.y_cord.append(y)

        plt.plot(self.x_cord, self.y_cord, color=self.delta_threshold)
        plt.draw() 
        plt.pause(0.01)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    plt.show(block=True)
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

