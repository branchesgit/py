from classifier import Classifier
import cv2
from rect import get_gaps, Choice
from util.projection import Y_Project, X_Project, get_rects
from util.data import get_lines, get_max_value, filter_zero, split_list_to_group_idx, is_exist_min_value, \
    is_width_rate_of_change, remove_exception_line
import numpy as np
import os

class ChoiceClassifier(Classifier):
    pass

    # 先按选项是水平分布的，按层来划分.
    def classifier(self):
        
        points = self.convergency_rect()
        self.do_vertica(points)
    

    
    def do_vertica(self, points):

        x, y, width, height = self.rect
        [[x_start, y_start], [x_end, y_end]] = points
        part = self.mat[y + y_start: y + y_end, x + x_start: x + x_end]
        cv2.imwrite("./imgs/part.png", part)
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(part, cv2.MORPH_OPEN, kernel)
        w_w, v_projection = X_Project(part)
        height, width = part.shape
        print(height, width)
        cv2.imwrite("./imgs/x.png", v_projection)
        c_w_w = filter_zero(w_w)
        max_value = get_max_value(c_w_w)
        lines = get_lines(w_w, 1, max_value, height, False)
        remove_exception_line(lines, w_w)

        print('size is ', len(lines))
        for i in range(len(lines)):
            x_start = lines[i].start
            x_end = lines[i].h
            cv2.imwrite("./imgs/line_" + str(i + 1) + ".png", part[0: height, x_start: x_start + x_end]);

    # 收敛
    def convergency_rect(self):
        x, y, width, height = self.rect
        part = self.mat[y:y + height, x: x + width]
        ret, part = cv2.threshold(part, 120, 255, cv2.THRESH_BINARY)
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(part, cv2.MORPH_OPEN, kernel)
        h_h, h_projection = Y_Project(part)
        c_w_w = filter_zero(h_h)
        max_value = get_max_value(c_w_w)
        lines = get_lines(h_h, 1, max_value, width, False)
        y_start = lines[0].start
        y_end = lines[len(lines) - 1].start + lines[len(lines) - 1].h

        w_w, v_projection = X_Project(part)
        c_w_w = filter_zero(w_w)
        max_value = get_max_value(c_w_w)
        lines = get_lines(w_w, 1, max_value, height, False)
        x_start = lines[0].start
        x_end = lines[len(lines) - 1].start + lines[len(lines) - 1].h
        # self.mat = part
        return [[x_start, y_start], [x_end, y_end]]

    def do_horization(self, points):
        x, y, width, height = self.rect
        [[x_start, y_start], [x_end, y_end]] = points
        part = self.mat[y + y_start: y + y_end, x + x_start: x + x_end]

        cv2.imwrite('./imgs/part_.png', part)
        height, width = part.shape
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(part, cv2.MORPH_OPEN, kernel)
        h_h, h_projection = Y_Project(part)
        # cv2.imwrite('./imgs/yy_.png', h_projection)
        c_h_h = filter_zero(h_h)
        max_value = get_max_value(c_h_h)
        lines = get_lines(h_h, 1, max_value, width, False)
        idx = 0

        options = []
        blocks = []
        for line in lines:
            layer_mat = part[line.start:line.start + line.h, 0:width]
            groups, lines = self.get_layer_desc(layer_mat, idx)
            idx += 1
            count = 0
            row_blocks = []
            if len(groups):
                choice_block_idx = 0
                for g_idx in range(len(groups)):
                    group = groups[g_idx]
                    group_len = len(group)
                    if group_len:
                        group_lines = lines[count: count + group_len]
                        h_start = group_lines[0].start
                        h_end = group_lines[len(group_lines) - 1].start + group_lines[len(group_lines) - 1].h
                        if g_idx == len(groups) - 1:
                            h_end = width
                        choice_mat = layer_mat[0: line.h, h_start: h_end]
                        row_blocks.append([h_start, h_end])
                        choice_x = x + x_start + h_start
                        choice_y = y + y_start + line.start
                        options.append(Choice(choice_x, choice_y, h_end - h_start, line.h, group_lines))
                        # cv2.imwrite("./imgs/choice_" + str(idx) + "_" + str(choice_block_idx) + ".png", choice_mat)
                        choice_block_idx += 1
                        count += group_len
                blocks.append(row_blocks)

            cv2.imwrite("./imgs/or.png", self.mat)
            idx = 0
            for choice in options:
                idx += 1
                number_item = choice.number_item
                item_mark = choice.item_mark
                cv2.imwrite("./imgs/c_" + str(idx) + ".png", self.mat[item_mark.y: item_mark.y + item_mark.h,
                                                             item_mark.x: item_mark.x + item_mark.w])
                cv2.imwrite("./imgs/numbers/" + self.file_name + "_" + str(idx) + ".png", self.mat[number_item.y: number_item.y + number_item.h,
                                                             number_item.x: number_item.x + number_item.w])

    # 获取每一层的信息. 数字和选项的分类判断.
    def get_layer_desc(self, mat, index):
        cv2.imwrite("./imgs/layer_" + str(index + 1) + ".png", mat)

        count = 0
        while True:
            # 防止死循环
            if count >= 20:
                break
            w_w, v_projection = X_Project(mat)
            cv2.imwrite("./imgs/y_projection_" + str(index) + ".png", v_projection)
            c_w_w = filter_zero(w_w)
            max_value = get_max_value(c_w_w)
            height, width = mat.shape
            lines = get_lines(w_w, 1, max_value, height, False)
            gaps = get_gaps(lines)
            if not is_exist_min_value(gaps, 2):
                break
            # 找到合适的间隙，进行膨胀.
            gap = 2
            # print(gaps, gap, 1)
            kernel = np.ones((gap, gap), np.uint8)
            mat = cv2.erode(mat, kernel)
            w_w, v_projection = X_Project(mat)
            cv2.imwrite('./imgs/erode_' + str(count) + ".png", v_projection)
            c_w_w = filter_zero(w_w)
            count += 1
            max_value = get_max_value(c_w_w)
            lines = get_lines(w_w, 1, max_value, height, False)
            gaps = get_gaps(lines)

            if not is_exist_min_value(gaps, 2):
                break

        split_list = split_list_to_group_idx(gaps)
        print('file_name', self.file_name, '===', split_list)
        return split_list, lines


path = "D:/study/py/imgs/"

if __name__ == '__main__':
    img = cv2.imread(path + "DN0114000003.TIF", 0)
    choiceClassifier = ChoiceClassifier(img, (184, 721, 1143, 123), "DN0114000003")
    choiceClassifier.classifier()

# if __name__ == '__main__':
#     files = os.listdir(path)  # 获得文件夹中所有文件的名称列表
#     for file in files:
#         i = 0
#         skip_zero = True
#         idx = -1
#         end = -1
#         while i < len(file):
#             value = file[i: i+1]
#             i += 1
#             if skip_zero:
#                 if '0' < value <= '9':
#                     if idx == -1:
#                         skip_zero = False
#                         idx = i
#             else:
#                 if not ('0' <= value <= '9'):
#                     if end == -1:
#                         end = i - 1

#         value = file[idx: end]
#         if int(value) % 2 == 1:
#             file = path + file
#             img = cv2.imread(file, 0)
#             img = np.rot90(img)
#             choiceClassifier = ChoiceClassifier(img, (102, 825, 999, 203), value)
#             # 103 824, 1011, 211
#             # choiceClassifier = ChoiceClassifier(img, (103, 824, 1011, 211), value)
#             choiceClassifier.classifier()
    


