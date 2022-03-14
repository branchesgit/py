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
                        rates.append(line.areaRate)
                        if (line.areaRate >= 0.06):
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
                    rates.append(line.areaRate)
                    if (line.areaRate >= 0.06):
                        lines.append(line)
                else:
                    lines.append(line)
            start = -1
            h = 0

    return lines


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
    while True:
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
