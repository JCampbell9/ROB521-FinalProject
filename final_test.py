#!/usr/bin/python3
# coding=utf8


import Camera_Motion
import CameraPerception
import os
direct = os.getcwd()

import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import json



class LetterStacker:
    """
    This class can be used to communicate with the Camera Perception and arm movement to stack blocks into a pattern to
    represent a letter
    """

    def __init__(self):
        self.my_camera = Camera.Camera()
        self.my_camera.camera_open()
        self.img = self.my_camera.frame
        self.camera_perception = CameraPerception.Perception()
        self.camera_motion = Camera_Motion.MoveBlock()
        self.goal_loc, self.letter_list = self.read_json()
        self.other_colors = ['green', "blue"]

    def main(self, letter="H"):
        """
        use to give a letter to be built from blocks
        :param letter: The letter to be built
        :return: None
        """
        letter_order = self.letter_list[letter]
        for r in range(3):
            for c in range(3):
                self.place_block(letter_order[r][c], self.goal_loc[r][c])

    def place_block(self, block_color, goal_loc):
        """
        uses the block color and goal location to move that specific block
        :param block_color: the color of block for camera perception to located
        :param goal_loc: The location to move the block once it is found
        :return: None
        """
        self.img = self.my_camera.frame
        if block_color == "skip":  # skip is used for testing single stacks
            return False
        elif block_color == "other":  # other is green and blue the color doesn't matter they are just non-red
            target_color = self.other_colors[0]  # set the remaining other color to the target color
            self.other_colors = self.other_colors[1:]
        else:  # set red as the target color
            target_color = block_color
        while True:
            self.img = self.my_camera.frame
            if self.img is not None:  # get the location of the target block from the camera
                frame = self.img.copy()
                Frame, coordinates, rect = self.camera_perception.main(frame, target_color)
                cv2.imshow('Frame', Frame)
                # send target and goal locations to the move class to pick and place the target block
                self.camera_motion.main(target_loc=(coordinates[0], coordinates[1], 1.5), goal_loc=goal_loc, rect=rect)
                break

    def read_json(self):
        """
        used to read in the json file which stores the goal locations and stacking order for each letter
        :return: the goal coordinates and the dictionary containing the color order for the letters
        """

        with open(f'{direct}/stacking_info.json', 'r') as read_file:
            stacking_info = json.load(read_file)

        goal_coordinates = stacking_info["goal_coordinates"]
        letter_order = stacking_info["letters"]

        return goal_coordinates, letter_order



def add_letter():
    """
    unneeded additional functionality
    :return: None
    """

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
    """
    unneeded additional functionality
    :return: None
    """
    with open(f'{direct}/stacking_info.json', 'w') as write_file:
        json.dump(updated_letter_list, write_file, indent=4)



if __name__ == '__main__':

    """Asks what letter to construct with the blocks"""
    letter = input('what letter to construct?    ')

    func = LetterStacker()
    func.main(letter) # sends the letter to the class to be built
