#!/usr/bin/python3
# -*- coding: utf-8 -*-

import zipfile
import sys
import os
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication, QGridLayout, QPushButton, QLineEdit, QCheckBox)
from skpy import Skype
import getpass

# TODO: сделать проверку на существование файлов, а не директории
LOG_ZIP_PATH = os.path.join(os.path.expanduser('~'), 'downloads') # Downloads folder
logs_list = ['app.log', 'credo.log', 'ibank.log', 'iss.log', 'request.log', 'server.log']

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.login_skype = input('Enter your skype login:\n')
        self.pass_skype = getpass.win_getpass('Enter your skype password:\n')
        print('Get connect to Skype...')
        self.sk = Skype(self.login_skype, self.pass_skype)  # connect to Skype
        print(self.sk.conn)

        self.BACK_ERROR = False
        self.FRONT_ERROR = False

        self.log_path = "\\nodes\\node1\standalone\\log"
        self.send_logs = QPushButton('Send logs')
        self.lbl1 = QLabel('back server path : ', self)
        self.lbl2 = QLabel('front server path: ', self)
        self.back_server_path = QLineEdit()
        self.back_server_path.setText("D:\credo")
        self.front_server_path = QLineEdit()
        self.front_server_path.setText("D:\credo_front")
        self.back_check = QCheckBox('Copy back logs', self)
        self.front_check = QCheckBox('Copy front logs', self)

        self.lbl3 = QLabel("Selected Node: ", self)
        self.lbl3_1 = QLabel("Other Node name: ", self)

        self.combo = QComboBox(self)
        self.combo.addItems(["node1", "node2", "node3", "node4", "node5", "node6", "node7",
                              "node8", "node9", "other"])

        self.user_list_combo = QComboBox(self)
        self.users_name = self.user_list()
        self.user_list_combo.addItems([str(user) for user in self.users_name.values()])

        self.other_node_edit = QLineEdit()

        self.lbl3.setText("Selected Node: " + str(self.combo.itemText(self.combo.currentIndex())))

        self.lbl4 = QLabel('Select logs: ', self)
        self.app_log = QCheckBox('app.log')
        self.credo_log = QCheckBox('credo.log')
        self.ibank_log = QCheckBox('ibank.log')
        self.iss_log = QCheckBox('iss.log')
        self.request_log = QCheckBox('request.log')
        self.server_log = QCheckBox('server.log')

        self.lbl5 = QLabel('Enter request number: ', self)
        self.request_number_edit = QLineEdit()
        self.lbl6 = QLabel('', self)    #result path
        self.lbl7 = QLabel('', self)    #result file name

        grid = QGridLayout()

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
        grid.addWidget(self.iss_log, 11, 0)
        grid.addWidget(self.server_log, 11, 1)

        grid.addWidget(self.lbl5, 12, 0)
        grid.addWidget(self.request_number_edit, 12, 1)

        grid.addWidget(self.send_logs, 13, 1)
        grid.addWidget(self.user_list_combo, 13, 0)
        grid.addWidget(self.lbl6, 14, 0)
        grid.addWidget(self.lbl7, 14, 1)

        self.back_check.setChecked(True)
        self.combo.activated[str].connect(self.combobox_node)
        self.user_list_combo.activated[str].connect(self.get_user_id)

        self.other_node_edit.setDisabled(True)
        self.app_log.setChecked(True)
        self.credo_log.setChecked(True)
        self.ibank_log.setChecked(True)
        self.iss_log.setChecked(True)
        self.request_log.setChecked(True)
        self.server_log.setChecked(True)

        self.send_logs.clicked.connect(lambda: self.push_btn_send_logs(self.request_number_edit.text()))

        self.setLayout(grid)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Log collector')
        self.show()


        self.request_number_edit.setFocus()
        self.app_log.stateChanged.connect(lambda: self.select_app_logs(self.app_log))
        self.ibank_log.stateChanged.connect(lambda: self.select_ibank_logs(self.ibank_log))
        self.ibank_log.stateChanged.connect(lambda: self.select_iss_logs(self.iss_log))
        self.credo_log.stateChanged.connect(lambda: self.select_credo_logs(self.credo_log))
        self.request_log.stateChanged.connect(lambda: self.select_request_logs(self.request_log))
        self.server_log.stateChanged.connect(lambda: self.select_server_logs(self.server_log))

    def get_user_id(self, names):
        user_id = [id for id, name in self.users_name.items() if str(name) == names]
        return user_id[0]

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

    def select_iss_logs(self, checkbox):
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
        with zipfile.ZipFile(LOG_ZIP_PATH + '\\' + name + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            try:
                for file in files:
                    prefix = file.split('\\')[-6] + '_' # credo or front
                    zip.write(file, prefix + file.split('\\')[-1])
            except:
                self.lbl7.setText("zip is empty!!!")
        self.ERROR = False
        user = str(self.user_list_combo.itemText(self.user_list_combo.currentIndex()))
        user_id = self.get_user_id(user)
        self.create_skype_chat(user_id, name + ".zip")
        return  self.lbl7.setText(name + ".zip is created")

    def push_btn_send_logs(self, number_request):
        self.files_to_zip = []
        self.BACK_SERVER_PATH = self.back_server_path.text()
        self.FRONT_SERVER_PATH = self.front_server_path.text()
        node_name = self.get_node_name()
        self.log_path = "\\nodes\\" + node_name + "\standalone\\log\\"
        self.back_log_path = self.BACK_SERVER_PATH + self.log_path
        self.front_log_path = self.FRONT_SERVER_PATH + self.log_path
        self.lbl6.setText('')

        if  (self.back_check.isChecked() == False) and  (self.front_check.isChecked() == False):
            self.lbl6.setText('No selected server!!!')
            self.BACK_ERROR = True
            self.FRONT_ERROR = True
        else:
            self.BACK_ERROR = False
            self.FRONT_ERROR = False

        if self.back_check.isChecked():
            if os.path.isdir(self.BACK_SERVER_PATH) == False:
                self.lbl6.setText('No exist back server dir')
                self.BACK_ERROR = True
            else:
                self.BACK_ERROR = False
        if self.front_check.isChecked():
            if os.path.isdir(self.FRONT_SERVER_PATH) == False:
                self.lbl6.setText('No exist front server dir')
                self.FRONT_ERROR = True
            else:
                self.FRONT_ERROR = False

        if not number_request:
            number_request = 'logs'

        if self.BACK_ERROR == False and self.FRONT_ERROR == False:
            if self.back_check.isChecked() == True:
                for file in logs_list:
                    self.files_to_zip += self.get_all_log_files(file, self.back_log_path)
            if self.front_check.isChecked() == True:
                for file in logs_list:
                    self.files_to_zip += self.get_all_log_files(file, self.front_log_path)

            self.create_zip(number_request, self.files_to_zip)
            self.lbl6.setText(LOG_ZIP_PATH + '\\')

    # def user_list(self):
    #     self.sk.contacts[self.sk.user.id].chat # для выполнения следующих задач. Без строки не работает
    #     groupe_user_list = self.sk.contacts.groups['ITWORKS'].userIds
    #     ITWORKS_GROUPE = {}
    #     for user in groupe_user_list:
    #         user_id = self.sk.contacts.user(user).id
    #         user_name = self.sk.contacts.user(user).name
    #         ITWORKS_GROUPE[user_id] = user_name
    #     return ITWORKS_GROUPE

    def user_list(self):
        self.sk.contacts[self.sk.user.id].chat # для выполнения следующих задач. Без строки не работает
        userId_list = self.sk.contacts
        SKYPE_USERS = {}
        for user in userId_list:
            if str(user.name):
                SKYPE_USERS[str(user.id)] = str(user.name)
        return SKYPE_USERS

    def create_skype_chat(self, user, file):
        chat = self.sk.contacts[user].chat
        chat.sendMsg('логи по заявке ' + file)
        chat.sendFile(open(LOG_ZIP_PATH + '\\' + file, "rb"), file)

    def get_all_log_files(self, log_name, log_path):
        logs_in_dir = []
        all_files_in_dir = os.listdir(log_path)
        logs = filter(lambda x: x.startswith(log_name), all_files_in_dir)
        for file in logs:
            logs_in_dir.append(log_path + file)
        return logs_in_dir


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())