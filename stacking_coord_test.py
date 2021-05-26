#!/usr/bin/python3
# coding=utf8


import Camera_Motion
import CameraPerception

import sys

sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera


def test_motion(target_color='red'):
    goal_coordinates = {
        'BL': (-14, -10.5, 1.5),
        'BM': (-14, -7.5, 1.5),
        'BR': (-14, -4.5, 1.5),
        'ML': (-14, -10.5, 4.5),
        'MM': (-14, -7.5, 4.5),
        'MR': (-14, -4.5, 4.5),
        'TL': (-14, -10.5, 7.5),
        'TM': (-14, -7.5, 7.5),
        'TR': (-14, -4.5, 7.5)
    }

    my_camera = Camera.Camera()
    my_camera.camera_open()
    img = my_camera.frame
    camera_perception = CameraPerception.Perception()
    camera_motion = Camera_Motion.MoveBlock()

    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame, coordinates, rect = camera_perception.main(frame)
            cv2.imshow('Frame', Frame)
            print(f'\n\n MADE IT    Coordinates:  {coordinates} \n\n')
            print(f'\n\n target loc: {coordinates[0]}, {coordinates[1]}, 1.5 \n\n')
            camera_motion.main(target_loc=(coordinates[0], coordinates[1], 1.5),
                               goal_loc=goal_coordinates['BL'], rect=rect)
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