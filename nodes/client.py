#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from punto3.srv import *
from std_srvs import Empty

def start_turtlesim_snake_client():
    rospy.wait_for_service('start_turtlesim_snake')
    try:
        start_turtlesim_snake = rospy.ServiceProxy('start_turtlesim_snake', Empty)
        start_turtlesim_snake()
        return 
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        cadena = str(sys.argv[1])
        if (cadena == 'start_turtlesim_snake'):
            start_turtlesim_snake_client()