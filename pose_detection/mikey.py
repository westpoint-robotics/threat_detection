from ctypes import *
import math
import random
import cv2
import time


def sample(probs):
    s = sum(probs)
    probs = [a / s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs) - 1


def c_array(ctype, values):
    return (ctype * len(values))(*values)


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

# Loading libdarknet.so
# I've used absolute path with great success, didn't experiment with relative path
lib = CDLL("/home/benjamin/darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

make_boxes = lib.make_boxes
make_boxes.argtypes = [c_void_p]
make_boxes.restype = POINTER(BOX)

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

num_boxes = lib.num_boxes
num_boxes.argtypes = [c_void_p]
num_boxes.restype = c_int

make_probs = lib.make_probs
make_probs.argtypes = [c_void_p]
make_probs.restype = POINTER(POINTER(c_float))

detect = lib.network_predict
detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

ndarray_image = lib.ndarray_to_image
ndarray_image.argtypes = [POINTER(c_ubyte), POINTER(c_long), POINTER(c_long)]
ndarray_image.restype = IMAGE

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

network_detect = lib.network_detect
network_detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res


def detect_im(net, meta, im, thresh=.5, hier_thresh=.5, nms=.45):
    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res


def detect_np(net, meta, np_img, thresh=.5, hier_thresh=.5, nms=.45):
    im = nparray_to_image(np_img)
    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res


def nparray_to_image(img):

    data = img.ctypes.data_as(POINTER(c_ubyte))
    image = ndarray_image(data, img.ctypes.shape, img.ctypes.strides)

    return image


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


if __name__ == "__main__":
    with open("yolo_config.yml", 'r') as ymlfile:
        if sys.version_info[0] > 2:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        else:
            cfg = yaml.load(ymlfile)

    # Setup yolo config
    yolo_data = cfg['yolo_data'] 
    yolo_config = cfg['yolo_config'] 
    yolo_weights = cfg['yolo_weights'] 

    net = load_net(yolo_config,yolo_weights,0)
    meta = load_meta(yolo_data)

    img = cv2.imread(cfg['single_image'] ,cv2.IMREAD_COLOR) #load image in cv2
    objects = detect_np(net, meta, cfg['single_image'])

    for detection in objects:
        box_color = (0,255,0)
        center_x = detection[2][0]
        center_y = detection[2][2]
        width = detection[2][1]
        height = detection[2][3]
        UL_x = int(center_x - width/2) #Upper Left corner X coord
        UL_y = int(center_y + height/2) #Upper left Y
        LR_x = int(center_x + width/2)
        LR_y = int(center_y - height/2)
        #write bounding box to image
        cv2.rectangle(img,(UL_x,UL_y),(LR_x,LR_y),box_color,5)
        cv2.circle(img,(int(center_x),int(center_y)), 10, (0,0,255), 1)
        # cv2.resizeWindow("image", crop_img.shape[0]*1,crop_img.shape[1]*1)
        
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyWindow("image")

    # # load video here
    # cap = cv2.VideoCapture(0)
    # ret, img = cap.read()
    # # im=nparray_to_image(img)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    # net = load_net(b"cfg/tiny-yolo.cfg", b"tiny-yolo.weights", 0)
    # meta = load_meta(b"cfg/coco.data")
    # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    # while(1):
    #     ret, img = cap.read()
    #     r = detect_np(net, meta, img)
    #     # print(r)
    #     for i in r:
    #         x, y, w, h = i[2][0], i[2][1], i[2][2], i[2][3]
    #         xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))
    #         pt1 = (xmin, ymin)
    #         pt2 = (xmax, ymax)
    #         cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
    #         cv2.putText(img, i[0].decode() + " [" + str(round(i[1] * 100, 2)) + "]", (pt1[0], pt1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0], 4)
    #     cv2.imshow("img", img)
    #     k = cv2.waitKey(1)
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #         exit()
