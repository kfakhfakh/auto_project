#!/usr/bin/env python3
import rospy
from autonome.srv import cmd
from autonome.msg import Pose
from service import send_srv
import math
import time

robot_off=False
def setSpacingEncoder(spacing):
    message=cmd()
    message.cmd="setSpacingEncoder"
    message.x=spacing
    feedback = send_srv(message)

    
def setCoeffs(kp, ki ,kb):
    message=cmd()
    message.cmd="setCoeffs"
    message.x=kp
    message.y=ki
    message.phi=kb
    feedback = send_srv(message)
    
    return feedback

def setRadius(R, L):
    message=cmd()
    message.cmd="setRadius"
    message.x=R
    message.y=L
    feedback = send_srv(message)
    
    return feedback

def setCoords(x, y, phi):
    message=cmd()
    message.cmd="setCoords"
    message.x=x
    message.y=y
    message.phi=phi
    feedback = send_srv(message)
    return feedback
def moveDistance(dist, speed):
    global  curr_phi,curr_x, curr_y,robot_off
    
    while True:
        if robot_off:
            return
        message=cmd()
        message.cmd="moveDistance"
        message.x=dist
        message.speed=speed
        feedback = send_srv(message)
        if feedback.success:
            break

def robotLocate(x, y, speed):
    if robot_off:
        return
    global curr_x, curr_y, curr_phi, switch
    time.sleep(0.1)
    message=cmd()
    message.cmd="robotLocate"
    message.x=x
    message.y=y
    message.speed=speed
    feedback = send_srv(message)
    if feedback.success:
        return feedback
    #setCoords(curr_x, curr_y, curr_phi)
    pos = [curr_x, curr_y]
    dist = math.sqrt((pos[0]-x)**2+(pos[1]-y)**2)
    return moveDistance(dist, speed)

def rotate(phi, speed):
    if robot_off:
        return
    message=cmd()
    message.cmd="rotate"
    message.phi=phi
    message.speed=speed
    feedback = send_srv(message)
    
    return feedback

def orientate(phi, speed):
    global curr_x, curr_y, curr_phi, switch
    time.sleep(0.1)
    if robot_off:
        return
    message=cmd()
    message.cmd="orientate"
    message.phi=phi
    message.speed=speed
    feedback = send_srv(message)
def pwm():
    message=cmd()
    message.cmd="pwm"
    feedback = send_srv(message)
def test():
    message=cmd()
    message.cmd="test"
    feedback = send_srv(message)

def sub_callback(message:Pose):
    global curr_x, curr_y, curr_phi
    curr_x=message.x
    curr_y=message.y
    curr_phi=message.phi
    return True
if __name__ == '__main__':
    global curr_x, curr_y
    print("Started")
    rospy.init_node("ros_autonome")
    rospy.Subscriber("position",Pose,sub_callback)
    #sequence houni 
    x=0