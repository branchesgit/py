import cv2

class Template(object):
    def __init__(self, template_file, rect, setting):
        self.template_file = template_file
        self.rect = rect
        self.setting = setting

    def pre_template_match(self, mat):
        sx = self.rect.x
        sy = self.rect.y
        ex = sx + self.rect.w
        ey = sy + self.rect.h
        setting = self.setting
        ds = int(min(setting.paperWidth, setting.paperHeight) / 30)

        if ds < 50:
            ds = 50

        height, width = mat.shape
        sx -= ds
        sx = max(0, sx)
        sy -= ds
        sy = max(0, sy)
        ex += ds
        ex = min(ex, width - 1)
        ey = min(ey, height - 1)

        if ((setting.paperWidth * 1.0 / setting.paperHeight > 1 and width / height < 1) or
                (setting.paperWidth * 1.0 / setting.paperHeight < 1 and width / height > 1)):
            mat = cv2.flip(mat, 1)
            mat = cv2.transpose(mat)

        self.template_match([sx, sy, ex, ey], mat)

    # 处理模板.
    def template_match(self, search_rect, mat):
        search_img
        [sx, sy, ex, ey] = search_rect
        mat[sy:ey, sx: ex].copyTo(search_img)

        start_angle = -15
        end_angle = 15
        angle_step = 0.05
        start_scale = 0.8
        end_scale = 1.2

        py_count = 0

        template_mate = cv2.imread(self.template_file, 0)
        height, width = template_mate
        min_size = min(height, width)
        last_size = 14
        while True:
            py_count += 1
            last_size *= 2
            if last_size > min_size:
                break

        beset_x = -1
        best_y = -1
        beset_match_center_x = -1
        beset_match_center_y = -1
        beset_match_angle = 0
        beset_match_value = -1


    def handle_template_match(self,temp_img, search_img, match_thresh, start_angle, end_angle, angle_step,
		start_scale, end_scale, py_count, beset_match_center_x, beset_match_center_y,
		beset_match_angle, beset_match_value, beset_x, beset_y):
        py_temps = []
        py_temps.append(temp_img)
        py_searches = []
        py_searches.append(search_img)

        i = 1
        while i < py_count:
            height, width = py_temps[i-1].shape
            py_temps.append(cv2.resize(py_temps[i-1], (widht / 2, height / 2)))
            height, width = py_searches[i - 1].shape
            py_searches.append(cv2.resize(py_searches[i - 1], (widht / 2, height / 2)))
            i += 1
        py_angle_steps = []
        py_angle_steps.append(angle_step)

        i = 1
        while i < py_count:
            py_angle_steps.append(py_angle_steps[i-1] * 2)

        match_threshes = []
        match_threshes.append(match_thresh)
        match_step = match_thresh / (py_count -1)
        i = 1
        while i < py_count:
            match_threshes.append(match_threshes[i-1] - match_step)


        level = py_count -1
        while level >= 0:
            b_m_c_x = 0
            b_m_c_y = 0
            b_m_a = 0
            b_m_v = 0
            batch_x = 0
            batch_y = 0

            test_mat_gx = cv2.Sobel(py_searches[level], CV_32F, 1, 0, 3)
            test_mat_gy = cv2.Sobel(py_searches[level], CV_32F, 0, 1, 3)

            height, width = test_mat_gx
            i = 0
            pixels_count = height * width
            while i < pixels_count:
                dx = test_mat_gx[i]
                dy = test_mat_gy[i]
                mgv = sqrt(dx * dx + dy*dy)

                if mgv != 0:
                    test_mat_gx[i] /= mgv
                    test_mgt_gy[i] /= mgv

            s_angle = start_angle
            e_angle = end_angle
            if level != py_count - 1:
                s_angle = beset_match_angle - 4 * py_angle_steps[level + 1]
                e_angle = beset_match_angle + 4 * py_angle_steps[level + 1]

            a = s_angle
            while a <= e_angle:
                rot_temp
                rot_temp_mask

                if abs(a) > 0.001:
                    height, width = py_temps[level].shape
                    center(width / 2, height / 2)
                    rot_mat = cv2.getRotationMatrix2D(center, a, 1)
                    bound_box = RotatedRect(center, width, height, a).boundingRect()

                    rot_temp = cv2.warpAffine(py_temps[level], rot_mat, bound_box)

            level -= 1



