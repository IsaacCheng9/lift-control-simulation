# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_sim.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_new_sim(object):
    def setupUi(self, dialog_new_sim):
        dialog_new_sim.setObjectName("dialog_new_sim")
        dialog_new_sim.resize(600, 275)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        dialog_new_sim.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(dialog_new_sim)
        self.gridLayout.setObjectName("gridLayout")
        self.vert_layout_new_sim = QtWidgets.QVBoxLayout()
        self.vert_layout_new_sim.setObjectName("vert_layout_new_sim")
        self.lbl_new_sim = QtWidgets.QLabel(dialog_new_sim)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setKerning(True)
        self.lbl_new_sim.setFont(font)
        self.lbl_new_sim.setObjectName("lbl_new_sim")
        self.vert_layout_new_sim.addWidget(self.lbl_new_sim)
        self.hori_line_create_sim = QtWidgets.QFrame(dialog_new_sim)
        self.hori_line_create_sim.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_create_sim.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_create_sim.setObjectName("hori_line_create_sim")
        self.vert_layout_new_sim.addWidget(self.hori_line_create_sim)
        self.grid_layout_create_sim = QtWidgets.QGridLayout()
        self.grid_layout_create_sim.setObjectName("grid_layout_create_sim")
        self.lbl_ui_speed = QtWidgets.QLabel(dialog_new_sim)
        self.lbl_ui_speed.setObjectName("lbl_ui_speed")
        self.grid_layout_create_sim.addWidget(self.lbl_ui_speed, 4, 0, 1, 1)
        self.line_edit_num_people = QtWidgets.QLineEdit(dialog_new_sim)
        self.line_edit_num_people.setMaxLength(40)
        self.line_edit_num_people.setObjectName("line_edit_num_people")
        self.grid_layout_create_sim.addWidget(self.line_edit_num_people, 2, 1, 1, 1)
        self.lbl_lift_capacity = QtWidgets.QLabel(dialog_new_sim)
        self.lbl_lift_capacity.setObjectName("lbl_lift_capacity")
        self.grid_layout_create_sim.addWidget(self.lbl_lift_capacity, 3, 0, 1, 1)
        self.line_edit_num_floors = QtWidgets.QLineEdit(dialog_new_sim)
        self.line_edit_num_floors.setMaxLength(13)
        self.line_edit_num_floors.setObjectName("line_edit_num_floors")
        self.grid_layout_create_sim.addWidget(self.line_edit_num_floors, 1, 1, 1, 1)
        self.lbl_num_people = QtWidgets.QLabel(dialog_new_sim)
        self.lbl_num_people.setObjectName("lbl_num_people")
        self.grid_layout_create_sim.addWidget(self.lbl_num_people, 2, 0, 1, 1)
        self.lbl_num_floors = QtWidgets.QLabel(dialog_new_sim)
        self.lbl_num_floors.setObjectName("lbl_num_floors")
        self.grid_layout_create_sim.addWidget(self.lbl_num_floors, 1, 0, 1, 1)
        self.line_edit_lift_capacity = QtWidgets.QLineEdit(dialog_new_sim)
        self.line_edit_lift_capacity.setMaxLength(40)
        self.line_edit_lift_capacity.setObjectName("line_edit_lift_capacity")
        self.grid_layout_create_sim.addWidget(self.line_edit_lift_capacity, 3, 1, 1, 1)
        self.line_edit_ui_speed = QtWidgets.QLineEdit(dialog_new_sim)
        self.line_edit_ui_speed.setMaxLength(40)
        self.line_edit_ui_speed.setObjectName("line_edit_ui_speed")
        self.grid_layout_create_sim.addWidget(self.line_edit_ui_speed, 4, 1, 1, 1)
        self.vert_layout_new_sim.addLayout(self.grid_layout_create_sim)
        self.btn_new_sim = QtWidgets.QPushButton(dialog_new_sim)
        self.btn_new_sim.setObjectName("btn_new_sim")
        self.vert_layout_new_sim.addWidget(self.btn_new_sim, 0, QtCore.Qt.AlignLeft)
        self.hori_line_new_sim = QtWidgets.QFrame(dialog_new_sim)
        self.hori_line_new_sim.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_new_sim.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_new_sim.setObjectName("hori_line_new_sim")
        self.vert_layout_new_sim.addWidget(self.hori_line_new_sim)
        self.lbl_start_successful = QtWidgets.QLabel(dialog_new_sim)
        self.lbl_start_successful.setText("")
        self.lbl_start_successful.setObjectName("lbl_start_successful")
        self.vert_layout_new_sim.addWidget(self.lbl_start_successful)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vert_layout_new_sim.addItem(spacerItem)
        self.gridLayout.addLayout(self.vert_layout_new_sim, 0, 0, 1, 1)

        self.retranslateUi(dialog_new_sim)
        QtCore.QMetaObject.connectSlotsByName(dialog_new_sim)

    def retranslateUi(self, dialog_new_sim):
        _translate = QtCore.QCoreApplication.translate
        dialog_new_sim.setWindowTitle(_translate("dialog_new_sim", "New Simulation - Lift Control"))
        self.lbl_new_sim.setText(_translate("dialog_new_sim", "New Simulation"))
        self.lbl_ui_speed.setText(_translate("dialog_new_sim", "UI Speed (Delay in Seconds):"))
        self.lbl_lift_capacity.setText(_translate("dialog_new_sim", "Lift Capacity:"))
        self.lbl_num_people.setText(_translate("dialog_new_sim", "Number of People:"))
        self.lbl_num_floors.setText(_translate("dialog_new_sim", "Number of Floors:"))
        self.btn_new_sim.setText(_translate("dialog_new_sim", "Start New Simulation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_new_sim = QtWidgets.QDialog()
    ui = Ui_dialog_new_sim()
    ui.setupUi(dialog_new_sim)
    dialog_new_sim.show()
    sys.exit(app.exec_())
