#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv
from std_srvs.srv import Empty

def handler(req):
    global flag_s
    flag_s = True
    return []

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    turtle_name = rospy.get_param('turtle', 'turtle2')
    

    turtle_vel = rospy.Publisher('%s/cmd_vel' % turtle_name, geometry_msgs.msg.Twist, queue_size=1)

    rate = rospy.Rate(10.0)

    flag = False
    flag_s = False

    
    server = rospy.Service('start_turtlesim_snake', Empty, handler)

    if(flag_s):
        while not rospy.is_shutdown():
            try:
                spawner(4, 2, 0, turtle_name)
                trans = tfBuffer.lookup_transform(turtle_name, 'turtle1', rospy.Time())
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rate.sleep()
                continue

            msg = geometry_msgs.msg.Twist()

            x_pose = trans.transform.translation.x
            y_pose = trans.transform.translation.y

            if (math.sqrt(x_pose ** 2 + y_pose ** 2)) < 1:
                flag = True

            if(flag):    
                msg.angular.z = 4 * math.atan2(y_pose, x_pose)
                msg.linear.x = 0.5 * math.sqrt(x_pose ** 2 + y_pose ** 2)

            turtle_vel.publish(msg)

            rate.sleep()
    

    
            
       