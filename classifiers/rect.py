class Rect: 
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = w * h


def sort_y(rect):
    return rect.y


def sort_x(rect):
    return rect.x
