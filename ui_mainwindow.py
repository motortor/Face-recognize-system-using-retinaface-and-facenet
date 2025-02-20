from PyQt5 import QtCore, QtGui, QtWidgets  # 导入PyQt5中的QtCore, QtGui, QtWidgets模块

# 创建Ui_MainWindow类
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ##############################################
        # "MainWindow"
        # 设置主窗口名称
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)  # 设置主窗口大小
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 创建一个垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        # 创建一个占位符对象（宽度，高度，水平方向尽可能缩小，垂直方向尽可能扩大）
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)  # 将其添加到垂直布局中

        ##############################################
        # 标题："宿舍门禁系统"
        # 创建一个标签对象，并将其添加到中心窗口部件的布局器中
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(20)  # 设置字体大小
        self.label.setFont(font)  # 将字体对象设置为标签的字体
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # 将标签的对齐方式设置为居中
        self.label.setObjectName("label")  # 设置标签的名称
        self.verticalLayout.addWidget(self.label)  # 将标签添加到垂直布局器中
        # 创建一个水平布局器_4对象
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        # 创建一个占位符对象
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)  # 将其添加到水平布局器_4中

        ##############################################
        # 状态栏："状态栏"
        # 创建一个标签对象，并将其添加到中心窗口部件的布局器中
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        font.setBold(True)
        self.label_status.setFont(font)  # 将字体对象设置为标签的字体
        self.label_status.setText("状态栏")  # 设置标签控件的文本内容
        self.label_status.setObjectName("label_status")  # 设置标签的名称
        self.horizontalLayout_4.addWidget(self.label_status)   # 将标签添加到水平布局器_4中
        # 创建一个占位符对象
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)  # 将其添加到水平布局器中
        self.horizontalLayout_4.setStretch(0, 1)  # 将第1个子控件（spacerItem1）设置为可拉伸
        self.horizontalLayout_4.setStretch(1, 1)  # 将第2个子控件（label_status）设置为可拉伸
        self.horizontalLayout_4.setStretch(2, 24)  # 将第3个子控件（spacerItem2）设置为24倍拉伸
        self.verticalLayout.addLayout(self.horizontalLayout_4)  # 将水平布局添加到垂直布局_4中
        # 创建一个新的水平布局
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")  # 设置布局的对象名称
        # 创建一个占位符对象
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)  # 将其添加到水平布局中

        ##############################################
        # 视频窗口
        # 创建一个标签对象，并将其添加到中心窗口部件的布局器中
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        # 设置水平和垂直大小调整策略为Expanding，表示可以自由扩展
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # 将水平和垂直大小调整策略设置为0，表示没有水平或垂直的伸缩性
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_video.sizePolicy().hasHeightForWidth())  # 在调整大小时保持纵横比
        self.label_video.setSizePolicy(sizePolicy)  # 设置大小调整策略
        self.label_video.setStyleSheet("")  # 设置样式表为空
        self.label_video.setFrameShape(QtWidgets.QFrame.StyledPanel)  # 设置框架形状
        self.label_video.setFrameShadow(QtWidgets.QFrame.Plain)  # 边框阴影样式设置为普通的边框
        self.label_video.setText("")  # 文本为空
        self.label_video.setScaledContents(True)  # 缩放内容设置为True，表示内容将自适应大小调整
        # 对齐方式为左对齐、顶对齐、以及从左到右的方向
        self.label_video.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_video.setObjectName("label_video")  # 设置标签的名称
        self.horizontalLayout.addWidget(self.label_video)  # 将标签添加到水平布局中
        # 创建一个占位符对象
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)  # 将其添加到水平布局中

        ##############################################
        # 创建一个堆叠窗口，并将其添加到主窗口上
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")  # 设置堆叠窗口名称
        # 创建一个名为page的窗口
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        # 创建一个水平布局器_2对象
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # 创建一个占位符对象
        spacerItem5 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)  # 将其添加到水平布局器_2中
        # 创建一个垂直布局器_2对象
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # 创建一个占位符对象
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)  # 将其添加到垂直布局器_2中

        ##############################################
        # 识别按钮
        # 创建一个名为shibie的按钮，将其添加到page界面中
        self.pushButton_shibie = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_shibie.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_shibie.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_shibie.setObjectName("pushButton_shibie")  # 设置按钮的对象名称
        self.verticalLayout_2.addWidget(self.pushButton_shibie)  # 将按钮添加到垂直布局器_2中
        # 创建一个占位符对象
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)  # 将其添加到垂直布局器_2中

        ##############################################
        # 开门按钮
        # 创建一个名为kaimen的按钮，将其添加到page界面中
        self.pushButton_kaimen = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_kaimen.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_kaimen.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_kaimen.setObjectName("pushButton_kaimen")  # 设置按钮的对象名称
        self.verticalLayout_2.addWidget(self.pushButton_kaimen)  # 将按钮添加到垂直布局器_2中
        # 创建一个占位符对象
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem8)  # 将其添加到垂直布局器_2中

        ##############################################
        # 录入按钮
        # 创建一个名为luru的按钮，将其添加到page界面中
        self.pushButton_luru = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_luru.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_luru.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_luru.setObjectName("pushButton_luru")  # 设置按钮的对象名称
        self.verticalLayout_2.addWidget(self.pushButton_luru)  # 将按钮添加到垂直布局器_2中
        # 创建一个占位符对象
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem9)  # 将其添加到垂直布局器_2中

        ##############################################
        # 训练按钮
        # 创建一个名为chushihua的按钮，将其添加到page界面中
        self.pushButton_chushihua = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_chushihua.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_chushihua.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_chushihua.setObjectName("pushButton_chushihua")  # 设置按钮的对象名称
        self.verticalLayout_2.addWidget(self.pushButton_chushihua)  # 将按钮添加到垂直布局器_2中
        # 创建一个占位符对象
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem10)  # 将其添加到垂直布局器_2中

        ##############################################
        # 分析按钮
        # 创建一个名为fenxi的按钮，将其添加到page界面中
        self.pushButton_fenxi = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_fenxi.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_fenxi.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_fenxi.setObjectName("pushButton_fenxi")  # 设置按钮的对象名称
        self.verticalLayout_2.addWidget(self.pushButton_fenxi)  # 将按钮添加到垂直布局器_2中
        # 创建一个占位符对象
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem19)  # 将其添加到垂直布局器_2中

        # 垂直布局拉伸
        self.verticalLayout_2.setStretch(0, 1)  # 将第1个子控件（spacerItem6）设置为可拉伸
        self.verticalLayout_2.setStretch(1, 2)  # 将第2个子控件（self.pushButton_shibie）设置为2倍拉伸
        self.verticalLayout_2.setStretch(2, 1)  # 将第3个子控件（spacerItem7）设置为可拉伸
        self.verticalLayout_2.setStretch(3, 2)  # 将第4个子控件（self.pushButton_kaimen）设置为2倍拉伸
        self.verticalLayout_2.setStretch(4, 1)  # 将第5个子控件（spacerItem8）设置为可拉伸
        self.verticalLayout_2.setStretch(5, 2)  # 将第6个子控件（self.pushButton_luru）设置为2倍拉伸
        self.verticalLayout_2.setStretch(6, 1)  # 将第7个子控件（spacerItem9）设置为可拉伸
        self.verticalLayout_2.setStretch(7, 2)  # 将第8个子控件（self.pushButton_xunlian）设置为2倍拉伸
        self.verticalLayout_2.setStretch(8, 1)  # 将第9个子控件（spacerItem10）设置为可拉伸
        self.verticalLayout_2.setStretch(9, 2)  # 将第10个子控件（self.pushButton_fenxi）设置为2倍拉伸
        self.verticalLayout_2.setStretch(10, 1)  # 将第11个子控件（spacerItem19）设置为可拉伸
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)  # 将垂直布局器_2添加到水平布局器_2中
        # 创建一个占位符对象
        spacerItem11 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem11)  # 将其添加到水平布局器_2中
        # 水平布局拉伸
        self.horizontalLayout_2.setStretch(0, 1)  # 将第1个子控件（spacerItem5）设置为可拉伸
        self.horizontalLayout_2.setStretch(1, 3)  # 将第2个子控件（self.verticalLayout_2）设置为3倍拉伸
        self.horizontalLayout_2.setStretch(2, 1)  # 将第3个子控件（spacerItem11）设置为可拉伸

        # 将页面1加入堆叠窗口中
        self.stackedWidget.addWidget(self.page)

        ############################################################################################
        # 第二页
        # 创建一个名为page_2的窗口
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        # 创建一个水平布局器_3对象
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # 创建一个占位符对象
        spacerItem12 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)  # 将其添加到水平布局器_3中
        # 创建一个垂直布局器_3对象
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        # 创建一个占位符对象
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem13)  # 将其添加到垂直布局器_3中

        ##############################################
        # 拍照按钮
        # 创建一个名为paizhao的按钮，将其添加到page_2界面中
        self.pushButton_paizhao = QtWidgets.QPushButton(self.page_2)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_paizhao.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_paizhao.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_paizhao.setObjectName("pushButton_paizhao")  # 设置按钮的对象名称
        self.verticalLayout_3.addWidget(self.pushButton_paizhao)  # 将按钮添加到垂直布局器_3中
        # 创建一个占位符对象
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem14)  # 将其添加到垂直布局器_3中

        ##############################################
        # 返回按钮
        # 创建一个名为返回的按钮，将其添加到page_2界面中
        self.pushButton_fanhui = QtWidgets.QPushButton(self.page_2)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_fanhui.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_fanhui.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_fanhui.setObjectName("pushButton_fanhui")  # 设置按钮的对象名称
        self.verticalLayout_3.addWidget(self.pushButton_fanhui)  # 将按钮添加到垂直布局器_3中
        # 创建一个占位符对象
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem15)  # 将其添加到垂直布局器_3中

        # 垂直布局拉伸
        self.verticalLayout_3.setStretch(0, 3)  # 将第1个子控件（spacerItem13）设置为3倍拉伸
        self.verticalLayout_3.setStretch(1, 2)  # 将第2个子控件（self.pushButton_paizhao）设置为2倍拉伸
        self.verticalLayout_3.setStretch(2, 1)  # 将第3个子控件（spacerItem14）设置为可拉伸
        self.verticalLayout_3.setStretch(3, 2)  # 将第4个子控件（self.pushButton_fanhui）设置为2倍拉伸
        self.verticalLayout_3.setStretch(4, 3)  # 将第5个子控件（spacerItem15）设置为3倍拉伸
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)  # 将垂直布局器_3添加到水平布局器_3中
        # 创建一个占位符对象
        spacerItem16 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem16)  # 将其添加到水平布局器_3中
        self.horizontalLayout_3.setStretch(0, 1)  # 将第1个子控件（spacerItem12）设置为可拉伸
        self.horizontalLayout_3.setStretch(1, 3)  # 将第2个子控件（self.verticalLayout_3）设置为3倍拉伸
        self.horizontalLayout_3.setStretch(2, 1)  # 将第3个子控件（spacerItem16）设置为可拉伸
        # 将页面2加入堆叠窗口
        self.stackedWidget.addWidget(self.page_2)

        ############################################################################################
        # 第三页
        # 创建一个名为page_3的窗口
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        # 创建一个水平布局器_5对象
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        # 创建一个占位符对象
        spacerItem20 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem20)  # 将其添加到水平布局器_5中
        # 创建一个垂直布局器_4对象
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        # 创建一个占位符对象
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem21)  # 将其添加到垂直布局器_5中

        ##############################################
        # 表格按钮
        # 创建一个名为biaoge的按钮，将其添加到page_3界面中
        self.pushButton_biaoge = QtWidgets.QPushButton(self.page_3)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_biaoge.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_biaoge.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_biaoge.setObjectName("pushButton_biaoge")  # 设置按钮的对象名称
        self.verticalLayout_5.addWidget(self.pushButton_biaoge)  # 将按钮添加到垂直布局器_5中
        # 创建一个占位符对象
        spacerItem22 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem22)  # 将其添加到垂直布局器_5中

        ##############################################
        # 折线图按钮
        # 创建一个名为zhexiantu的按钮，将其添加到page_3界面中
        self.pushButton_zhexiantu = QtWidgets.QPushButton(self.page_3)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_zhexiantu.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_zhexiantu.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_zhexiantu.setObjectName("pushButton_zhexiantu")  # 设置按钮的对象名称
        self.verticalLayout_5.addWidget(self.pushButton_zhexiantu)  # 将按钮添加到垂直布局器_5中
        # 创建一个占位符对象
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem23)  # 将其添加到垂直布局器_5中

        ##############################################
        # 返回按钮
        # 创建一个名为返回2的按钮，将其添加到page_3界面中
        self.pushButton_fanhui2 = QtWidgets.QPushButton(self.page_3)
        font = QtGui.QFont()  # 创建字体对象
        font.setPointSize(16)  # 设置字体大小
        self.pushButton_fanhui2.setFont(font)  # 将字体对象设置为按钮的字体
        self.pushButton_fanhui2.setFixedSize(200, 50)  # 设置按钮的大小
        self.pushButton_fanhui2.setObjectName("pushButton_fanhui2")  # 设置按钮的对象名称
        self.verticalLayout_5.addWidget(self.pushButton_fanhui2)  # 将按钮添加到垂直布局器_5中
        # 创建一个占位符对象
        spacerItem24 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem24)  # 将其添加到垂直布局器_5中

        # 垂直布局拉伸
        self.verticalLayout_5.setStretch(0, 3)  # 将第1个子控件（spacerItem21）设置为3倍拉伸
        self.verticalLayout_5.setStretch(1, 2)  # 将第2个子控件（self.pushButton_biaoge）设置为2倍拉伸
        self.verticalLayout_5.setStretch(2, 1)  # 将第3个子控件（spacerItem22）设置为可拉伸
        self.verticalLayout_5.setStretch(3, 2)  # 将第4个子控件（self.pushButton_zhexiantu）设置为2倍拉伸
        self.verticalLayout_5.setStretch(4, 1)  # 将第3个子控件（spacerItem23）设置为可拉伸
        self.verticalLayout_5.setStretch(5, 2)  # 将第4个子控件（self.pushButton_fanhui2）设置为2倍拉伸
        self.verticalLayout_5.setStretch(6, 3)  # 将第5个子控件（spacerItem24）设置为3倍拉伸
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)  # 将垂直布局器_5添加到水平布局器_5中
        # 创建一个占位符对象
        spacerItem25 = QtWidgets.QSpacerItem(36, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem25)  # 将其添加到水平布局器_3中
        self.horizontalLayout_5.setStretch(0, 1)  # 将第1个子控件（spacerItem20）设置为可拉伸
        self.horizontalLayout_5.setStretch(1, 3)  # 将第2个子控件（self.verticalLayout_5）设置为3倍拉伸
        self.horizontalLayout_5.setStretch(2, 1)  # 将第3个子控件（spacerItem25）设置为可拉伸
        # 将页面3加入堆叠窗口
        self.stackedWidget.addWidget(self.page_3)

        ############################################################################################
        # 在水平布局中添加堆叠窗口
        self.horizontalLayout.addWidget(self.stackedWidget)
        # 创建一个占位符对象
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem17)  # 将其添加到水平布局中
        # 水平布局拉伸
        self.horizontalLayout.setStretch(0, 1)  # 将第1个子控件（spacerItem3）设置为可拉伸
        self.horizontalLayout.setStretch(1, 20)  # 将第2个子控件（self.label_video）设置为20倍拉伸
        self.horizontalLayout.setStretch(2, 1)  # 将第3个子控件（spacerItem4）设置为可拉伸
        self.horizontalLayout.setStretch(3, 10)  # 将第4个子控件（self.stackedWidget）设置为10倍拉伸
        self.horizontalLayout.setStretch(4, 1)  # 将第5个子控件（spacerItem17）设置为可拉伸
        self.verticalLayout.addLayout(self.horizontalLayout)  # 将水平布局添加到垂直布局中
        # 创建一个占位符对象
        spacerItem18 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem18)  # 将其添加到垂直布局中
        self.verticalLayout.setStretch(0, 1)  # 将第1个子控件（spacerItem）设置为可拉伸
        self.verticalLayout.setStretch(1, 2)  # 将第2个子控件（self.label）设置为2倍拉伸
        self.verticalLayout.setStretch(2, 1)  # 将第3个子控件（self.horizontalLayout_4）设置为可拉伸
        self.verticalLayout.setStretch(3, 20)  # 将第4个子控件（self.horizontalLayout）设置为20倍拉伸
        self.verticalLayout.setStretch(4, 1)  # 将第4个子控件（spacerItem18）设置为可拉伸

        # 设置窗口的中央窗口部件
        MainWindow.setCentralWidget(self.centralwidget)
        # 创建一个状态栏对象，并将其父窗口设置为MainWindow
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")  # 设置状态栏的对象名称
        MainWindow.setStatusBar(self.statusbar)  # 将状态栏设置为窗口的状态栏
        # 翻译UI界面中的文本
        self.retranslateUi(MainWindow)
        # 设置当前堆叠窗口的索引为0
        self.stackedWidget.setCurrentIndex(0)
        # 连接UI界面中定义的信号和槽
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate  # 创建一个翻译对象
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))  # 设置主窗口的标题
        self.label.setText(_translate("MainWindow", "宿舍门禁系统"))  # 设置标签控件的文本
        # 设置按钮控件的文本
        self.pushButton_shibie.setText(_translate("MainWindow", "识别"))
        self.pushButton_kaimen.setText(_translate("MainWindow", "开门"))
        self.pushButton_luru.setText(_translate("MainWindow", "录入"))
        self.pushButton_chushihua.setText(_translate("MainWindow", "初始化"))
        self.pushButton_paizhao.setText(_translate("MainWindow", "拍照"))
        self.pushButton_fanhui.setText(_translate("MainWindow", "返回"))
        self.pushButton_fenxi.setText(_translate("MainWindow", "分析"))
        self.pushButton_biaoge.setText(_translate("MainWindow", "生成表格"))
        self.pushButton_zhexiantu.setText(_translate("MainWindow", "生成折线图"))
        self.pushButton_fanhui2.setText(_translate("MainWindow", "返回"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)  # 创建一个Qt应用程序对象，用于管理应用程序的事件循环和GUI
    MainWindow = QtWidgets.QMainWindow()  # 创建一个主窗口对象
    ui = Ui_MainWindow()  # 创建一个UI对象，该对象包含了创建和设置主窗口界面的方法
    ui.setupUi(MainWindow)  # 调用UI对象的setupUi()方法来设置主窗口的界面
    MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 进入事件循环并等待应用程序退出
