#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/ArmPi/')
# sys.path.append('/Users/socce/Desktop/git_repos/RobotSystems_arm/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


class MoveBlock:
    """
    Class that moves the arm to given locations
    """
    def __init__(self):
        self.AK = ArmIK()

        self.gripper_close = 500

        self.goal_coordinates = {
            'red': (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5, 1.5),
            'blue': (-15 + 0.5, 0 - 0.5, 1.5),
            'stacking': (-15 + 1, -7 - 0.5, 1.5)
        }

    def main(self, target_loc, goal_loc, rect):
        """
        Runs the basic pick and place by giving the blocks location and desire goal location
        :param target_loc: where the block is located, (x,y,z)
        :param goal_loc: where the robot should drop the block, (x,y,z)
        :param rect: the rect from perception class used for angle sometimes
        :return:
        """
        # print('\n step initial pose \n')
        self.init_pose()
        # print('\n move above block \n')
        # move above the target block
        if not self.move_arm((target_loc[0], target_loc[1], target_loc[2]+3), time_delay=False):
            # print("target location is unreachable")
            return False
        # print('\n open gripper \n')

        # get the gripper ready to pick up block
        self.open_gripper()
        # print('\n angle gripper \n')
        self.angle_gripper((target_loc[0], target_loc[1], rect[2]))
        # Grab the block
        # print('\n lower arm \n')
        self.move_arm((target_loc[0], target_loc[1], target_loc[2]), time_delay=1.5)
        # print('\n close gripper \n')
        self.close_gripper()
        # lift block up
        # print('\n lift block up')
        self.move_arm((target_loc[0], target_loc[1], target_loc[2] + 10), time_delay=1)
        # move block above goal location
        self.move_arm((goal_loc[0], goal_loc[1], goal_loc[2] + 8), time_delay=False)
        # properly angle gripper
        self.angle_gripper((goal_loc[0], goal_loc[1], -90))
        # lower the gripper to 3cm above the final z
        self.move_arm((goal_loc[0], goal_loc[1], goal_loc[2] + 3), time_delay=1)
        # set block down
        self.move_arm(goal_loc, time_delay=0.5)
        self.open_gripper()
        self.move_arm((goal_loc[0], goal_loc[1], goal_loc[2] + 10), time_delay=0.8)
        self.init_pose()

    def init_pose(self):
        """
        Starting and ending pose
        :return:
        """
        Board.setBusServoPulse(1, self.gripper_close - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
        time.sleep(1.5)

    def open_gripper(self):
        """
        Opens the Gripper
        :return:
        """
        Board.setBusServoPulse(1, self.gripper_close - 280, 500)  # Paws open
        time.sleep(0.5)

    def angle_gripper(self, loc):
        """
        Sets the angle of the gripper based off the target location
        :param loc: target location (x,y,z)
        :return:
        """
        gripper_angle = getAngle(loc[0], loc[1], loc[2])
        Board.setBusServoPulse(2, gripper_angle, 500)
        time.sleep(0.8)

    def close_gripper(self):
        """
        Closes the gripper
        :return:
        """
        Board.setBusServoPulse(1, self.gripper_close, 500)  # Paws open
        time.sleep(0.8)

    def move_arm(self, target_loc, time_delay):
        """
        Moves the arm to a desired location
        :param target_loc: location to move arm to (x,y,z)
        :param time_delay: set time delay for arm moving, mseconds
        :return:
        """

        if time_delay == False:
            result = self.AK.setPitchRangeMoving(target_loc, -90, -90, 0)
            if result == False:
                return False
            time.sleep(result[2] / 1000)
        else:
            result = self.AK.setPitchRangeMoving(target_loc, -90, -90, 0, int(time_delay * 1000))
            if not result:
                return False
            time.sleep(time_delay)
        return True




if __name__ == '__main__':

    move = MoveBlock()

    move.main(target_loc=(2.06, 23.6, 1.5), goal_loc=(-15 + 0.5, 12 - 0.5, 1.5), rect=90)
#    move.init_pose()
