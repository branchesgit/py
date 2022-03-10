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

class Line:
    def __init__(self, start, h):
        self.start = start
        self.h = h
        self.areaRate = 0.0    


def remove_too_large_gap_line(lines):
    gaps = get_gaps(lines)
    c_pags = [i for i in gaps]
    ws = get_line_widths(lines)
    gaps.sort()
    print('remove gaps', gaps)
    l = len(gaps)
    max_value =  gaps[l - 1]
    total = sum(gaps) - max_value
    avg = total / (l - 1)
    avg += gaps[0]    
    for i in range(len(gaps)):
        print('i')
        

def get_line_widths(list):
    ws = []
    for i in list:
        ws.append(i.h)
    return ws


def get_gaps(lines):
    gaps = []
    print('get_gaps size', len(lines))
    for i in range(len(lines)):
        if i >= 1:
            gap = lines[i].start - lines[i-1].start -lines[i-1].h
            gaps.append(gap)
    return gaps

