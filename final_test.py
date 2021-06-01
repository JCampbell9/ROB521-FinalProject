#!/usr/bin/python3
# coding=utf8


import Camera_Motion
import CameraPerception

import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import json
import os


direct = os.getcwd()
# print(direct)


class LetterStacker:

    def __init__(self):
        self.my_camera = Camera.Camera()
        self.my_camera.camera_open()
        self.img = self.my_camera.frame
        self.camera_perception = CameraPerception.Perception()
        self.camera_motion = Camera_Motion.MoveBlock()
        self.goal_loc, self.letter_list = self.read_json()

    def main(self, letter="H"):
        letter_order = self.letter_list[letter]
        for r in range(3):
            for c in range(3):
                self.place_block(letter_order[r][c], self.goal_loc[r][c])

    def place_block(self, block_color, goal_loc):
        self.img = self.my_camera.frame
        if block_color == "skip":
            return False
        while True:
            self.img = self.my_camera.frame
            if self.img is not None:
                frame = self.img.copy()
                Frame, coordinates, rect = self.camera_perception.main(frame, (block_color))
                cv2.imshow('Frame', Frame)
                print(f'\n\n MADE IT    Coordinates:  {coordinates} \n\n')
                print(f'\n\n target loc: {coordinates[0]}, {coordinates[1]}, 1.5 \n\n')
                self.camera_motion.main(target_loc=(coordinates[0], coordinates[1], 1.5),
                                   goal_loc=goal_loc, rect=rect)
                break
        self.my_camera.camera_close()
        cv2.destroyAllWindows()

    def read_json(self):

        with open(f'{direct}/stacking_info.json', 'r') as read_file:
            stacking_info = json.load(read_file)

        goal_coordinates = stacking_info["goal_coordinates"]
        letter_order = stacking_info["letters"]

        return goal_coordinates, letter_order

        # print(f'\n\n {goal_coordinates} \n\n  {letter_order["H"]} \n\n')

        # letter_h = letter_order["H"]
        #
        # for r, row in enumerate(goal_coordinates):
        #     for c, col in enumerate(row):
        #         print(f'block color: {letter_h[r][c]},   block location: {col}')


def add_letter():

    key = input('what is the new letter you want to add?')
    new_letter = []
    locations = [['bottom left', 'bottom middle', 'bottom right'], ['middle left', "middle middle", "middle right"],
                 ['top left', "top middle", 'top right']]
    for i in locations:
        row = []
        for loc in i:

            locat = input(f'write the color of the block(red or other): {loc} locations: ')
            row.append(locat)
        new_letter.append(row)


def write_json(updated_letter_list):
    with open(f'{direct}/stacking_info.json', 'w') as write_file:
        json.dump(updated_letter_list, write_file, indent=4)



if __name__ == '__main__':

    func = LetterStacker()
    func.main("single_stack")

# print(stacking_info)