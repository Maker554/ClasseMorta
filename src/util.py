import sys
import os

def align(position, object, mode: str):

    if mode == "bottom_left":
        return (position[0], position[1] - object.get_height())
    if mode == "top_right":
        return (position[0] - object.get_width(), position[1])
    if mode == "bottom_right":
        return (position[0] - object.get_width(), position[1] - object.get_height())
    if mode == "center":
        return (position[0] - object.get_width() / 2, position[1] - object.get_height() / 2)
    if mode == "top_center":
        return (position[0] - object.get_width() / 2, position[1])
    if mode == "bottom_center":
        return (position[0] - object.get_width() / 2, position[1] - object.get_height())

    return position

def align_x(position, object_length, mode: str):

    if mode == "top_right" or mode == "bottom_right":
        return position - object_length
    if mode == "center" or mode == "bottom_center" or mode == "top_center":
        return position - object_length / 2

    return position


def align_y(position, object_height, mode: str):
    if mode == "bottom_left" or mode == "bottom_right" or mode == "bottom_center":
        return position - object_height
    if mode == "center":
        return position - object_height / 2

    return position

def media(list):
    media = 0
    for i in list:
        media += i
    if len(list) > 0:
        return media / len(list)
    else:
        return 0


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)