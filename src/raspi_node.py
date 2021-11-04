#!/usr/bin/env python3
import serial
import rospy
from std_msgs.msg import Int8MultiArray
#this program is designed to send serial commands to the arduino, and eventually to the Braccio robot
#it now also has ROS integration - it is subscribed to the topic "move_cmd" with the listen() function

class BraccioRobot:
    '''This is the initialization function, it opens the serial port.'''
    def __init__(self):
        #this try/except statement should find the device name of the serial port
        try:
            self.ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)
        except FileNotFoundError:
            self.ser = serial.Serial('/dev/ttyACM1',9600, timeout=1)
        self.ser.flush() #flushes the incoming serial buffer, but not necessary (useful for duplex)
        rospy.init_node('robot_cmd_sub', anonymous=True) #creates a subscriber node called 'listener'
        self.params = [20, 90, 90, 90, 90, 90, 10] #initializes params sent to robot with arm straight up

    '''This function sends a movement command with its current params.'''
    def primitive_move(self):
        command = str(self.params[0]) + ' ' #initializes command with step size
        #iterates through the rest of params, converting to string and adding preceding '0's
        for sub_param in self.params[1:]:
            sub_param = str(sub_param)
            sub_param = (3-len(sub_param))*'0' + sub_param #makes sure each sub_command is 3 char long
            command = command + sub_param + ' '
        self.ser.write(command.encode('ascii')) #writes command to the serial port

    '''This is a more refined movement command that can take in any number of movements.
    If nothing is passed to it, it simply points to the primitive_move() function'''
    def move(self, *params_list):
        #deals with the number of params in params list
        if isinstance(params_list[0], int): #only 1 set of params is passed into params_list
            self.params = params_list
            self.primitive_move()
        elif len(params_list) != 0: #params_list has multiple sets of params
            #iterates through the each set of params in params_list and sends movement commands
            for params in params_list:
                self.params = params
                self.primitive_move()
        else: #no params were passed to move(), so just uses primitive_move() on current self.params
            self.primitive_move()

    '''This function gets params from the user and enters into self.params'''
    def userinput(self):
        #iterates through the 7 parameters and asks user for each one
        for i in range(7):
            self.params[i] = int(input("enter param " + str(i) + ": "))

    '''This is a callback function for the subscriber to '''
    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + ": " + str(data.data)) #logs input data to terminal
        self.move(data.data) #calls move function on data

    '''This function creates a subscriber to the 'move_cmd' topic'''
    def listen(self):
        rospy.loginfo("Listening...") #logs to terminal
        rospy.Subscriber("/move_cmd", Int8MultiArray, self.callback) #subscribes to 'move_cmd', with data type and callback
        rospy.spin() #prevents exit until node is destroyed

if __name__ == '__main__':
    Braccio = BraccioRobot()
    Braccio.listen()
    '''to test node, use the following:
    rostopic pub -r 1  /move_cmd std_msgs/Int8MultiArray '{data:  [20, 90, 90, 90, 90, 90, 73]}'''