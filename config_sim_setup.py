# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_sim.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_config_sim(object):
    def setupUi(self, dialog_config_sim):
        dialog_config_sim.setObjectName("dialog_config_sim")
        dialog_config_sim.resize(600, 275)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        dialog_config_sim.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(dialog_config_sim)
        self.gridLayout.setObjectName("gridLayout")
        self.vert_layout_config_sim = QtWidgets.QVBoxLayout()
        self.vert_layout_config_sim.setObjectName("vert_layout_config_sim")
        self.lbl_config_sim = QtWidgets.QLabel(dialog_config_sim)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setKerning(True)
        self.lbl_config_sim.setFont(font)
        self.lbl_config_sim.setObjectName("lbl_config_sim")
        self.vert_layout_config_sim.addWidget(self.lbl_config_sim)
        self.hori_line_config_sim = QtWidgets.QFrame(dialog_config_sim)
        self.hori_line_config_sim.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_config_sim.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_config_sim.setObjectName("hori_line_config_sim")
        self.vert_layout_config_sim.addWidget(self.hori_line_config_sim)
        self.grid_layout_config_sim = QtWidgets.QGridLayout()
        self.grid_layout_config_sim.setObjectName("grid_layout_config_sim")
        self.lbl_num_people = QtWidgets.QLabel(dialog_config_sim)
        self.lbl_num_people.setObjectName("lbl_num_people")
        self.grid_layout_config_sim.addWidget(self.lbl_num_people, 2, 0, 1, 1)
        self.lbl_num_floors = QtWidgets.QLabel(dialog_config_sim)
        self.lbl_num_floors.setObjectName("lbl_num_floors")
        self.grid_layout_config_sim.addWidget(self.lbl_num_floors, 1, 0, 1, 1)
        self.lbl_lift_capacity = QtWidgets.QLabel(dialog_config_sim)
        self.lbl_lift_capacity.setObjectName("lbl_lift_capacity")
        self.grid_layout_config_sim.addWidget(self.lbl_lift_capacity, 3, 0, 1, 1)
        self.lbl_ui_delay = QtWidgets.QLabel(dialog_config_sim)
        self.lbl_ui_delay.setObjectName("lbl_ui_delay")
        self.grid_layout_config_sim.addWidget(self.lbl_ui_delay, 4, 0, 1, 1)
        self.line_edit_num_floors = QtWidgets.QLineEdit(dialog_config_sim)
        self.line_edit_num_floors.setObjectName("line_edit_num_floors")
        self.grid_layout_config_sim.addWidget(self.line_edit_num_floors, 1, 2, 1, 1)
        self.line_edit_num_people = QtWidgets.QLineEdit(dialog_config_sim)
        self.line_edit_num_people.setObjectName("line_edit_num_people")
        self.grid_layout_config_sim.addWidget(self.line_edit_num_people, 2, 2, 1, 1)
        self.line_edit_lift_capacity = QtWidgets.QLineEdit(dialog_config_sim)
        self.line_edit_lift_capacity.setObjectName("line_edit_lift_capacity")
        self.grid_layout_config_sim.addWidget(self.line_edit_lift_capacity, 3, 2, 1, 1)
        self.line_edit_ui_delay = QtWidgets.QLineEdit(dialog_config_sim)
        self.line_edit_ui_delay.setObjectName("line_edit_ui_delay")
        self.grid_layout_config_sim.addWidget(self.line_edit_ui_delay, 4, 2, 1, 1)
        self.vert_layout_config_sim.addLayout(self.grid_layout_config_sim)
        self.btn_save_sim = QtWidgets.QPushButton(dialog_config_sim)
        self.btn_save_sim.setObjectName("btn_save_sim")
        self.vert_layout_config_sim.addWidget(self.btn_save_sim, 0, QtCore.Qt.AlignLeft)
        self.hori_line_save_sim = QtWidgets.QFrame(dialog_config_sim)
        self.hori_line_save_sim.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_save_sim.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_save_sim.setObjectName("hori_line_save_sim")
        self.vert_layout_config_sim.addWidget(self.hori_line_save_sim)
        self.lbl_save_successful = QtWidgets.QLabel(dialog_config_sim)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lbl_save_successful.setFont(font)
        self.lbl_save_successful.setText("")
        self.lbl_save_successful.setObjectName("lbl_save_successful")
        self.vert_layout_config_sim.addWidget(self.lbl_save_successful)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vert_layout_config_sim.addItem(spacerItem)
        self.gridLayout.addLayout(self.vert_layout_config_sim, 0, 0, 1, 1)

        self.retranslateUi(dialog_config_sim)
        QtCore.QMetaObject.connectSlotsByName(dialog_config_sim)

    def retranslateUi(self, dialog_config_sim):
        _translate = QtCore.QCoreApplication.translate
        dialog_config_sim.setWindowTitle(_translate("dialog_config_sim", "Configure Simulation - Lift Control"))
        self.lbl_config_sim.setText(_translate("dialog_config_sim", "Configure Simulation"))
        self.lbl_num_people.setText(_translate("dialog_config_sim", "Number of People:"))
        self.lbl_num_floors.setText(_translate("dialog_config_sim", "Number of Floors:"))
        self.lbl_lift_capacity.setText(_translate("dialog_config_sim", "Lift Capacity:"))
        self.lbl_ui_delay.setText(_translate("dialog_config_sim", "UI Delay (Milliseconds):"))
        self.btn_save_sim.setText(_translate("dialog_config_sim", "Save Simulation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_config_sim = QtWidgets.QDialog()
    ui = Ui_dialog_config_sim()
    ui.setupUi(dialog_config_sim)
    dialog_config_sim.show()
    sys.exit(app.exec_())
