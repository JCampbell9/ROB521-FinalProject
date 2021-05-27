#!/usr/bin/python3
# coding=utf8


import Camera_Motion
import CameraPerception

import sys

sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera


def test_motion():

    # Current plan:
    # Call letter_dict['letter'][goal_coords[pos]] --> color needed
    # Search for color
    # Grab block
    # Move to goal location
    # Increment goal locations to next space to fill
    # Fill spaces bottom to top, left to right

    goal_coordinates = {
        'BL': (-14, -7.5, 1.5),
        'BM': (-14, -4.5, 1.5),
        'BR': (-14, -1.5, 1.5),
        'ML': (-14, -7.5, 4.5),
        'MM': (-14, -4.5, 4.5),
        'MR': (-14, -1.5, 4.5),
        'TL': (-14, -7.5, 7.5),
        'TM': (-14, -4.5, 7.5),
        'TR': (-14, -1.5, 7.5)
    }
    letter_dict = {
        'C':{goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'red',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'red',
         goal_coordinates['MM']: 'green',
         goal_coordinates['MR']: 'blue',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'red',
         goal_coordinates['TR']: 'red'},
        'H': {goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'blue',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'red',
         goal_coordinates['MM']: 'red',
         goal_coordinates['MR']: 'red',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'green',
         goal_coordinates['TR']: 'red'},
         'I': {goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'red',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'blue',
         goal_coordinates['MM']: 'red',
         goal_coordinates['MR']: 'green',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'red',
         goal_coordinates['TR']: 'red'},
        'N': {goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'blue',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'red',
         goal_coordinates['MM']: 'green',
         goal_coordinates['MR']: 'red',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'red',
         goal_coordinates['TR']: 'red'},
        'O': {goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'red',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'red',
         goal_coordinates['MM']: 'blue',
         goal_coordinates['MR']: 'red',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'red',
         goal_coordinates['TR']: 'red'},
        'U': {goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'red',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'red',
         goal_coordinates['MM']: 'blue',
         goal_coordinates['MR']: 'red',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'green',
         goal_coordinates['TR']: 'red'},
        'Z': {goal_coordinates['BL']: 'red',
         goal_coordinates['BM']: 'red',
         goal_coordinates['BR']: 'red',
         goal_coordinates['ML']: 'blue',
         goal_coordinates['MM']: 'red',
         goal_coordinates['MR']: 'green',
         goal_coordinates['TL']: 'red',
         goal_coordinates['TM']: 'red',
         goal_coordinates['TR']: 'red'}
        }


    my_camera = Camera.Camera()
    my_camera.camera_open()
    img = my_camera.frame
    camera_perception = CameraPerception.Perception()
    motion = Camera_Motion.MoveBlock()

    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame, coordinates, rect = camera_perception.main(frame)
            cv2.imshow('Frame', Frame)
            print(f'\n\n MADE IT    Coordinates:  {coordinates} \n\n')
            print(f'\n\n target loc: {coordinates[0]}, {coordinates[1]}, 1.5 \n\n')
            print('\n step initial pose \n')
            motion.init_pose()
            print('\n move above block \n')
            # move above the target block
            if not motion.move_arm((coordinates[0], coordinates[1], 6), time_delay=False):
                print("target location is unreachable")
                return False
            print('\n open gripper \n')

            # get the gripper ready to pick up block
            motion.open_gripper()
            print('\n angle gripper \n')
            motion.angle_gripper((coordinates[0], coordinates[1], rect[2]))
            # Grab the block
            print('\n lower arm \n')
            motion.move_arm((coordinates[0], coordinates[1], 1.5), time_delay=1.5)
            print('\n close gripper \n')
            motion.close_gripper()
            # lift block up
            print('\n lift block up')
            motion.move_arm((coordinates[0], coordinates[1], 11.5), time_delay=1.5)
            print('\n lift block up')
            goal_loc = goal_coordinates['BR']
            # goal_loc = (-15 + 1, -7 - 0.5, 1.5)
            print(f'\n\n goal loc: {goal_loc} \n\n')
            # move block above goal location
            motion.move_arm((goal_loc[0], goal_loc[1], goal_loc[2] + 8), time_delay=1.5)
            # properly angle gripper
            motion.angle_gripper((goal_loc[0], goal_loc[1], 0))
            # lower the gripper to 3cm above the final z
            motion.move_arm((goal_loc[0], goal_loc[1], goal_loc[2] + 3), time_delay=1.5)
            # set block down
            motion.move_arm(goal_loc, time_delay=1.5)
            motion.open_gripper()
            motion.move_arm((goal_loc[0], goal_loc[1], goal_loc[2] + 10), time_delay=1.5)
            motion.init_pose()
            break


def camera_test():
    my_camera = Camera.Camera()
    my_camera.camera_open()
    img = my_camera.frame
    camera_perception = CameraPerception.Perception()
    i = 0
    while True:

        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame, coordinates, _ = camera_perception.main(frame)
            cv2.imshow('Frame', Frame)
            print(f'\n Loop: {i}  Coordinates:  {coordinates} \n')
            key = cv2.waitKey(1)
            if key == 27:
                break
        # print(f'\n loop: {i}  Coordinates:  {coordinates} \n')
        i += 1
    my_camera.camera_close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test_motion()
    # camera_test()
