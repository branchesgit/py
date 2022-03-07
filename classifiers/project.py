import cv2
import numpy as np

# 水平方向投影
def hProject(binary):
    cv2.imwrite("./imgs/part.png", binary)
    h, w = binary.shape

    # 水平投影
    hprojection = np.zeros(binary.shape, dtype=np.uint8)

    # 创建h长度都为0的数组
    h_h = [0]*h
    for j in range(h):
        for i in range(w):
            if binary[j,i] == 0:
                h_h[j] += 1
    # 画出投影图
    for j in range(h):
        for i in range(h_h[j]):
            hprojection[j,i] = 255

    cv2.imwrite("./imgs/hpro.png", hprojection)
    return h_h

    
# 垂直反向投影
def vProject(binary):
    h, w = binary.shape
    # 垂直投影
    vprojection = np.zeros(binary.shape, dtype=np.uint8)

    # 创建 w 长度都为0的数组
    w_w = [0]*w
    for i in range(w):
        for j in range(h):
            if binary[j, i ] == 0:
                w_w[i] += 1

    for i in range(w):
        for j in range(w_w[i]):
            vprojection[j,i] = 255

    cv2.imwrite("./imgs/vpro.png", vprojection)
    return w_w

# 集中分布 集中分布在哪几段. 可偏差范围
def concentrated(list, num):
    list.sort()
    centers = []
    size = int(len(list) / num)
    i = 0
    loop = 0
    while(loop < num):
        if i != num -1:
            value, dis = get_concentrated(list[i: i + size])
            centers.append(value)
            centers.append(dis)
            i = i + size
        else: 
            value, dis = get_concentrated(list[i: len(list)])
            centers.append(value)
            centers.append(dis)
        loop = loop + 1
    
    return centers

def get_concentrated(list):
    middle = list[int(len(list) / 2)]
    ps = [0.5, 0.6, 0.7, 0.8, 0.9]
    ranges = []
    for k in range(len(ps)):
        loop = 0
        p = 0
        size = 0
        while(p < ps[k]):
            size = 0
            loop = loop + 1
            n = middle - loop
            m = middle + loop
           
            for i in range(len(list)):
                if list[i] >= n and list[i] <= m:
                    size = size + 1
            p = size / len(list)
        ranges.append(loop)
    dis = []
    
    for i in range(len(ranges)):
        if i >= 1:
            loop = ranges[i] - ranges[i - 1]
            dis.append(loop)

    idx = -1
    for i in range(len(dis)):
        if dis[i] > 30:
            idx = i - 1
            break
        else:
            idx = i

    loop = ranges[idx + 1]
    
    return middle, ranges[idx + 1]














