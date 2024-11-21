#!/usr/bin/env python3
import rospy
from autonome.srv import cmd
stm_proxy=None
def send_srv(message):
    global stm_proxy
    if stm_proxy==None:
        rospy.wait_for_service('stm_cmd')    
        try:
            stm_proxy = rospy.ServiceProxy('stm_cmd', cmd , persistent=True)
        except: print("erreur") 
    try:   
        resp = stm_proxy(message)
        return resp
    except rospy.ServiceException as e:
        stm_proxy=None
        rospy.loginfo("Service call failed: %s" % e)
        
if __name__ == '__main__':
    x=0