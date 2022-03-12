class Rect: 
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = w * h


class Line:
    def __init__(self, start, h):
        self.start = start
        self.h = h
        self.areaRate = 0.0    


def get_gaps(lines):
    gaps = []
    for i in range(len(lines)):
        if i >= 1:
            gap = lines[i].start - lines[i-1].start -lines[i-1].h
            gaps.append(gap)
    return gaps


class Choice:
    def __init__(self, x, y, w, h, lines):
        self.number = 1
        self.number_item = self.get_number_item(x, y, lines, h)
        self.item_mark = self.get_item_mark(x, y, w, h)

    def get_number_item(self, x, y, lines, h):
        line = lines[0]
        w = line.h
        return Rect(x - 3, y, w + 6, h)

    def get_item_mark(self, x, y, w, h):
        return Rect(x, y, w, h)

