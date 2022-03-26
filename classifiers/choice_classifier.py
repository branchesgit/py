from classifier import Classifier
import cv2
from rect import get_gaps, Choice
from util.projection import Y_Project, X_Project, get_rects
from util.data import get_lines, get_max_value, filter_zero, split_list_to_group_idx, is_exist_min_value, \
    is_width_rate_of_change, remove_exception_line, get_value_index
import numpy as np
import os


class ChoiceClassifier(Classifier):
    pass

    # 先按选项是水平分布的，按层来划分.
    def classifier(self):
        points = self.convergency_rect()
        self.is_horization(points)
        #self.do_horization(points)


    def get_mat_gap(self, layer, row):
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(layer, cv2.MORPH_OPEN, kernel)
        gap = 0
        w_w, x_project = X_Project(layer)
        height, width = layer.shape
        w_lines = get_lines(w_w, 1, width, 0, False)
        w_gaps = get_gaps(w_lines)
        split_groups = split_list_to_group_idx(w_gaps)
        # find min length.
        if len(split_groups) > 0:
            __idx = -1
            l = 0
            for idx in range(len(split_groups)):
                if l == 0:
                    l = len(split_groups[idx])
                    __idx = idx

                if len(split_groups[idx]) < l:
                    l = len(split_groups[idx])
                    __idx = idx

            if __idx != -1:
                idx__ = 0
                for i in range(__idx):
                    idx__ += len(split_groups[i])
                s_line = w_lines[idx__]
                e_line = w_lines[idx__ + len(split_groups[__idx])]
                if __idx != len(split_groups) - 1:
                    e_line = w_lines[idx__ + len(split_groups[__idx]) - 1]

                block_mat = layer[0: height, s_line.start: e_line.start + e_line.h]
                height, width = block_mat.shape
                w_w, x_project = X_Project(block_mat)
                w_lines = get_lines(w_w, 1, width, 0, False)
                gaps = get_gaps(w_lines)

                if not self.is_choice_closed(w_lines):
                    gap = -1
                    ws = []
                    for line in w_lines:
                        ws.append(line.h)
                    c_ws = [i for i in ws]
                    max_w = get_max_value(c_ws)
                    idx__ = get_value_index(max_w, ws)

                    __i__ = idx__ + 1
                    ws__ = []
                    total = 0
                    while __i__ < len(w_lines):
                        if __i__ == idx__ + 1:
                            ws__.append(w_lines[__i__].h)
                            total += w_lines[__i__].h
                        else:
                            gap = w_lines[__i__].start - w_lines[__i__ - 1].h - w_lines[__i__ - 1].start
                            w = w_lines[__i__].h
                            total += gap
                            total += w
                            ws__.append(gap)
                            ws__.append(w)
                        if total > max_w:
                            break
                        __i__ += 1

        if len(ws__) == 5:
            gap = max(ws__[1], ws__[3])
        if gap == -1 and len(ws__):
            ws__.sort()
            gap = ws__[0]
        return gap

    # 判断选项是否封闭.
    def is_choice_closed(self, w_lines):
        ws = []
        for line in w_lines:
            ws.append(line.h)

        c_ws = [i for i in ws]
        max_w = get_max_value(c_ws)
        count = 0
        for w in ws:
            if w / max_w >= 0.5:
                count += 1

        return count > 2

    def is_horization(self, points):
        x, y, width, height = self.rect
        [[x_start, y_start], [x_end, y_end]] = points
        part = self.mat[y + y_start: y + y_end, x + x_start: x + x_end]
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(part, cv2.MORPH_OPEN, kernel)
        # 取两层：
        h_h, y_project = Y_Project(part)
        height, width = part.shape
        lines = get_lines(h_h, width / 40, width, width, False)
        if len(lines) >= 3:
            layer1 = part[lines[0].start : lines[0].start + lines[0].h, 0: width]
            layer2 = part[lines[1].start: lines[1].start + lines[1].h, 0: width]

    def get_near_choice(self, w_lines, idx, max_w, layer, row):
        nears = []
        __idx = idx - 1
        l_h, l_w = layer.shape
        if __idx > 1:
            __start = w_lines[__idx].start
            __w = w_lines[__idx].h
            __start = __start - (max_w - __w)
            some = layer[0:l_h, __start: __start + max_w + 2]
            cv2.imwrite("./imgs/s_" + str(row) + ".png", some)
            s_h, s_w = some.shape
            w_w, x_project = X_Project(some)
            c_w = [i for i in w_w]
            max_v = get_max_value(c_w)
            __lines = get_lines(w_w, 1, max_v, s_h, False)
            gaps = get_gaps(__lines)
            nears.append(gaps)

        __idx = idx + 1
        if __idx >= len(w_lines):
            __start = w_lines[__idx].start
            some = layer[0:l_h, __start: __start + max_w]
            cv2.imwrite("./imgs/s_2_" + str(row) + ".png", some)
            s_h, s_w = some.shape
            w_w, x_project = X_Project(some)
            c_w = [i for i in w_w]
            max_v = get_max_value(c_w)
            __lines = get_lines(w_w, 1, max_v, s_h, False)
            gaps = get_gaps(__lines)
            nears.append(gaps)

        return nears

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
                cv2.imwrite("./imgs/numbers/" + self.file_name + "_" + str(idx) + ".png",
                            self.mat[number_item.y: number_item.y + number_item.h,
                            number_item.x: number_item.x + number_item.w])

    # 获取每一层的信息. 数字和选项的分类判断.
    def get_layer_desc(self, mat, index):
        cv2.imwrite("./imgs/layer_" + str(index + 1) + ".png", mat)

        count = 0
        while True:
            # 防止死循环
            if count >= 10:
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
            gap = 5
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
    img = cv2.imread(path + "4.TIF", 0)
    choiceClassifier = ChoiceClassifier(img, (242, 800, 1272, 188), "4")
    choiceClassifier.classifier()
