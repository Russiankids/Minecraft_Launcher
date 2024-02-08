import minecraft_launcher_lib
from PyQt5 import QtCore, QtGui, QtWidgets
from random_username.generate import generate_username
from uuid import uuid1
import subprocess

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'deflauncher')

class LaunchThread(QtCore.QThread):

    launch_setup_signal = QtCore.pyqtSignal(str, str)
    progress_update_signal = QtCore.pyqtSignal(int, int, str)
    state_update_signal = QtCore.pyqtSignal(bool)

    version_id = ''
    username = ''
    prong = 0
    prong_max = 0
    prong_label = ''

    def __init__(self):
        super().__init__()
        self.launch_setup_signal.connect(self.launch_setup)

    def launch_setup(self, version_id, username):
        self.version_id = version_id
        self.username = username

    def update_progress_label(self, value):
        self.prong_label = value
        self.progress_update_signal.emit(self.prong, self.prong_max, self.prong_label)
    def update_progress(self, value):
        self.prong = value
        self.progress_update_signal.emit(self.prong, self.prong_max, self.prong_label)
    def update_progress_max(self, value):
        self.prong_max = value
        self.progress_update_signal.emit(self.prong, self.prong_max, self.prong_label)

    def run(self):
        self.state_update_signal.emit(True)
        minecraft_launcher_lib.install.install_minecraft_version(versionid=self.version_id, minecraft_directory=minecraft_directory, callback={ 'setStatus': self.update_progress_label, 'setProgress': self.update_progress, 'setMax': self.update_progress_max})
        if self.username == '':
            self.username = generate_username()[0]
        options = {
            'username': self.username,
            'uuid': str(uuid1()),
            'token': ''
        }
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version = self.version_id, minecraft_directory=minecraft_directory, options=options))

        self.state_update_signal.emit(False)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(383, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(256, 70))
        self.label.setBaseSize(QtCore.QSize(240, 240))
        self.label.setText("")
        self.label.setPixmap(
            QtGui.QPixmap("assets/2b2mk2rpkn3sy0ptbabmzflxae0ulg9h78f60jga1jue2z9rgei0c93ykiphln5u.png"))
        self.label.setScaledContents(True)
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText('Username')
        self.verticalLayout.addWidget(self.lineEdit)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")

        for version in minecraft_launcher_lib.utils.get_version_list():
            self.comboBox.addItem(version['id'])

        self.verticalLayout.addWidget(self.comboBox)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.verticalLayout.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('Launch')
        self.pushButton.clicked.connect(self.launch_game)
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 383, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_prog)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def state_update(self, value):
        self.pushButton.setDisabled(value)
        self.progressBar.setVisible(value)

    def update_prog(self, proj, max_proj):
        self.progressBar.setValue(proj)
        self.progressBar.setMaximum(max_proj)
    def launch_game(self):
        self.launch_thread.launch_setup_signal.emit(self.comboBox.currentText(), self.lineEdit.text())
        self.launch_thread.start()


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
