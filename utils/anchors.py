from itertools import product as product
from math import ceil

import torch


class Anchors(object):
    def __init__(self, cfg, image_size=None):
        super(Anchors, self).__init__()
        self.min_sizes  = cfg['min_sizes']
        self.steps      = cfg['steps']
        self.clip       = cfg['clip']

        #   图片的尺寸
        self.image_size = image_size

        #   三个有效特征层高和宽
        self.feature_maps = [[ceil(self.image_size[0]/step), ceil(self.image_size[1]/step)] for step in self.steps]

    def get_anchors(self):
        anchors = []  # 创建一个空列表来存储锚框
        for k, f in enumerate(self.feature_maps):
            min_sizes = self.min_sizes[k]  # 获取当前特征层的min_sizes

            #   对特征层的高和宽进行循环迭代
            for i, j in product(range(f[0]), range(f[1])):
                for min_size in min_sizes:
                    s_kx = min_size / self.image_size[1]  # 计算当前锚框的宽度缩放比例
                    s_ky = min_size / self.image_size[0]  # 计算当前锚框的高度缩放比例
                    dense_cx = [x * self.steps[k] / self.image_size[1] for x in [j + 0.5]]  # 计算当前锚框的中心点的x坐标
                    dense_cy = [y * self.steps[k] / self.image_size[0] for y in [i + 0.5]]  # 计算当前锚框的中心点的y坐标
                    for cy, cx in product(dense_cy, dense_cx):  # 对中心点的y坐标和x坐标进行循环迭代
                        anchors += [cx, cy, s_kx, s_ky]  # 将生成的锚框添加到锚框列表中

        output = torch.Tensor(anchors).view(-1, 4)  # 将锚框列表转换为Tensor，并调整形状为(-1, 4)
        # -1表示自动计算该维度的大小，而4表示每个锚框具有4个元素
        if self.clip:  # 判断是否进行锚框的裁剪操作，目的是确保锚框的坐标值限制在图像范围内
            output.clamp_(max=1, min=0)   # 对锚框的坐标进行截断，限制在[0, 1]范围内
        return output  # 返回生成的锚框作为输出
