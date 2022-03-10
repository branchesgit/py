from rect import Line

def get_middle_value(list):
    list_length = len(list)
    if list_length > 0:
        l = [i for i in list]
        l = sort_value(l, comp_value)
        idx = int(len(list) / 2)
        return l[idx]
    else:
        return 0

def comp_value(a, b):
    if a > b:
        return False
    else: 
        return True

def get_max_value(list):
    list_length = len(list)
    if list_length > 0:
        l = [i for i in list]
        l = sort_value(l, comp_value)
        return l[list_length -1]
    else:
        return 0

def get_lines(list, w_min, w_max, w_h):
    lines = []
    start = -1
    h = 0
    total = 0
    for i in range(len(list)):
        value =  list[i]
        if value >= w_min and value <= w_max :
            if start == -1:
                start = i
                h = 1
                total = value 
            else: 
                h += 1
                total += value
        else:
            if start == -1:
               continue
            else:
                line = Line(start, h)
                line.areaRate = total / (h * w_h)
                if (line.areaRate >= 0.06):
                    lines.append(line)
                start = -1
    
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
            k -=1

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
        value = list[idx]

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


def split_list_to_group_idx(list):
    c_list = [i for i in list]
    list.sort()
    min_value = list[0]
    idx = get_index(c_list, min_value)
    # 最小值附近变动应该是最明显的
    rates = []
    idx = 0
    while idx < len(list):
        value = c_list[idx]
        rates.append(value / min_value)
        idx += 1
    rates.sort()
    
    mid_rate = (rates[0] + rates[len(rates) - 1]) / 2
    idx = -1
    for i in range(len(rates)):
        if i:
            if rates[i] > mid_rate:
                idx = i
                break
    return idx

    
