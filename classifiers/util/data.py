from rect import Line


def get_max_value(list):
    list_length = len(list)
    if list_length > 0:
        list.sort()
        return list[list_length - 1]
    else:
        return 0


def get_lines(list, w_min, w_max, w_h, is_print):
    lines = []
    start = -1
    h = 0
    total = 0
    rates = []
    for i in range(len(list)):
        value = list[i]
        if is_print:
            print(value, i)
        # 有值，且值满足要求.
        if value > w_min and value <= w_max:
            if is_print:
                print('if', start, h)
            if start == -1:
                start = i
                h = 1
                total = value
            else:
                h += 1
                total += value

            if i == len(list) - 1:
                if start != -1:
                    line = Line(start, h)
                    if w_h and h:
                        line.areaRate = total / (h * w_h)
                        line.total = total
                        rates.append(line.areaRate)
                        if (line.areaRate >= 0.05):
                            lines.append(line)
                    else:
                        lines.append(line)
                        #  当没有白色像素的时候，
        else:
            if is_print:
                print('else', start, h)
            if start == -1:
                continue
            else:
                line = Line(start, h)
                if w_h:
                    line.areaRate = total / (h * w_h)
                    line.total = total
                    rates.append(line.areaRate)
                    if (line.areaRate >= 0.05):
                        lines.append(line)
                else:
                    lines.append(line)
            start = -1
            h = 0

    return lines


def sortSum(list):
    return list[len(list) - 1]

# 找到小于0的连续数据.
def get_lower_zero_lines(list):
    lines = []
    start = -1
    some = []
    for idx in range(len(list)):
        if  list[idx] < 0:
            if start == -1:
                some = []
                some.append(idx)
                some.append(list[idx])
                start = idx
            else:
                some.append(list[idx])
        else:
            if len(some) > 0:
                sum = 0
                for i in range(len(some)):
                    if i > 0:
                        sum += some[i]
                some.append(sum)
                lines.append(some)
                start = -1
                some = []
    # 暂时不判断这种值的合法性.
    lines.sort(key=sortSum)
    return lines



def remove_exception_line(lines, list):
    if len(lines) <= 2:
        return

    ws = []
    for line in lines:
        ws.append(line.h)
    
    c_ws = [i for i in ws]
    c_ws.sort()
    min_w = c_ws[0];
    count = 0

    for w in ws:
        if min_w * 3 / 2 >= w :
            count += 1

    if count / len(ws) > 0.5:
        for idx in range(len(ws)):
            # 过宽的线段需要修正.
            if ws[idx] / min_w > 1.8:
                line = lines[idx]
                start = line.start
                some = list[start: start + line.h]
                total = 0
                for i in some:
                    total += i
                avg  = int(total / ws[idx])
                for i in range(len(some)):
                    some[i] = some[i] - avg
                print('some', some)
                c = round(ws[idx] / min_w) - 1
                i = 0
                r_idx = ws[idx] / (c + 1)

                while i < c:
                    low_lines = get_lower_zero_lines(some)
                    __idx__ = -1
                    for l_l in range(len(low_lines)):
                        index = low_lines[l_l][0]
                        print(low_lines[l_l][0], abs(index - r_idx), 1/2 * min_w)
                        if abs(index - r_idx * (i + 1)) <  1 / 2 * min_w:
                            __idx__ = l_l
                            break
                    
                    if __idx__ != -1:
                        split__idx = low_lines[l_l][0]
                        
                        lines[idx].h = split__idx
                        lines.insert(idx + 1, Line(lines[idx].start + split__idx + len(low_lines[l_l]) - 3, ws[idx] + 3 - split__idx -len(low_lines[l_l])))
                                        
                    i += 1





















def sort_value(list, sort_func):
    list_length = len(list)
    i = list_length - 1
    while i > 0:
        j = i - 1
        k = j
        while k >= 0:
            if sort_func(list[i], list[k]):
                tmp = list[i]
                list[i] = list[k]
                list[k] = tmp
            k -= 1

        i -= 1
    return list


def filter_zero(list):
    l = len(list) - 1
    ls = []
    while l:
        if list[l]:
            ls.append(list[l])
        l -= 1

    return ls


def get_site_value(list, max_gap):
    list.sort()
    idx = -1
    for i in range(len(list)):
        if i >= max_gap:
            idx = i
            break

    value = max_gap
    if idx > 0:
        idx -= 1
        value = list[idx] + 1

    return value


def get_index(list, value):
    idx = -1
    for i in range(len(list)):
        if list[i] == value:
            idx = i
            break
    return idx


def filter_list(list):
    values = []
    for i in list:
        idx = get_index(values, i)
        if idx == -1:
            values.append(i)
    return values


def get_max_list_item(list):
    idx = -1
    l = 0
    for i in range(len(list)):
        l_l = len(list[i])
        if l_l > l:
            idx = i
            l = l_l
    return idx, l


# 按最大值进行分割，
def split_list_to_group_idx(list):
    if len(list) <= 2:
        return [list]
    c_list = [i for i in list]
    list.sort()
    list_length = len(list)
    split_list = [c_list]
    # 分割的间隙值
    max_values = []
    count = 0
    max_loop = len(list)
    while True:
        if count > max_loop:
            break
        max_idx, l = get_max_list_item(split_list)
        values = split_list[max_idx]
        c_values = [i for i in values]
        max_value = get_split_max_value(c_values, max_values)

        if max_value <= 0:
            break
        max_values.append(max_value)
        idx = get_index(values, max_value)
        split_list[max_idx] = values[0: idx + 1]
        split_list.insert(max_idx + 1, values[idx + 1: len(values)])

        count += 1
    return split_list


def get_split_max_value(values, max_values):
    if len(values) <= 2:
        return 0

    c_values = [i for i in values]
    values.sort()
    min_value = values[0]
    max_value = values[len(values) - 1]
    max_idx = get_index(c_values, max_value)

    if max_idx >= len(values) - 2:
        max_value = values[len(values) - 2]
        max_idx = get_index(values, max_value)

    if len(max_values):
        max_values.sort()
        max_min_value = max_values[0]

        if max_value - min_value < max_min_value - max_value:
            return 0

    return max_value


def is_exist_min_value(values, min_value):
    is_exist = False

    for i in values:
        if i <= min_value:
            is_exist = True
            break

    return is_exist


def is_width_rate_of_change(values):
    values.sort()
    count = 0
    min_value = values[0]
    for value in values:
        if value > 2 * min_value:
            count += 1

    return count >= 2


def get_value_index(max_w, ws):
    i = -1
    for idx in range(len(ws)):
        if ws[idx] == max_w:
            i = idx
            break
    return i