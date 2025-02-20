import numpy as np
import torch
from torchvision.ops import nms


#   将输出调整为相对于原图的大小
def retinaface_correct_boxes(result, input_shape, image_shape):
    new_shape   = image_shape*np.min(input_shape/image_shape)  # 计算新的形状，使得图像按比例缩放到输入形状的最小尺寸

    offset      = (input_shape - new_shape) / 2. / input_shape  # 计算偏移量，将新形状放置在输入形状中心位置
    scale       = input_shape / new_shape  # 计算比例尺，用于将坐标值缩放到新形状
    
    scale_for_boxs      = [scale[1], scale[0], scale[1], scale[0]]  # 为边界框计算的比例尺
    # 为人脸关键点计算的比例尺
    scale_for_landmarks = [scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0]]

    offset_for_boxs         = [offset[1], offset[0], offset[1],offset[0]]   # 为边界框计算的偏移量
    # 为人脸关键点计算的偏移量
    offset_for_landmarks    = [offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0]]

    result[:, :4] = (result[:, :4] - np.array(offset_for_boxs)) * np.array(scale_for_boxs)  # 根据比例尺和偏移量，对结果中的边界框进行修正
    # 根据比例尺和偏移量，对结果中的人脸关键点进行修正
    result[:, 5:] = (result[:, 5:] - np.array(offset_for_landmarks)) * np.array(scale_for_landmarks)

    return result

#   中心解码，宽高解码
def decode(loc, priors, variances):
    # 根据定位偏移量、先验框和方差解码生成预测的边界框
    boxes = torch.cat((priors[:, :2] + loc[:, :2] * variances[0] * priors[:, 2:],  # 计算边界框的中心点坐标
                    priors[:, 2:] * torch.exp(loc[:, 2:] * variances[1])), 1)  # 计算边界框的宽度和高度
    # 根据预测的边界框坐标进行调整
    boxes[:, :2] -= boxes[:, 2:] / 2
    boxes[:, 2:] += boxes[:, :2]
    return boxes

#   关键点解码
def decode_landm(pre, priors, variances):
    landms = torch.cat((priors[:, :2] + pre[:, :2] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 2:4] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 4:6] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 6:8] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 8:10] * variances[0] * priors[:, 2:],
                        ), dim=1)
    return landms


def non_max_suppression(detection, conf_thres=0.5, nms_thres=0.3):
    # 找出该图片中得分大于门限函数的框。在进行重合框筛选前就进行得分的筛选可以大幅度减少框的数量
    mask        = detection[:, 4] >= conf_thres  # 标记得分大于等于门限值的框
    detection   = detection[mask]  # 筛选出得分大于等于门限值的框

    if len(detection) <= 0:  # 如果筛选后的框数量为空，则返回空列表
        return []

    keep = nms(
        detection[:, :4],  # 提取框的坐标信息（x, y, width, height）
        detection[:, 4],  # 提取框的得分
        nms_thres  # NMS的阈值，表示当两个边界框之间的重叠程度超过30%时，其中一个边界框将被抑制
    )
    best_box = detection[keep]  # 根据NMS的结果，选择保留的框

    return best_box.cpu().numpy()  # 将选择的框转换为NumPy数组，并返回
