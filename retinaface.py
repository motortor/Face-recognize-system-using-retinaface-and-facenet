import cv2  # 导入cv2（OpenCV）模块
import numpy as np  # 导入numpy模块
import torch  # 导入PyTorch模块
import torch.nn as nn  # 导入PyTorch中的神经网络模块
from PIL import Image, ImageDraw, ImageFont  # 导入PIL模块中的Image、ImageDraw、ImageFont类
from tqdm import tqdm  # 展示进度条的模块

from nets.facenet import Facenet  # 导入nets/facenet.py中的Facenet类
from nets_retinaface.retinaface import RetinaFace  # 导入nets_retinaface/retinaface.py中的RetinaFace类
from utils.anchors import Anchors  # 导入utils/anchors.py中的Anchors类
from utils.config import cfg_mnet, cfg_re50  # 导入utils/config.py中的cfg_mnet和cfg_re50配置信息
from utils.utils import (Alignment_1, compare_faces, letterbox_image, preprocess_input)  # 导入utils/utils.py中的函数
from utils.utils_bbox import (decode, decode_landm, non_max_suppression, retinaface_correct_boxes)  # 导入utils/utils_bbox.py中的函数

def cv2ImgAddText(img, label, left, top, textColor=(255, 255, 255)):
# img: 一个numpy数组表示的图像
# label: 需要添加到图像上的标签或文本
# left: 文本的左边距离
# top: 文本的上边距离
# textColor: 可选参数，指定文本颜色，默认为白色
    img = Image.fromarray(np.uint8(img))  # 通过将numpy数组转换为PIL图像来准备图像处理
    font = ImageFont.truetype(font='model_data/fangzhengxiangsu12.ttf', size=20)
    # 设置（名字）字体：方正像素12，字体大小20
    draw = ImageDraw.Draw(img)  # 创建一个可绘制的图像对象
    label = label.encode('utf-8')   # 将标签编码为 utf-8 格式的字符串
    draw.text((left, top), str(label, 'UTF-8'), fill=textColor, font=font)   # 在图像上绘制文本，包括文本的位置、内容、颜色和字体
    return np.asarray(img)  # 将绘制好的图像转化为 numpy 数组并返回

