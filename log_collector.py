#!/usr/bin/python3
# -*- coding: utf-8 -*-

import zipfile
import sys
import os
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication, QGridLayout, QPushButton, QLineEdit, QCheckBox)


WORKING_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_ZIP_PATH = 'D:\downloads\\'
BACK_SERVER_PATH = WORKING_PATH + "\credo"
FRONT_SERVER_PATH = WORKING_PATH + "\credo_front"
logs_list = ['app.log', 'credo.log', 'ibank.log', 'request.log', 'server.log']
# logs_list = []

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.log_path = "\\nodes\\node1\standalone\\"
        self.copyLog = QPushButton('Copy logs')
        self.lbl1 = QLabel('back server path : ', self)
        self.lbl2 = QLabel('front server path: ', self)
        self.back_server_path = QLineEdit()
        self.back_server_path.setText(BACK_SERVER_PATH)
        self.front_server_path = QLineEdit()
        self.front_server_path.setText(FRONT_SERVER_PATH)
        self.back_check = QCheckBox('Copy back logs', self)
        self.front_check = QCheckBox('Copy front logs', self)

        self.lbl3 = QLabel("Selected Node: ", self)
        self.lbl3_1 = QLabel("Other Node name: ", self)

        self.combo = QComboBox(self)
        self.combo.addItems(["node1", "node2", "node3", "node4", "node5", "node6", "node7",
                              "node8", "node9", "other"])
        self.other_node_edit = QLineEdit()

        self.lbl3.setText("Selected Node: " + str(self.combo.itemText(self.combo.currentIndex())))



        self.lbl4 = QLabel('Select logs: ', self)
        self.app_log = QCheckBox('app.log')
        self.credo_log = QCheckBox('credo.log')
        self.ibank_log = QCheckBox('ibank.log')
        self.request_log = QCheckBox('request.log')
        self.server_log = QCheckBox('server.log')

        self.lbl5 = QLabel('Enter request number: ', self)
        self.request_number_edit = QLineEdit()
        self.lbl6 = QLabel('', self)    #result

        grid = QGridLayout()
        # grid.setSpacing(5)

        grid.addWidget(self.lbl1, 1, 0)
        grid.addWidget(self.back_server_path, 1, 1)

        grid.addWidget(self.lbl2, 2, 0)
        grid.addWidget(self.front_server_path, 2, 1)

        grid.addWidget(self.back_check, 3, 0)
        grid.addWidget(self.front_check, 3, 1)

        grid.addWidget(self.lbl3, 6, 0)
        grid.addWidget(self.combo, 6, 1)

        grid.addWidget(self.lbl3_1, 7, 0)
        grid.addWidget(self.other_node_edit, 7, 1)

        grid.addWidget(self.lbl4, 8, 0)
        grid.addWidget(self.app_log, 9, 0)
        grid.addWidget(self.credo_log, 9, 1)
        grid.addWidget(self.ibank_log, 10, 0)
        grid.addWidget(self.request_log, 10, 1)
        grid.addWidget(self.server_log, 11, 1)

        grid.addWidget(self.lbl5, 12, 0)
        grid.addWidget(self.request_number_edit, 12, 1)

        grid.addWidget(self.copyLog, 13, 1)
        grid.addWidget(self.lbl6, 14, 0)

        self.back_check.setChecked(True)
        self.combo.activated[str].connect(self.combobox_node)

        self.other_node_edit.setDisabled(True)
        self.app_log.setChecked(True)
        self.credo_log.setChecked(True)
        self.ibank_log.setChecked(True)
        self.request_log.setChecked(True)
        self.server_log.setChecked(True)

        self.copyLog.clicked.connect(lambda: self.create_zip_logs(self.request_number_edit.text()))

        self.setLayout(grid)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Log collector')
        self.show()

        self.request_number_edit.setFocus()
        self.app_log.stateChanged.connect(lambda: self.select_app_logs(self.app_log))
        self.ibank_log.stateChanged.connect(lambda: self.select_ibank_logs(self.ibank_log))
        self.credo_log.stateChanged.connect(lambda: self.select_credo_logs(self.credo_log))
        self.request_log.stateChanged.connect(lambda: self.select_request_logs(self.request_log))
        self.server_log.stateChanged.connect(lambda: self.select_server_logs(self.server_log))

    def combobox_node(self, text):
        if text != 'other':
            self.other_node_edit.setDisabled(True)
            self.lbl3.setText("Selected Node: " + text)
            self.lbl3.adjustSize()
            self.other_node_edit.clear()
        else:
            self.lbl3.setText("Selected Node: ")
            self.other_node_edit.setDisabled(False)
        return text

    def get_node_name(self):
        node_name = self.combo.itemText(self.combo.currentIndex())
        if node_name == 'other':
            node_name = self.other_node_edit.text()
            if not node_name:
                node_name = 'other'
        return node_name

    def select_app_logs(self, checkbox):
        if checkbox.isChecked() == True:
            logs_list.append(checkbox.text())
        else:
            logs_list.remove(checkbox.text())
        return logs_list

    def select_ibank_logs(self, checkbox):
        if checkbox.isChecked() == True:
            logs_list.append(checkbox.text())
        else:
            logs_list.remove(checkbox.text())
        return logs_list

    def select_credo_logs(self, checkbox):
        if checkbox.isChecked() == True:
            logs_list.append(checkbox.text())
        else:
            logs_list.remove(checkbox.text())
        return logs_list

    def select_request_logs(self, checkbox):
        if checkbox.isChecked() == True:
            logs_list.append(checkbox.text())
        else:
            logs_list.remove(checkbox.text())
        return logs_list

    def select_server_logs(self, checkbox):
        if checkbox.isChecked() == True:
            logs_list.append(checkbox.text())
        else:
            logs_list.remove(checkbox.text())
        return logs_list

    def create_zip(self, name, files):
        node_name = self.get_node_name()
        self.log_path = "\\nodes\\" + node_name + "\standalone\\log\\"
        with zipfile.ZipFile(LOG_ZIP_PATH + name + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            if self.back_check.isChecked() == True:
                for file in files:
                    print(file)
                    zip.write(BACK_SERVER_PATH + self.log_path + file, 'credo_' + file)
            if self.front_check.isChecked() == True:
                for file in files:
                    print(file)
                    zip.write(FRONT_SERVER_PATH + self.log_path + file, 'front_' + file)

    def create_zip_logs(self, number_request):
        self.lbl6.setText('')


        if not (self.back_check.isChecked() == False and self.front_check.isChecked() == False):
            if not number_request:
                self.create_zip('logs', logs_list)
                self.lbl6.setText('logs.zip is created')
            else:
                self.create_zip(number_request, logs_list)
                self.lbl6.setText(number_request + ".zip is created")
        else:
            self.lbl6.setText('No selected server!!!')



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())