import os  # 导入os模块，提供访问操作系统功能的方法
import time  # 导入time模块，提供时间相关的函数
import cv2  # 导入cv2模块，提供图像处理相关的函数
import numpy as np  # 导入numpy模块，提供多维数组和矩阵处理功能
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia  # 导入PyQt5中的模块
from PyQt5.QtCore import QUrl  # 导入PyQt5.QtCore中的类
from PyQt5.QtWidgets import QFileDialog  # 导入PyQt5.QtWidgets中的类
from retinaface import Retinaface  # 导入Retinaface类，用于人脸检测
from ui_mainwindow import Ui_MainWindow  # 导入ui_mainwindow.py中的Ui_MainWindow类
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog, QMessageBox
from PyQt5.QtCore import QDateTime


class PasswordDialog(QDialog):  # 点击"录入"时，为了只让管理员操作，所以弹出密码框
    def __init__(self):
        super().__init__()
        self.setWindowTitle('请输入密码：')
        self.password_edit = QLineEdit(self)  # 创建一个单行文本编辑器用于输入密码
        self.password_edit.setEchoMode(QLineEdit.Password)  # 设置文本编辑器的回显模式为密码,"QLineEdit.Normal"为默认模式
        self.confirm_button = QPushButton('确认', self)  # 创建一个按钮用于确认密码
        self.confirm_button.clicked.connect(self.check_password)  # 将按钮的 clicked 信号连接到 check_password 方法
        # 创建一个垂直布局管理器，并将文本编辑器和按钮添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.password_edit)  # 输入密码的编辑框
        layout.addWidget(self.confirm_button)  # 确认按钮
        self.setLayout(layout)  # 将布局设置为对话框的布局
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)  # 去掉帮助按钮

    def check_password(self):
        password = self.password_edit.text()  # 获取文本编辑器中输入的密码
        if password == '666666':  # 如果密码正确，则接受对话框
            self.accept()
        else:  # 如果密码错误，则弹出警告框
            QMessageBox.warning(self, '警告', '密码错误')

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        self.camera_active = False  # 添加一个状态变量，用于跟踪摄像头和显示是否已经打开

        super(MainWindow, self).__init__(parent)

        self.setupUi(self)  # 初始化控件布局
        self.initialParams()  # 初始化参数
        self.initialSlots()  # 初始化槽函数

        self.nameliist = []  # 名字列表

    def initialParams(self):
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()  # 视频流
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头

        self.retinaface = Retinaface()
        self.retinaface_train = Retinaface(1)

    def initialSlots(self):
        # 定时器
        self.timer_camera.timeout.connect(self.show_camera)
        # 按钮
        self.pushButton_shibie.clicked.connect(self.pushButton_shibie_clicked)
        self.pushButton_kaimen.clicked.connect(self.pushButton_kaimen_clicked)
        self.pushButton_luru.clicked.connect(self.pushButton_luru_clicked)
        self.pushButton_paizhao.clicked.connect(self.pushButton_paizhao_clicked)
        self.pushButton_fanhui.clicked.connect(self.pushButton_fanhui_clicked)
        self.pushButton_chushihua.clicked.connect(self.pushButton_chushihua_clicked)
        self.pushButton_fenxi.clicked.connect(self.pushButton_fenxi_clicked)
        self.pushButton_biaoge.clicked.connect(self.pushButton_biaoge_clicked)
        self.pushButton_zhexiantu.clicked.connect(self.pushButton_zhexiantu_clicked)
        self.pushButton_fanhui2.clicked.connect(self.pushButton_fanhui2_clicked)

    ##############################################
    # 点击识别
    def pushButton_shibie_clicked(self):
        if not self.camera_active:  # 若摄像头未启动
            self.cap = cv2.VideoCapture(self.CAM_NUM)  # 初始化摄像头
            self.timer_camera.start(30)  # 启动计时器，每隔30ms读取一帧图像
            self.label_status.setStyleSheet("color: black")
            self.label_status.setText("未开门")
            self.pushButton_shibie.setText("关闭摄像头")  # 修改按钮文本
            self.camera_active = True
        else:  # 若摄像头已启动
            self.timer_camera.stop()  # 停止计时器
            self.cap.release()  # 释放摄像头资源
            self.label_video.clear()  # 清空视频标签的内容
            self.label_status.setStyleSheet("color: black")
            self.label_status.setText("摄像头已关闭")
            self.pushButton_shibie.setText("识别")  # 修改按钮文本
            self.camera_active = False  # 将摄像头状态设置为已关闭

    def show_camera(self):
        if not self.camera_active:
            return

        flag, self.image = self.cap.read()  # 从相机读取一帧图像
        frame = cv2.resize(self.image, (640, 480))  # 调整图像大小为(600, 400)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色

        old_image, namelist = self.retinaface.detect_image(frame)  # 通过RetinaFace进行人脸检测，返回检测结果和人名列表
        self.nameliist = namelist  # 将人名列表保存到类属性self.nameliist中
        # print(namelist)
        frame = np.array(old_image)  # 将旧图像转换为numpy数组
        # 把读取到的视频数据变成QImage形式
        showImage = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.label_video.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 在Qt界面上显示图像

    ###############################
    # 开门
    def pushButton_kaimen_clicked(self):
        if not self.camera_active:  # 若摄像头未启动
            msg = QtWidgets.QMessageBox.information(self, 'FAILED', "摄像头未开启！", buttons=QtWidgets.QMessageBox.Ok)
        else:
            face_names2 = self.nameliist
            now = QDateTime.currentDateTime()  # 获取当前日期和时间
            timestamp = now.toString("yyyy/MM/dd-hh:mm:ss")  # 格式化时间为字符串
            if len(face_names2) == 1 and face_names2[0] != 'Unknown':  # 如果只识别到一个人且身份不为Unknown
                name = face_names2[0]  # 获取人名
                self.label_status.setStyleSheet("color: green")
                self.label_status.setText("已开门")
                if int(now.time().hour()) >= 23:
                    with open('jilu.txt', 'a', encoding='utf-8') as f:  # 打开文件
                        f.write(f"{name}  {timestamp}  晚归\n")  # 写入记录
                    url = QUrl.fromLocalFile("music/早点回来.mp3")
                    content = QtMultimedia.QMediaContent(url)  # 创建一个 QMediaContent 对象，参数是一个 URL，用于媒体内容的播放
                    player = QtMultimedia.QMediaPlayer()  # 创建一个 QMediaPlayer 对象，用于控制媒体的播放
                    player.setMedia(content)  # 将 QMediaContent 对象设置为 QMediaPlayer 对象的媒体内容
                    player.setVolume(100)  # 设置 QMediaPlayer 对象的音量为 100
                    player.play()  # 开始播放媒体
                    time.sleep(1)  # 程序暂停 1 秒钟，让媒体播放一段时间后停止
                    msg = QtWidgets.QMessageBox.information(self, '已开门', "下次要早点回来哦！", buttons=QtWidgets.QMessageBox.Ok)
                else:
                    with open('jilu.txt', 'a', encoding='utf-8') as f:  # 打开文件
                        f.write(f"{name}  {timestamp}  准时\n")  # 写入记录
                    url = QUrl.fromLocalFile("music/开门.wav")
                    content = QtMultimedia.QMediaContent(url)
                    player = QtMultimedia.QMediaPlayer()
                    player.setMedia(content)
                    player.setVolume(100)
                    player.play()
                    time.sleep(1)
                    msg = QtWidgets.QMessageBox.information(self, '已开门', "欢迎回来！", buttons=QtWidgets.QMessageBox.Ok)
            else:
                self.label_status.setStyleSheet("color: red")
                self.label_status.setText("识别失败，无法开门")
                msg = QtWidgets.QMessageBox.information(self, 'FAILED', "人脸识别失败或人数≠1", buttons=QtWidgets.QMessageBox.Ok)

    ##############################################
    # 录入
    def pushButton_luru_clicked(self):
        password_dialog = PasswordDialog()  # 创建一个 PasswordDialog 对象，即密码输入对话框
        if password_dialog.exec_() == QDialog.Accepted:   # 如果用户输入的密码正确
            self.stackedWidget.setCurrentIndex(1)  # 则将当前页面切换到索引为 1 的页面，即录入人脸的页面

    def pushButton_paizhao_clicked(self):
        face_names2 = self.nameliist
        flag, self.image = self.cap.read()  # 从视频流中读取
        if flag and len(face_names2) == 1:  # 判断摄像头是否打开且只识别到一个人
            img = cv2.resize(self.image, (640, 480))  # 将图像的大小调整为 640*480
            # 通过 QFileDialog 弹出一个保存文件对话框
            # 获取保存文件的路径及文件类型（jpg 或 png）
            fname, ftype = QFileDialog.getSaveFileName(self, 'save file', './face_dataset', "Image files(*.jpg *.png)")
            if fname != "":  # 如果选择了保存文件的路径
                cv2.imwrite(fname, img)  # 使用 cv2.imwrite() 函数将图像保存到指定路径
                # 在消息框中提示用户保存成功
                msg = QtWidgets.QMessageBox.information(self, 'SUCCESS', "保存成功", buttons=QtWidgets.QMessageBox.Ok)
        else:
            msg = QtWidgets.QMessageBox.information(self, 'FAILED', "摄像头未打开或人数≠1", buttons=QtWidgets.QMessageBox.Ok)

    def pushButton_fanhui_clicked(self):   # 当 "返回" 按钮被点击时
        self.stackedWidget.setCurrentIndex(0)  # 将当前页面切换到索引为 0 的页面，即主页面

    ##############################################
    # 初始化
    def pushButton_chushihua_clicked(self):
        password_dialog = PasswordDialog()  # 创建一个 PasswordDialog 对象，即密码输入对话框
        if password_dialog.exec_() == QDialog.Accepted:  # 如果用户输入的密码正确
            list_dir = os.listdir("face_dataset")
            # 读取名为"face_dataset"的目录下的所有文件和目录的名称，将其以列表的形式返回，并将返回的列表存储在 'list_dir'变量中
            image_paths = []
            names = []
            # 创建两个空列表'image_paths'和 'names'，用于存储"face_dataset"目录中所有图像文件的路径和文件名（不包含文件扩展名）

            for name in list_dir:  # 使用for循环遍历目录中的所有文件和目录名称
                image_paths.append("face_dataset/" + name)  # .append()用于将新元素添加到列表的末尾 list.append(item)
                # 将每个文件名的"face_dataset/"和 'name' 拼接成一个新的字符串，表示该目录下图像文件的路径,并将其添加到'image_paths'列表中
                names.append(name.split("_")[0])
                # 文件名中找到第一个下划线之前的字符串作为人物的名称，并将其添加到 'names' 列表中
                # 例如：LYH_1.jpg执行 'name.split("_")[0]'后会得到 'LYH'

            # 这段代码可以将 "face_dataset" 目录中所有图像文件的绝对路径和文件名提取出来，并将人物名称存储在 'names' 列表中，以备后续的人脸检测使用

            self.retinaface_train.encode_face_dataset(image_paths, names)
            # 调用 retinaface.py 中 'encode_face_dataset' 函数，并将 'image_paths' 和 'names' 作为输入参数传递给该函数
            self.retinaface = Retinaface()
            self.retinaface_train = Retinaface(1)
            msg = QtWidgets.QMessageBox.information(self, 'SUCCESS', "初始化完成！", buttons=QtWidgets.QMessageBox.Ok)
            pass

    ##############################################
    # 分析
    def pushButton_fenxi_clicked(self):
        password_dialog = PasswordDialog()  # 创建一个 PasswordDialog 对象，即密码输入对话框
        if password_dialog.exec_() == QDialog.Accepted:   # 如果用户输入的密码正确
            self.stackedWidget.setCurrentIndex(2)  # 则将当前页面切换到索引为 2 的页面，即分析的页面

    def pushButton_biaoge_clicked(self):
        import subprocess
        subprocess.Popen(['python', 'biaoge.py'])
        time.sleep(1)
        if os.path.exists("output.xlsx"):
            os.startfile("output.xlsx")
            msg = QtWidgets.QMessageBox.information(self, 'SUCCESS', "表格已生成！", buttons=QtWidgets.QMessageBox.Ok)
        else:
            msg = QtWidgets.QMessageBox.information(self, 'ERROR', "程序运行失败！", buttons=QtWidgets.QMessageBox.Ok)

    def pushButton_zhexiantu_clicked(self):
        import subprocess
        try:
            subprocess.Popen(['python', 'zhexiantu.py'])
            time.sleep(1)
            msg = QtWidgets.QMessageBox.information(self, 'SUCCESS', "折线图已生成！", buttons=QtWidgets.QMessageBox.Ok)
        except subprocess.CalledProcessError as e:
            msg = QtWidgets.QMessageBox.information(self, 'ERROR', "程序运行失败！", buttons=QtWidgets.QMessageBox.Ok)

    def pushButton_fanhui2_clicked(self):  # 当 "返回" 按钮被点击时
        self.stackedWidget.setCurrentIndex(0)  # 将当前页面切换到索引为 0 的页面，即主页面