class Retinaface(object):
    _defaults = {
        "retinaface_model_path": 'model_data/Retinaface_mobilenet0.25.pth',  # retinaface训练完的权值路径
        "retinaface_backbone": "mobilenet",  # retinaface所使用的主干网络，有mobilenet和resnet50
        "confidence": 0.75,  # retinaface中只有得分>0.75置信度的预测框会被保留下来
        "nms_iou": 0.3,  # 非极大值抑制（NMS）的 IOU 阈值，用于去除重叠的人脸框
        "retinaface_input_shape": [640, 640, 3],  # RetinaFace 的输入图像大小为 640x640 像素，且每个像素包含 3 个通道（即 RGB 颜色空间）
        # RetinaFace 是一个基于 Anchor 的人脸检测器，其输入图像大小必须是32的倍数
        # 这是因为在Anchor - based的检测器中，检测框的大小和位置是通过一系列预定义的Anchor和相应的偏移量来确定的
        # 如果输入图像的尺寸不是32的倍数，则在Anchor的计算过程中会出现小数，从而导致Anchor无法匹配到与之相对应的特征图上的位置，进而影响检测结果的准确性
        "letterbox_image": True,    # 是否将输入图像调整为 RetinaFace 的输入图像大小

        "facenet_model_path": 'model_data/facenet_mobilenet.pth',  # facenet训练完的权值路径
        "facenet_backbone": "mobilenet",  # facenet所使用的主干网络， mobilenet和inception_resnetv1
        "facenet_input_shape": [160, 160, 3],  # 人脸识别模型的输入图像大小
        "facenet_threhold": 0.9,  # 人脸识别模型的阈值，用于判断两张人脸是否为同一个人
        "cuda": False,  # 是否使用 GPU 进行计算
    }

    @classmethod  # 类方法
    def get_defaults(cls, n):  # cls 表示类自身
        if n in cls._defaults:
            return cls._defaults[n]    # 返回默认值
        else:
            return "参数名无法识别"

    # 初始化Retinaface
    def __init__(self, encoding=0, **kwargs):  # encoding为是否对已有人脸进行编码的标志位
        self.__dict__.update(self._defaults)   # 更新默认参数
        for name, value in kwargs.items():  # 遍历kwargs字典中的参数并设置
            setattr(self, name, value)

        # 不同主干网络的config信息
        if self.retinaface_backbone =="mobilenet":  # 判断使用哪种RetinaFace模型
            self.cfg = cfg_mnet  # mobilenet
        else:
            self.cfg = cfg_re50  # resnet50

        # 先验框的生成
        self.anchors = Anchors(self.cfg, image_size=(self.retinaface_input_shape[0], self.retinaface_input_shape[1])).get_anchors()
        self.generate()  # 生成RetinaFace网络

        try:  # 尝试加载已经存储的人脸特征和姓名
            self.known_face_encodings = np.load("model_data/{backbone}_face_encoding.npy".format(backbone=self.facenet_backbone))
            self.known_face_names = np.load("model_data/{backbone}_names.npy".format(backbone=self.facenet_backbone))
        except:  # 如果加载失败
            if not encoding:  # 如果encoding为False，说明不允许重新编码，则提示人脸特征载入失败
                print("载入已有人脸特征失败，请检查model_data下面是否生成了相关的人脸特征文件。")
            pass  # 继续执行

    # 获得所有的分类
    def generate(self):
        # 载入模型与权值
        self.net = RetinaFace(cfg=self.cfg, phase='eval', pre_train=False).eval()  # 创建一个 RetinaFace 的模型实例，并设置为评估模式，即不进行梯度更新
        # cfg:模型的配置参数  phase:模型的阶段=评估模式  pre_train:是否进行预训练=否
        self.facenet = Facenet(backbone=self.facenet_backbone, mode="predict").eval()  #创建一个 Facenet 的模型实例
        # backbone：模型的主干网络  mode:模型的模式=预测模式

        print('加载中...')  # 加载 RetinaFace 模型的权重，并将其加载到模型实例中
        state_dict = torch.load(self.retinaface_model_path,map_location=torch.device('cpu'))
        self.net.load_state_dict(state_dict)

        state_dict = torch.load(self.facenet_model_path,map_location=torch.device('cpu'))  # 加载 Facenet 模型的权重，并将其加载到模型实例中
        self.facenet.load_state_dict(state_dict, strict=False)

        if self.cuda:  # 如果设置了使用 CUDA 加速，则将模型移动到 GPU 上
            self.net = nn.DataParallel(self.net)  # 使用 nn.DataParallel 将模型并行化
            self.net = self.net.cuda()

            self.facenet = nn.DataParallel(self.facenet)
            self.facenet = self.facenet.cuda()
        print('Finished!')

    def encode_face_dataset(self, image_paths, names):  # 将人脸图像编码为特征向量
        face_encodings = []  # 定义一个空列表用于存储人脸图像的特征向量
        for index, path in enumerate(tqdm(image_paths)):  # 遍历 image_paths 列表中的每个元素，并给每个元素赋予一个索引 index 和一个路径 path
            # tqdm()函数可以展示出一个进度条，方便观察整个遍历的进度
            image = np.array(Image.open(path), np.float32)   # 读取人脸图像，将其转换为 numpy 数组，并将其数据类型转换为 np.float32
            old_image =image.copy()  # 对输入图像进行一个备份，避免修改原始图像数据
            im_height, im_width, _ = np.shape(image)   # 获取人脸图像的高度、宽度和通道数，即获取人脸图像的形状信息

            # 定义一个列表 scale，用于存储当前遍历到的人脸图像的缩放比例信息
            # 列表中的四个元素分别代表原始图像的宽度、高度、宽度和高度
            scale = [np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0]]
            # 该列表中的元素数量比 scale 列表中多了6个，是因为还需要用到人脸的关键点信息
            scale_for_landmarks = [
                np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
                np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
                np.shape(image)[1], np.shape(image)[0]
            ]
            if self.letterbox_image:  # 如果需要进行 letterbox 缩放操作，则调用 letterbox_image 函数对当前遍历到的人脸图像进行缩放
                image = letterbox_image(image, [self.retinaface_input_shape[1], self.retinaface_input_shape[0]])  # 将返回值赋值给 image 变量
                anchors = self.anchors
            # 如果不需要进行 letterbox 缩放操作，则调用 Anchors 类的 get_anchors 方法获取当前遍历到的人脸图像的 anchor boxes
            else:
                anchors = Anchors(self.cfg, image_size=(im_height, im_width)).get_anchors()  # 将返回值赋值给 anchors 变量
            # 在RetinaFace中，anchor boxes是指一组按照预定义大小和宽高比分布在输入图像上的矩形框，用于检测人脸的位置和大小

            # 将处理完的图片传入Retinaface网络当中进行预测
            with torch.no_grad():  # 关闭梯度计算，加速模型推理
                # 将图像转化为张量，并进行预处理和转置，最后在第0维添加一个维度，变为[1,C,H,W]的张量
                image = torch.from_numpy(preprocess_input(image).transpose(2, 0, 1)).unsqueeze(0).type(torch.FloatTensor)
                # preprocess_input(image) 对图像进行预处理，可能包括像素值归一化、减去均值等操作，以适应模型的输入要求
                # transpose(2, 0, 1) 对图像的维度进行调整，即将原始的H*W*C的图像变成C*H*W的形状
                # unsqueeze(0) 在第0维（即第一个维度）上添加一个维度，将单张图像的Tensor包装成一个mini-batch的Tensor，以便进行批量处理
                # type(torch.FloatTensor) 将Tensor的数据类型转换为浮点型。

                if self.cuda:  # 如果开启了CUDA加速，则将张量和anchors放入GPU中进行计算
                    image = image.cuda()
                    anchors = anchors.cuda()

                loc, conf, landms = self.net(image)   # 输入到RetinaFace网络中进行前向传播
                # 将网络输出的loc、conf和landms解码得到预测的边框框、置信度和关键点位置等信息
                boxes = decode(loc.data.squeeze(0), anchors, self.cfg['variance'])  # 对预测框进行解码
                conf = conf.data.squeeze(0)[:, 1:2]   # 取置信度中的第二个值，即正样本的概率
                landms = decode_landm(landms.data.squeeze(0), anchors, self.cfg['variance'])  # 对人脸关键点进行解码

                # 将解码得到的边框、置信度和关键点位置等信息进行拼接
                boxes_conf_landms = torch.cat([boxes, conf, landms], -1)
                # 对拼接后的信息进行非极大值抑制，筛选出置信度较高的bounding boxes
                boxes_conf_landms = non_max_suppression(boxes_conf_landms, self.confidence)

                # 如果未检测到人脸，跳过当前图像
                if len(boxes_conf_landms) <= 0:
                    print(names[index], ": 未检测到人脸")
                    continue

                # 如果使用了letterbox_image的话，需要将输入的图片缩放到指定大小，去掉灰条
                if self.letterbox_image:
                    boxes_conf_landms = retinaface_correct_boxes(boxes_conf_landms,  # 预测出的人脸框
                        np.array([self.retinaface_input_shape[0], self.retinaface_input_shape[1]]),  # 缩放后的图像大小
                        np.array([im_height, im_width]))  # 原图像大小
                # 该函数的作用是对预测出的人脸框进行缩放和平移，以适应原图像上的位置
                # 如果 self.letterbox_image 为 True，那么 image 会被使用 letterbox_image 函数增加灰条，以便进行不失真的resize
                # 在这种情况下，使用 retinaface_correct_boxes 函数将 boxes_conf_landms 中的坐标从填充的图像大小转换回原始图像大小
                # 这就相当于将灰条去掉，还原原始图像

            boxes_conf_landms[:, :4] = boxes_conf_landms[:, :4] * scale  # 将检测到的人脸框的坐标按照之前的缩放比例进行还原
            boxes_conf_landms[:, 5:] = boxes_conf_landms[:, 5:] * scale_for_landmarks  # 将检测到的人脸关键点的坐标按照之前的缩放比例进行还原

            # 选取最大的人脸框
            best_face_location = None  # 初始化最佳人脸位置为 None
            biggest_area = 0  # 初始化最大面积为 0
            for result in boxes_conf_landms:  # 对每个检测到的人脸框进行循环遍历
                left, top, right, bottom = result[0:4]  # 获取当前人脸框的左上角和右下角坐标
                # 计算人脸框的宽和高
                w = right - left
                h = bottom - top
                if w * h > biggest_area:  # 如果当前人脸框的面积大于之前最大的面积
                    biggest_area = w * h  # 更新最大面积值
                    best_face_location = result  # 更新最佳人脸位置
            # 最终 best_face_location 将保存最大面积的人脸框

            # 截取图像
            crop_img = old_image[int(best_face_location[1]):int(best_face_location[3]),  # 从左上角的横坐标开始，裁剪到右下角的横坐标
                       int(best_face_location[0]):int(best_face_location[2])]  # 从左上角的纵坐标开始，裁剪到右下角的纵坐标
            # 从原始图像中裁剪出的包含人脸的图像
            # best_face_location：具有最高置信度的人脸框（左上角和右下角的坐标以及人脸关键点的位置）
            landmark = np.reshape(best_face_location[5:], (5, 2)) - np.array([int(best_face_location[0]), int(best_face_location[1])])
            # 将最佳人脸位置中的5个关键点的坐标提取出来，并进行归一化
            # best_face_location[5:]表示从位置信息中取出后面的10个元素，即5个关键点的坐标
            # (5,2)表示将这10个坐标重新组织成一个5*2的矩阵，即每行两个元素，共5行
            # np.array(~) 表示将人脸左上角的坐标作为偏移量，将关键点的坐标进行平移，以便与crop_img对齐
            crop_img, _ = Alignment_1(crop_img, landmark)  # 进行人脸对齐

            crop_img = np.array(letterbox_image(np.uint8(crop_img), (self.facenet_input_shape[1], self.facenet_input_shape[0]))) / 255
            # 将对齐后的人脸图像缩放为 facenet_input_shape 指定的大小，并将像素值标准化为0到1之间的浮点数
            crop_img = crop_img.transpose(2, 0, 1)
            crop_img = np.expand_dims(crop_img, 0)  # 在第0个位置增加一个新的维度

            # 利用图像算取长度为128的特征向量
            with torch.no_grad():  # 关闭梯度计算，加速模型推理
                crop_img = torch.from_numpy(crop_img).type(torch.FloatTensor)  # 将crop_img转换为FloatTensor类型的张量
                if self.cuda:  # 如果GPU可用，将张量移至GPU上进行计算
                    crop_img = crop_img.cuda()
                face_encoding = self.facenet(crop_img)[0].cpu().numpy()  # 将张量输入facenet模型得到特征向量，并将结果转换为numpy数组
                face_encodings.append(face_encoding)  # 将特征向量添加到列表中
            # 该代码利用输入的人脸图像（crop_img），通过深度学习模型（self.facenet）计算得到该人脸的128维特征向量（face_encodings）
            # 其中，首先将crop_img转换为张量类型，然后将张量输入到模型中得到输出，最后将输出转换为numpy数组类型的特征向量，并将该特征向量添加到列表中
            # 该代码使用了PyTorch框架，并使用了GPU进行计算

        np.save("model_data/{backbone}_face_encoding.npy".format(backbone=self.facenet_backbone), face_encodings)  # 保存人脸特征向量
        np.save("model_data/{backbone}_names.npy".format(backbone=self.facenet_backbone), names)  # 保存人名

    # 检测图片
    def detect_image(self, image):
        old_image = image.copy()  # 对输入图像进行一个备份，后面用于绘图
        image = np.array(image, np.float32)  # 把图像转换成numpy的形式

        # Retinaface检测部分
        im_height, im_width, _ = np.shape(image)
        # 计算scale，用于将获得的预测框转换成原图的高宽
        scale = [np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0]]
        scale_for_landmarks = [
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0]
        ]
        # letterbox_image可以给图像增加灰条，实现不失真的resize
        if self.letterbox_image:
            image = letterbox_image(image, [self.retinaface_input_shape[1], self.retinaface_input_shape[0]])
            anchors = self.anchors
        else:
            anchors = Anchors(self.cfg, image_size=(im_height, im_width)).get_anchors()
        #  将处理完的图片传入Retinaface网络当中进行预测
        with torch.no_grad():  # 关闭梯度计算,加速模型推理
            image = torch.from_numpy(preprocess_input(image).transpose(2, 0, 1)).unsqueeze(0).type(torch.FloatTensor)

            if self.cuda:  # 如果开启了CUDA加速，则将张量和anchors放入GPU中进行计算
                image = image.cuda()
                anchors = anchors.cuda()
            # 传入网络进行预测
            loc, conf, landms = self.net(image)
            boxes = decode(loc.data.squeeze(0), anchors, self.cfg['variance'])
            conf = conf.data.squeeze(0)[:, 1:2]
            landms = decode_landm(landms.data.squeeze(0), anchors, self.cfg['variance'])
            # 对人脸检测结果进行堆叠
            boxes_conf_landms = torch.cat([boxes, conf, landms], -1)
            boxes_conf_landms = non_max_suppression(boxes_conf_landms, self.confidence)
            # 如果没有预测框则返回原图
            if len(boxes_conf_landms) <= 0:
                return old_image, []
            # 如果使用了letterbox_image的话，要把灰条的部分去除掉
            if self.letterbox_image:
                boxes_conf_landms = retinaface_correct_boxes(boxes_conf_landms, \
                    np.array([self.retinaface_input_shape[0], self.retinaface_input_shape[1]]), np.array([im_height, im_width]))
            boxes_conf_landms[:, :4] = boxes_conf_landms[:, :4] * scale
            boxes_conf_landms[:, 5:] = boxes_conf_landms[:, 5:] * scale_for_landmarks

        # Facenet编码部分
        face_encodings = []
        for boxes_conf_landm in boxes_conf_landms:
            # 图像截取，人脸矫正
            boxes_conf_landm = np.maximum(boxes_conf_landm, 0)  # 将坐标值小于0的部分设为0
            crop_img = np.array(old_image)[int(boxes_conf_landm[1]):int(boxes_conf_landm[3]),
                       int(boxes_conf_landm[0]):int(boxes_conf_landm[2])]  # 截取原图像中的人脸部分
            landmark = np.reshape(boxes_conf_landm[5:],(5,2)) - \
                       np.array([int(boxes_conf_landm[0]),int(boxes_conf_landm[1])])  # 根据人脸检测的关键点对人脸进行校正
            crop_img, _ = Alignment_1(crop_img, landmark)
            # 人脸编码
            crop_img = np.array(letterbox_image(np.uint8(crop_img), (self.facenet_input_shape[1],self.facenet_input_shape[0])))/255
            crop_img = np.expand_dims(crop_img.transpose(2, 0, 1),0)   # 调整图像维度
            with torch.no_grad():
                crop_img = torch.from_numpy(crop_img).type(torch.FloatTensor)
                if self.cuda:
                    crop_img = crop_img.cuda()
                #   利用facenet_model计算长度为128特征向量
                face_encoding = self.facenet(crop_img)[0].cpu().numpy()  # 计算人脸图像的特征向量
                face_encodings.append(face_encoding)  # 将特征向量添加到列表中

        # 人脸特征比对
        face_names = []  # 创建一个空的人脸名称列表
        for face_encoding in face_encodings:  # 循环遍历已知人脸编码列表中的每个编码
            # 与已知人脸编码列表中的每个编码进行比较，返回匹配结果和欧几里得距离
            matches, face_distances = compare_faces(self.known_face_encodings, face_encoding, tolerance = self.facenet_threhold)
            name = 'Unknown'  # 将名称设置为“Unknown”
            best_match_index = np.argmin(face_distances)  # 找到最佳匹配编码的索引
            if matches[best_match_index]:   # 如果最佳匹配编码的匹配结果为True，则将名称设置为对应的人名
                name = self.known_face_names[best_match_index]
            face_names.append(name)  # 将名称添加到人脸名称列表中

        for i, b in enumerate(boxes_conf_landms):  # 循环迭代每一个人脸框（包含位置、置信度和面部特征点）
            text = "conf:{:.4f}".format(b[4])  # 获取人脸框的置信度并格式化为小数点后四位的字符串
            b = list(map(int, b))  # 将人脸框的位置和置信度从浮点数转换为整数
            # b[0]-b[3]为人脸框的坐标，b[4]为置信度（该人脸框中是否存在人脸的可信度）
            cv2.rectangle(old_image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)  # 给原始图像中的人脸框添加蓝色矩形边框
            # 左上角置信度的文本框
            cx = b[0]  # 文本框左上角的x坐标
            cy = b[1] + 12  # 文本框左上角的y坐标再向下移动12个像素
            cv2.putText(old_image, text, (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

            # b[5]-b[14]为人脸关键点的坐标
            cv2.circle(old_image, (b[5], b[6]), 1, (0, 0, 255), 4)  # 蓝色  左眼坐标（观察者视角）
            cv2.circle(old_image, (b[7], b[8]), 1, (0, 255, 255), 4)  # 青色  右眼坐标
            cv2.circle(old_image, (b[9], b[10]), 1, (255, 0, 255), 4)  # 品红色  鼻子坐标
            cv2.circle(old_image, (b[11], b[12]), 1, (0, 255, 0), 4)  # 绿色  嘴角左边
            cv2.circle(old_image, (b[13], b[14]), 1, (255, 0, 0), 4)  # 红色  嘴角右边
            name = face_names[i]  # 获取人脸的名称
            old_image = cv2ImgAddText(old_image, name, b[0] + 5, b[3] - 25)  # 在原始图像上添加人脸名称的文本
        return old_image, face_names
