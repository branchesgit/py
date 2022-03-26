import cv2
import math
from util.projection import X_Project
from util.data import get_lines, get_max_value, get_value_index, get_index


def sort_y(rect):
    x, y, w, h = rect
    return x


class OptionClassifier:
    def classifier(self, mat):
        self.cuttingOptions(mat)

    def cuttingOptions(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        height, width = gray.shape
        cnts, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        list = []
        for cnt in cnts:
            # 外接矩形框，没有方向角
            x, y, w, h = cv2.boundingRect(cnt)
            if w < width / 2 and h > 3:
                list.append((x, y, w, h))
                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
                cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 0), -1)

        cv2.imwrite("./imgs/c_4.png", gray)
        list.sort(key=sort_y)
        rates = []
        for rect in list:
            x, y, w, h = rect
            rates.append(h / w)

        w_w, x_project = X_Project(gray)
        lines = get_lines(w_w, 1, height, height, False)
        line_list = len(lines) - 1
        h_w_rates = []
        while line_list:
            line = lines[line_list]
            h_w_rates.append(line.total / line.h / line.h)
            line_list -= 1

        print(h_w_rates)
        lines.reverse()
        merge_lines = []
        exceptions = []
        useIdxs = []
        if len(h_w_rates) > 5:
            for idx in range(len(h_w_rates)):
                rate = h_w_rates[idx]
                if rate < 0.85 or rate > 1.6:
                    continue

                use_idx = -1
                for useIdx in useIdxs:
                    if useIdx == idx:
                        use_idx = 0
                        break

                if use_idx != -1:
                    continue

                is_right_line = False
                is_left_line = False
                right_line = []
                left_line = []
                line = lines[idx]

                cv2.rectangle(gray2, (line.start, 0), (line.start + line.h, height), (0, 0, 255), -1)
                # 向两边搜索.
                if idx > 0:
                    right_line = lines[idx - 1]
                    is_right_line = self.is_line(gray2[0: height, right_line.start: right_line.start + right_line.h],
                                                 idx,
                                                 1)

                if idx < len(h_w_rates) - 1:
                    left_line = lines[idx + 1]
                    is_left_line = self.is_line(gray2[0: height, left_line.start: left_line.start + left_line.h], idx,
                                                0)

                print(is_right_line, is_left_line, line.start, line.h)
                if is_right_line and is_left_line:
                    useIdxs.append(idx - 1)
                    useIdxs.append(idx)
                    useIdxs.append(idx + 1)
                    merge_lines.append([left_line.start, right_line.start + right_line.h])
                    cv2.rectangle(img, (left_line.start, 0), (right_line.start + right_line.h, height), (255, 0, 0), 1)

                else:
                    if is_left_line:
                        useIdxs.append(idx - 1)
                        useIdxs.append(idx)
                        useIdxs.append(idx + 1)
                        merge_lines.append([left_line.start, right_line.start + left_line.h + 2])
                        exceptions.append([right_line.start + left_line.h + 2, right_line.h])
                        cv2.rectangle(img, (left_line.start, 0), (right_line.start + right_line.h, height), (0, 120, 0),
                                      1)
                    else:
                        if is_right_line:
                            useIdxs.append(idx - 1)
                            useIdxs.append(idx)
                            useIdxs.append(idx + 1)
                            merge_lines.append(
                                [left_line.start + left_line.h - right_line.h - 2, right_line.start + right_line.h])
                            exceptions.append([left_line.start, left_line.start + left_line.h - right_line.h - 2])
                            cv2.rectangle(img, (left_line.start + left_line.h - right_line.h - 2, 0),
                                          (right_line.start + right_line.h, height),
                                          (0, 255, 0), 1)

        for idx in range(len(exceptions)):
            ary = exceptions[idx]
            cv2.rectangle(img, (ary[0], 0), (ary[1], height), (0, 0, 255), 1)

        for idx in range(len(lines)):
            i = -1
            for __idx__ in range(len(useIdxs)):
                if useIdxs[__idx__] == idx:
                    i = __idx__
                    break
            if i == -1:
                cv2.rectangle(img, (lines[idx].start, 0), (lines[idx].start + lines[idx].h, height), (0, 0, 255), 1)

        print(exceptions, len(lines))
        cv2.imwrite("./imgs/c_5.png", img)
        cv2.imwrite("./imgs/c_5_1.png", gray2)

    def is_line(self, mat, idx, direction):

        # cv2.imwrite("./imgs/line_" + str(idx) + "_" + str(direction) + ".png", mat)
        w_w, x_project = X_Project(mat)
        while w_w[-1] == 0:
            w_w = w_w[0: len(w_w) - 2]
        while w_w[0] == 0:
            w_w = w_w[1:]
        middle = math.ceil(len(w_w) / 2)
        left_sum = 0
        right_sum = 0
        c_w = [i for i in w_w]
        max_value = get_max_value(c_w)

        height, width = mat.shape
        for idx in range(middle):
            left_sum += w_w[idx]
            right_sum += w_w[len(w_w) - 1 - idx]

        isTrue = False
        if direction == 1:
            isTrue = right_sum > left_sum
        else:
            isTrue = left_sum > right_sum

        if isTrue:
            return len(w_w) <= 12
        else:
            return isTrue


# path = "./imgs/op_1.png"
path = "D:/sb/10500/op_10.png"
path = "./imgs/er_3.png"
if __name__ == "__main__":
    img = cv2.imread(path)
    classifier = OptionClassifier()
    classifier.classifier(img)
