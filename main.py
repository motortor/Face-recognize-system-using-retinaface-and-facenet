from PyQt5 import QtWidgets  # 导入PyQt5中的模块
from mainwindow import MainWindow  # 导入MainWindow类
import sys  # 导入sys模块

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个Qt应用程序对象，用于管理应用程序的事件循环和GUI
    mainWindow = MainWindow()  # 创建一个主窗口对象
    mainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 进入事件循环并等待应用程序退出
