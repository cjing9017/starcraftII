from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from module.video.VideoPlayerForm import Ui_MainWindow
from module.video.DoubleClickedVideoWidget import VideoWidgetDoubleClicked
import sys


class VideoPlayWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.videoFullScreen = False   # 判断当前widget是否全屏
        self.videoFullScreenWidget = VideoWidgetDoubleClicked()   # 创建一个全屏的widget
        self.videoFullScreenWidget.setFullScreen(1)
        self.videoFullScreenWidget.hide()               # 不用的时候隐藏起来
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)  # 视频播放输出的widget，就是上面定义的
        self.btn_open.clicked.connect(self.open_video_file)   # 打开视频文件按钮
        self.btn_play.clicked.connect(self.play_video)       # play
        self.btn_stop.clicked.connect(self.pause_video)       # pause
        self.player.positionChanged.connect(self.change_slide)      # change Slide
        self.videoFullScreenWidget.doubleClickedItem.connect(self.video_double_clicked)  #双击响应
        self.wgt_video.doubleClickedItem.connect(self.video_double_clicked)   #双击响应

    def open_video_file(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        self.player.play()  # 播放视频

    def play_video(self):

        self.player.play()

    def pause_video(self):
        self.player.pause()

    def change_slide(self, position):
        self.vidoeLength = self.player.duration()+0.1
        self.sld_video.setValue(round((position/self.vidoeLength)*100))
        self.lab_video.setText(str(round((position/self.vidoeLength)*100, 2))+'%')

    def video_double_clicked(self, text):
        if self.player.duration() > 0:  # 开始播放后才允许进行全屏操作
            if self.videoFullScreen:
                self.player.pause()
                self.videoFullScreenWidget.hide()
                self.player.setVideoOutput(self.wgt_video)
                self.player.play()
                self.videoFullScreen = False
            else:
                self.player.pause()
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.player.play()
                self.videoFullScreen = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = VideoPlayWindow()
    vieo_gui.show()
    sys.exit(app.exec_())