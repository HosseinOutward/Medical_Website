import numpy as np
import cv2


def edit_database(image_pk):
    import django, os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    from patient.models import ImagePatient

    img = ImagePatient.objects.filter(pk=image_pk).get()
    if len(img.shape)==3: img=img[:, :, 0]
    img.machine_label_data_imag = points_to_label(masks_to_points(get_masks(img), lim=0.115, many=True))
    img.save()

    return


def get_masks(image):
    img_x = image.shape[0]
    img_y = image.shape[1]
    resize=lambda x: cv2.resize(x, (img_y, img_x), interpolation=cv2.INTER_AREA)
    return [
        resize(cv2.imread(r"D:\Ext. App Files\Code\Py\Test\test_script\results\1- results.jpg", 0)),
        resize(cv2.imread(r"D:\Ext. App Files\Code\Py\Test\test_script\results\2- results.jpg", 0)),
        resize(cv2.imread(r"D:\Ext. App Files\Code\Py\Test\test_script\results\3- results.jpg", 0)),
    ]
    # prediction.cpu().numpy()


def masks_to_points(mask_image, lim=0.16, many=False):
    if many:
        out_ps = []; out_cs = []
        for mask in mask_image:
            p, c = masks_to_points(mask, lim)
            out_ps.append(p)
            out_cs.append(c)
        return out_ps, out_cs

    from math import ceil, sqrt, atan

    def get_slope(p1, p2):
        m = (p2[0] - p1[0])
        m = 1 / m if m != 0 else 1e-8
        return m * (p2[1] - p1[1])

    def line_split(beg_idx, end_idx, cont, steps=200):
        m = get_slope(cont[beg_idx], cont[end_idx])
        c = cont[beg_idx]
        c = -m * c[0] + c[1]
        get_dis = lambda p: abs((m * p[0] + c - p[1])) / sqrt(m ** 2 + 1)

        new_p = []
        steps = ceil((end_idx - beg_idx) / steps)
        for r in range(beg_idx, end_idx, steps):
            new_p.append((get_dis(cont[r]), r))

        # print(max(new_p, key=lambda x: x[0]), cont[beg_idx], cont[end_idx], get_dis(cont[end_idx]))
        return max(new_p, key=lambda x: x[0])

    def add_lines(poly_points, poly_rs, ratio):
        i = 1
        while i != len(poly_points):
            if i == len(poly_points): break
            dis, r = line_split(poly_rs[i - 1], poly_rs[i], contours)
            if dis < pix_lim * ratio: i += 1; continue
            poly_rs = np.insert(poly_rs, i, r)
            poly_points = np.insert(poly_points, i, contours[r], axis=0)
        return poly_points, poly_rs

    def clean_straight_lines(poly_points, poly_rs, ratio):
        i = 1
        while i != len(poly_points) - 1:
            angle1 = atan(get_slope(poly_points[i - 1], poly_points[i]))
            angle2 = atan(get_slope(poly_points[i], poly_points[i + 1]))
            delta_angle = abs(angle1 - angle2)
            if delta_angle > lim * 1.571 * ratio: i += 1; continue
            # print(delta_angle, lim*1.571)
            poly_rs = np.delete(poly_rs, i)
            poly_points = np.delete(poly_points, i, axis=0)
        return poly_points, poly_rs

    def clean_short_lines(poly_points, poly_rs, ratio):
        i = 1
        dis = lambda p1, p2: sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        while i != len(poly_points):
            if dis(poly_points[i - 1], poly_points[i]) > pix_lim * ratio: i += 1; continue
            _, r = line_split(poly_rs[i - 1], poly_rs[i], contours)

            poly_rs = np.delete(np.insert(poly_rs, i, r), [i - 1, i + 1])
            poly_points = np.delete(np.insert(poly_points, i, contours[r], axis=0), [i - 1, i + 1], axis=0)
        return poly_points, poly_rs

    contours, _ = cv2.findContours(mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours)<3: return [], []

    j=r=0
    for i, c in enumerate(contours):
        if c.size>r: j=i;r=c.size
    contours = contours[j][:, 0]

    poly_rs = np.array([r for r in range(0, len(contours) // 3 * 3, max((len(contours) - 1) // 3,1))] + [len(contours) - 1])
    poly_points = np.array([contours[r] for r in poly_rs])

    pix_lim = lim * \
              sqrt((max(contours, key=lambda x: x[0])[0] - min(contours, key=lambda x: x[0])[0])**2 + \
               (max(contours, key=lambda x: x[1])[1] - min(contours, key=lambda x: x[1])[1])**2)

    poly_points, poly_rs = add_lines(poly_points, poly_rs, 0.6)
    poly_points, poly_rs = clean_straight_lines(poly_points, poly_rs, 1.0)
    poly_points, poly_rs = clean_short_lines(poly_points, poly_rs, 1.1)
    # poly_points, poly_rs = add_lines(poly_points, poly_rs, 1.1)
    # poly_points, poly_rs = clean_short_lines(poly_points, poly_rs, 0.6)

    poly_points = poly_points[:-1]
    print("number of points:", len(poly_points) - 1)
    return poly_points, contours


def points_to_label(points):
    label = [
        {
            "value": {
                "points": [],
                "polygonlabels": ["CVC"]
            },
            "original_width": 3020,
            "original_height": 2400,
            "image_rotation": 0,
            "id": "j-hZ4vZ1QE",
            "from_name": "polygons",
            "to_name": "img",
            "type": "polygonlabels"
        },
        {
            "value": {
                "points": [],
                "polygonlabels": ["Heart"]
            },
            "original_width": 3020,
            "original_height": 2400,
            "image_rotation": 0,
            "id": "9BtXVdVBBm",
            "from_name": "polygons",
            "to_name": "img",
            "type": "polygonlabels"
        },
        {
            "value": {
                "points": [],
                "polygonlabels": ["Aorta"]
            },
            "original_width": 3020,
            "original_height": 2400,
            "image_rotation": 0,
            "id": "AFYF-6kcsm",
            "from_name": "polygons",
            "to_name": "img",
            "type": "polygonlabels"
        }
    ]
    for i, obj_points in enumerate(points):
        polygonlabels = {0:'CVC', 1:'Heart', 2:'Aorta'}[i]
        label[i]["value"]["polygonlabels"][0]=polygonlabels
        label[i]["value"]["points"]=obj_points

    return str(label)


def debug_points(points, input_img):
    img_x = input_img.shape[0]
    img_y = input_img.shape[1]
    image=[]
    for p in points:
        if p!=[]: image.append(cv2.polylines(np.zeros([img_x, img_y], dtype=np.uint8), [p], True, (255, 255, 255), 2))
        else: image.append(np.zeros([img_x, img_y], dtype=np.uint8))
        # cv2.imshow("i", image[-1]);cv2.waitKey(0)
    image = np.argmax(image, 0)
    label_colors = np.array([(128, 0, 0), (0, 128, 0), (0, 0, 128)])
    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    for l in range(0, 3):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]
    rgb = np.stack([r, g, b], axis=2)

    result = cv2.addWeighted(input_img,1, rgb, 0.35, 0)

    return result


if __name__ == "__main__":
    input_img = cv2.imread(r"D:\Ext. App Files\Code\Py\Test\test_script\4002362_Rashidi_luna_1.png")
    out_ps, _ = masks_to_points(get_masks(input_img[:, :, 0]), lim=0.115, many=True)
    cv2.imshow("i", debug_points(out_ps, input_img))
    cv2.waitKey(0)
    print(points_to_label(out_ps))