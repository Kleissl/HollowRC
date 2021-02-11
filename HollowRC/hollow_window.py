# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hollow_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .Plots import MyGeometryView
from .Plots import MyResultView
from .TableInterface import MyTable

from  . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1031, 775)
        icon = QIcon()
        icon.addFile(u":/Icons/resources/Icon.png", QSize(), QIcon.Normal, QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.openAct = QAction(MainWindow)
        self.openAct.setObjectName(u"openAct")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/resources/Open_icon.png", QSize(), QIcon.Normal, QIcon.On)
        self.openAct.setIcon(icon1)
        self.saveAct = QAction(MainWindow)
        self.saveAct.setObjectName(u"saveAct")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/resources/Save_icon.png", QSize(), QIcon.Normal, QIcon.On)
        self.saveAct.setIcon(icon2)
        self.exitAct = QAction(MainWindow)
        self.exitAct.setObjectName(u"exitAct")
        icon3 = QIcon()
        icon3.addFile(u":/Icons/resources/Exit_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.exitAct.setIcon(icon3)
        self.analyseAct = QAction(MainWindow)
        self.analyseAct.setObjectName(u"analyseAct")
        icon4 = QIcon()
        icon4.addFile(u":/Icons/resources/Analyse_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.analyseAct.setIcon(icon4)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_about = QWidget()
        self.tab_about.setObjectName(u"tab_about")
        self.verticalLayout_11 = QVBoxLayout(self.tab_about)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_heading = QLabel(self.tab_about)
        self.label_heading.setObjectName(u"label_heading")
        self.label_heading.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_heading.setFont(font)
        self.label_heading.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_11.addWidget(self.label_heading)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_left_text = QLabel(self.tab_about)
        self.label_left_text.setObjectName(u"label_left_text")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_left_text.sizePolicy().hasHeightForWidth())
        self.label_left_text.setSizePolicy(sizePolicy)
        self.label_left_text.setMinimumSize(QSize(540, 485))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_left_text.setFont(font1)
        self.label_left_text.setAutoFillBackground(False)
        self.label_left_text.setMidLineWidth(4)
        self.label_left_text.setScaledContents(False)
        self.label_left_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_left_text.setWordWrap(True)
        self.label_left_text.setIndent(-1)

        self.verticalLayout_9.addWidget(self.label_left_text)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_5)

        self.label_version = QLabel(self.tab_about)
        self.label_version.setObjectName(u"label_version")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setItalic(True)
        self.label_version.setFont(font2)

        self.verticalLayout_9.addWidget(self.label_version)


        self.horizontalLayout_3.addLayout(self.verticalLayout_9)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_right_text = QLabel(self.tab_about)
        self.label_right_text.setObjectName(u"label_right_text")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_right_text.sizePolicy().hasHeightForWidth())
        self.label_right_text.setSizePolicy(sizePolicy1)
        self.label_right_text.setMinimumSize(QSize(325, 280))
        self.label_right_text.setFont(font1)
        self.label_right_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_right_text.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.label_right_text)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_8.addItem(self.verticalSpacer_6)

        self.label_24 = QLabel(self.tab_about)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setPixmap(QPixmap(u":/Figures/resources/coordinates_and_sign_convention.png"))

        self.verticalLayout_8.addWidget(self.label_24)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.label_author = QLabel(self.tab_about)
        self.label_author.setObjectName(u"label_author")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setItalic(False)
        self.label_author.setFont(font3)
        self.label_author.setLocale(QLocale(QLocale.English, QLocale.Denmark))
        self.label_author.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.label_author.setOpenExternalLinks(True)

        self.verticalLayout_8.addWidget(self.label_author)


        self.horizontalLayout_3.addLayout(self.verticalLayout_8)


        self.verticalLayout_11.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tab_about, "")
        self.tab_geometry = QWidget()
        self.tab_geometry.setObjectName(u"tab_geometry")
        self.gridLayout = QGridLayout(self.tab_geometry)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.tab_geometry)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.geometry_table = MyTable(self.tab_geometry)
        if (self.geometry_table.columnCount() < 5):
            self.geometry_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.geometry_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.geometry_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.geometry_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.geometry_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.geometry_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.geometry_table.rowCount() < 4):
            self.geometry_table.setRowCount(4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.geometry_table.setVerticalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.geometry_table.setVerticalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.geometry_table.setVerticalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.geometry_table.setVerticalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.geometry_table.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.geometry_table.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.geometry_table.setItem(0, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.geometry_table.setItem(0, 3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.geometry_table.setItem(0, 4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.geometry_table.setItem(1, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.geometry_table.setItem(1, 1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.geometry_table.setItem(1, 2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.geometry_table.setItem(1, 3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.geometry_table.setItem(1, 4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.geometry_table.setItem(2, 0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.geometry_table.setItem(2, 1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.geometry_table.setItem(2, 2, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.geometry_table.setItem(2, 3, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.geometry_table.setItem(2, 4, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.geometry_table.setItem(3, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.geometry_table.setItem(3, 1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.geometry_table.setItem(3, 2, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.geometry_table.setItem(3, 3, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.geometry_table.setItem(3, 4, __qtablewidgetitem28)
        self.geometry_table.setObjectName(u"geometry_table")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.geometry_table.sizePolicy().hasHeightForWidth())
        self.geometry_table.setSizePolicy(sizePolicy2)
        self.geometry_table.setLayoutDirection(Qt.LeftToRight)
        self.geometry_table.setInputMethodHints(Qt.ImhDigitsOnly)
        self.geometry_table.setFrameShape(QFrame.StyledPanel)
        self.geometry_table.setFrameShadow(QFrame.Sunken)
        self.geometry_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.geometry_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.geometry_table.setDragEnabled(True)
        self.geometry_table.setAlternatingRowColors(False)
        self.geometry_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.geometry_table.setGridStyle(Qt.SolidLine)
        self.geometry_table.setSortingEnabled(False)
        self.geometry_table.horizontalHeader().setVisible(False)
        self.geometry_table.horizontalHeader().setCascadingSectionResizes(True)
        self.geometry_table.horizontalHeader().setDefaultSectionSize(140)
        self.geometry_table.horizontalHeader().setProperty("showSortIndicator", False)
        self.geometry_table.horizontalHeader().setStretchLastSection(False)
        self.geometry_table.verticalHeader().setVisible(False)
        self.geometry_table.verticalHeader().setCascadingSectionResizes(True)
        self.geometry_table.verticalHeader().setProperty("showSortIndicator", False)
        self.geometry_table.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout_7.addWidget(self.geometry_table)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.addRowButton = QToolButton(self.tab_geometry)
        self.addRowButton.setObjectName(u"addRowButton")
        icon5 = QIcon()
        icon5.addFile(u":/Icons/resources/add_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.addRowButton.setIcon(icon5)

        self.verticalLayout_5.addWidget(self.addRowButton)

        self.removeRowButton = QToolButton(self.tab_geometry)
        self.removeRowButton.setObjectName(u"removeRowButton")
        icon6 = QIcon()
        icon6.addFile(u":/Icons/resources/minus_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeRowButton.setIcon(icon6)

        self.verticalLayout_5.addWidget(self.removeRowButton)

        self.moveUpRowButton = QToolButton(self.tab_geometry)
        self.moveUpRowButton.setObjectName(u"moveUpRowButton")
        icon7 = QIcon()
        icon7.addFile(u":/Icons/resources/up_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.moveUpRowButton.setIcon(icon7)

        self.verticalLayout_5.addWidget(self.moveUpRowButton)

        self.moveDownRowButton = QToolButton(self.tab_geometry)
        self.moveDownRowButton.setObjectName(u"moveDownRowButton")
        icon8 = QIcon()
        icon8.addFile(u":/Icons/resources/down_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.moveDownRowButton.setIcon(icon8)

        self.verticalLayout_5.addWidget(self.moveDownRowButton)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.line = QFrame(self.tab_geometry)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.graphicsViewGeometry = MyGeometryView(self.tab_geometry)
        self.graphicsViewGeometry.setObjectName(u"graphicsViewGeometry")
        self.graphicsViewGeometry.setFrameShape(QFrame.NoFrame)
        self.graphicsViewGeometry.setLineWidth(1)

        self.horizontalLayout_9.addWidget(self.graphicsViewGeometry)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.label_2 = QLabel(self.tab_geometry)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_geometry, "")
        self.tab_materials = QWidget()
        self.tab_materials.setObjectName(u"tab_materials")
        self.horizontalLayout = QHBoxLayout(self.tab_materials)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.InputGrid = QGridLayout()
        self.InputGrid.setObjectName(u"InputGrid")
        self.Material = QHBoxLayout()
        self.Material.setObjectName(u"Material")
        self.Input_verticalLayout = QVBoxLayout()
        self.Input_verticalLayout.setObjectName(u"Input_verticalLayout")
        self.label_3 = QLabel(self.tab_materials)
        self.label_3.setObjectName(u"label_3")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_3.setFont(font4)

        self.Input_verticalLayout.addWidget(self.label_3)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_17 = QLabel(self.tab_materials)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font1)

        self.gridLayout_3.addWidget(self.label_17, 0, 3, 1, 1)

        self.label_13 = QLabel(self.tab_materials)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_13, 1, 0, 1, 1)

        self.lineEdit_f_yk = QLineEdit(self.tab_materials)
        self.lineEdit_f_yk.setObjectName(u"lineEdit_f_yk")
        self.lineEdit_f_yk.setFont(font1)

        self.gridLayout_3.addWidget(self.lineEdit_f_yk, 2, 2, 1, 1)

        self.lineEdit_f_ck = QLineEdit(self.tab_materials)
        self.lineEdit_f_ck.setObjectName(u"lineEdit_f_ck")
        self.lineEdit_f_ck.setFont(font1)

        self.gridLayout_3.addWidget(self.lineEdit_f_ck, 0, 2, 1, 1)

        self.lineEdit_E_cm = QLineEdit(self.tab_materials)
        self.lineEdit_E_cm.setObjectName(u"lineEdit_E_cm")
        self.lineEdit_E_cm.setFont(font1)

        self.gridLayout_3.addWidget(self.lineEdit_E_cm, 1, 2, 1, 1)

        self.label_12 = QLabel(self.tab_materials)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)

        self.lineEdit_E_s = QLineEdit(self.tab_materials)
        self.lineEdit_E_s.setObjectName(u"lineEdit_E_s")
        self.lineEdit_E_s.setFont(font1)

        self.gridLayout_3.addWidget(self.lineEdit_E_s, 3, 2, 1, 1)

        self.label_14 = QLabel(self.tab_materials)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_15 = QLabel(self.tab_materials)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_15, 3, 0, 1, 1)

        self.label_19 = QLabel(self.tab_materials)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font1)

        self.gridLayout_3.addWidget(self.label_19, 1, 3, 1, 1)

        self.label_20 = QLabel(self.tab_materials)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)

        self.gridLayout_3.addWidget(self.label_20, 2, 3, 1, 1)

        self.label_21 = QLabel(self.tab_materials)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font1)

        self.gridLayout_3.addWidget(self.label_21, 3, 3, 1, 1)

        self.label_7 = QLabel(self.tab_materials)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.gridLayout_3.addWidget(self.label_7, 4, 3, 1, 1)

        self.lineEdit_alpha_cc = QLineEdit(self.tab_materials)
        self.lineEdit_alpha_cc.setObjectName(u"lineEdit_alpha_cc")
        self.lineEdit_alpha_cc.setFont(font1)

        self.gridLayout_3.addWidget(self.lineEdit_alpha_cc, 4, 2, 1, 1)

        self.label_6 = QLabel(self.tab_materials)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_6, 4, 0, 1, 1)

        self.label_23 = QLabel(self.tab_materials)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font1)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_23, 5, 0, 1, 1)

        self.comboBox_nu = QComboBox(self.tab_materials)
        self.comboBox_nu.addItem("")
        self.comboBox_nu.setObjectName(u"comboBox_nu")
        self.comboBox_nu.setFont(font1)

        self.gridLayout_3.addWidget(self.comboBox_nu, 5, 2, 1, 1)

        self.label_10 = QLabel(self.tab_materials)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.gridLayout_3.addWidget(self.label_10, 5, 3, 1, 1)


        self.Input_verticalLayout.addLayout(self.gridLayout_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Input_verticalLayout.addItem(self.verticalSpacer_4)


        self.Material.addLayout(self.Input_verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.Material.addItem(self.horizontalSpacer_2)


        self.InputGrid.addLayout(self.Material, 0, 0, 1, 1)

        self.Analysis = QHBoxLayout()
        self.Analysis.setObjectName(u"Analysis")
        self.Input_verticalLayout_2 = QVBoxLayout()
        self.Input_verticalLayout_2.setObjectName(u"Input_verticalLayout_2")
        self.label_4 = QLabel(self.tab_materials)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font4)

        self.Input_verticalLayout_2.addWidget(self.label_4)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.comboBox_concrete = QComboBox(self.tab_materials)
        self.comboBox_concrete.addItem("")
        self.comboBox_concrete.addItem("")
        self.comboBox_concrete.addItem("")
        self.comboBox_concrete.setObjectName(u"comboBox_concrete")
        self.comboBox_concrete.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.comboBox_concrete)

        self.label_11 = QLabel(self.tab_materials)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.comboBox_reinf = QComboBox(self.tab_materials)
        self.comboBox_reinf.addItem("")
        self.comboBox_reinf.setObjectName(u"comboBox_reinf")
        self.comboBox_reinf.setFont(font1)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.comboBox_reinf)

        self.label_22 = QLabel(self.tab_materials)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_22)


        self.Input_verticalLayout_2.addLayout(self.formLayout_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lineEdit_gamma_c = QLineEdit(self.tab_materials)
        self.lineEdit_gamma_c.setObjectName(u"lineEdit_gamma_c")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEdit_gamma_c.sizePolicy().hasHeightForWidth())
        self.lineEdit_gamma_c.setSizePolicy(sizePolicy3)
        self.lineEdit_gamma_c.setFont(font1)

        self.gridLayout_4.addWidget(self.lineEdit_gamma_c, 1, 1, 1, 1)

        self.lineEdit_gamma_s = QLineEdit(self.tab_materials)
        self.lineEdit_gamma_s.setObjectName(u"lineEdit_gamma_s")
        self.lineEdit_gamma_s.setFont(font1)

        self.gridLayout_4.addWidget(self.lineEdit_gamma_s, 3, 1, 1, 1)

        self.label_9 = QLabel(self.tab_materials)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(100, 0))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_8 = QLabel(self.tab_materials)
        self.label_8.setObjectName(u"label_8")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)
        self.label_8.setMinimumSize(QSize(100, 0))
        self.label_8.setBaseSize(QSize(0, 0))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_28 = QLabel(self.tab_materials)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font1)

        self.gridLayout_4.addWidget(self.label_28, 1, 2, 1, 1)

        self.label_35 = QLabel(self.tab_materials)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font1)

        self.gridLayout_4.addWidget(self.label_35, 3, 2, 1, 1)


        self.Input_verticalLayout_2.addLayout(self.gridLayout_4)

        self.checkBox_analSLS_1 = QCheckBox(self.tab_materials)
        self.checkBox_analSLS_1.setObjectName(u"checkBox_analSLS_1")
        self.checkBox_analSLS_1.setFont(font1)
        self.checkBox_analSLS_1.setChecked(True)
        self.checkBox_analSLS_1.setTristate(False)

        self.Input_verticalLayout_2.addWidget(self.checkBox_analSLS_1)

        self.checkBox_analULS_1 = QCheckBox(self.tab_materials)
        self.checkBox_analULS_1.setObjectName(u"checkBox_analULS_1")
        self.checkBox_analULS_1.setFont(font1)
        self.checkBox_analULS_1.setChecked(False)

        self.Input_verticalLayout_2.addWidget(self.checkBox_analULS_1)

        self.checkBox_analULS_2 = QCheckBox(self.tab_materials)
        self.checkBox_analULS_2.setObjectName(u"checkBox_analULS_2")
        font5 = QFont()
        font5.setPointSize(9)
        font5.setStrikeOut(True)
        self.checkBox_analULS_2.setFont(font5)
        self.checkBox_analULS_2.setCheckable(False)

        self.Input_verticalLayout_2.addWidget(self.checkBox_analULS_2)

        self.checkBox_analSLS_2 = QCheckBox(self.tab_materials)
        self.checkBox_analSLS_2.setObjectName(u"checkBox_analSLS_2")
        self.checkBox_analSLS_2.setFont(font5)
        self.checkBox_analSLS_2.setCheckable(False)

        self.Input_verticalLayout_2.addWidget(self.checkBox_analSLS_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Input_verticalLayout_2.addItem(self.verticalSpacer)


        self.Analysis.addLayout(self.Input_verticalLayout_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.Analysis.addItem(self.horizontalSpacer_3)


        self.InputGrid.addLayout(self.Analysis, 1, 0, 1, 1)


        self.horizontalLayout.addLayout(self.InputGrid)

        self.PlotLayout = QVBoxLayout()
        self.PlotLayout.setObjectName(u"PlotLayout")
        self.graphicsViewConcrete = QGraphicsView(self.tab_materials)
        self.graphicsViewConcrete.setObjectName(u"graphicsViewConcrete")

        self.PlotLayout.addWidget(self.graphicsViewConcrete)

        self.graphicsViewReinforcement = QGraphicsView(self.tab_materials)
        self.graphicsViewReinforcement.setObjectName(u"graphicsViewReinforcement")

        self.PlotLayout.addWidget(self.graphicsViewReinforcement)


        self.horizontalLayout.addLayout(self.PlotLayout)

        self.tabWidget.addTab(self.tab_materials, "")
        self.tab_loading = QWidget()
        self.tab_loading.setObjectName(u"tab_loading")
        self.verticalLayout_7 = QVBoxLayout(self.tab_loading)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.SectionForces_tableWidget = MyTable(self.tab_loading)
        if (self.SectionForces_tableWidget.columnCount() < 8):
            self.SectionForces_tableWidget.setColumnCount(8)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.SectionForces_tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem36)
        if (self.SectionForces_tableWidget.rowCount() < 1):
            self.SectionForces_tableWidget.setRowCount(1)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.SectionForces_tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.SectionForces_tableWidget.setItem(0, 0, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.SectionForces_tableWidget.setItem(0, 1, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.SectionForces_tableWidget.setItem(0, 2, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.SectionForces_tableWidget.setItem(0, 3, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.SectionForces_tableWidget.setItem(0, 4, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.SectionForces_tableWidget.setItem(0, 5, __qtablewidgetitem43)
        self.SectionForces_tableWidget.setObjectName(u"SectionForces_tableWidget")
        sizePolicy3.setHeightForWidth(self.SectionForces_tableWidget.sizePolicy().hasHeightForWidth())
        self.SectionForces_tableWidget.setSizePolicy(sizePolicy3)
        self.SectionForces_tableWidget.setMinimumSize(QSize(500, 0))
        self.SectionForces_tableWidget.setMaximumSize(QSize(745, 56))
        font6 = QFont()
        font6.setPointSize(10)
        self.SectionForces_tableWidget.setFont(font6)
        self.SectionForces_tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SectionForces_tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.SectionForces_tableWidget.horizontalHeader().setDefaultSectionSize(90)

        self.horizontalLayout_2.addWidget(self.SectionForces_tableWidget)

        self.horizontalSpacer_7 = QSpacerItem(5, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalSpacer_8 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_8)

        self.label_5 = QLabel(self.tab_loading)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_5)

        self.lineEdit_wallNodeN = QLineEdit(self.tab_loading)
        self.lineEdit_wallNodeN.setObjectName(u"lineEdit_wallNodeN")
        sizePolicy2.setHeightForWidth(self.lineEdit_wallNodeN.sizePolicy().hasHeightForWidth())
        self.lineEdit_wallNodeN.setSizePolicy(sizePolicy2)
        self.lineEdit_wallNodeN.setMaximumSize(QSize(80, 16777215))
        self.lineEdit_wallNodeN.setFont(font1)

        self.verticalLayout_3.addWidget(self.lineEdit_wallNodeN)

        self.verticalSpacer_7 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_7)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_4 = QSpacerItem(5, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.load_fac_label = QLabel(self.tab_loading)
        self.load_fac_label.setObjectName(u"load_fac_label")
        self.load_fac_label.setFont(font1)

        self.verticalLayout_6.addWidget(self.load_fac_label)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.graphicsViewResults = MyResultView(self.tab_loading)
        self.graphicsViewResults.setObjectName(u"graphicsViewResults")
        self.graphicsViewResults.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_4.addWidget(self.graphicsViewResults)

        self.vLayout_view_filter = QVBoxLayout()
        self.vLayout_view_filter.setObjectName(u"vLayout_view_filter")
        self.label_25 = QLabel(self.tab_loading)
        self.label_25.setObjectName(u"label_25")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy5)

        self.vLayout_view_filter.addWidget(self.label_25)

        self.checkBox_plot1 = QCheckBox(self.tab_loading)
        self.checkBox_plot1.setObjectName(u"checkBox_plot1")
        self.checkBox_plot1.setChecked(False)

        self.vLayout_view_filter.addWidget(self.checkBox_plot1)

        self.checkBox_plot2 = QCheckBox(self.tab_loading)
        self.checkBox_plot2.setObjectName(u"checkBox_plot2")
        self.checkBox_plot2.setChecked(False)

        self.vLayout_view_filter.addWidget(self.checkBox_plot2)

        self.checkBox_plot3 = QCheckBox(self.tab_loading)
        self.checkBox_plot3.setObjectName(u"checkBox_plot3")
        self.checkBox_plot3.setChecked(False)

        self.vLayout_view_filter.addWidget(self.checkBox_plot3)

        self.checkBox_plot4 = QCheckBox(self.tab_loading)
        self.checkBox_plot4.setObjectName(u"checkBox_plot4")
        self.checkBox_plot4.setChecked(False)

        self.vLayout_view_filter.addWidget(self.checkBox_plot4)

        self.checkBox_plot5 = QCheckBox(self.tab_loading)
        self.checkBox_plot5.setObjectName(u"checkBox_plot5")
        self.checkBox_plot5.setChecked(False)

        self.vLayout_view_filter.addWidget(self.checkBox_plot5)

        self.checkBox_plot6 = QCheckBox(self.tab_loading)
        self.checkBox_plot6.setObjectName(u"checkBox_plot6")

        self.vLayout_view_filter.addWidget(self.checkBox_plot6)

        self.checkBox_plot7 = QCheckBox(self.tab_loading)
        self.checkBox_plot7.setObjectName(u"checkBox_plot7")

        self.vLayout_view_filter.addWidget(self.checkBox_plot7)

        self.checkBox_plot8 = QCheckBox(self.tab_loading)
        self.checkBox_plot8.setObjectName(u"checkBox_plot8")

        self.vLayout_view_filter.addWidget(self.checkBox_plot8)

        self.checkBox_plot9 = QCheckBox(self.tab_loading)
        self.checkBox_plot9.setObjectName(u"checkBox_plot9")

        self.vLayout_view_filter.addWidget(self.checkBox_plot9)

        self.checkBox_plot10 = QCheckBox(self.tab_loading)
        self.checkBox_plot10.setObjectName(u"checkBox_plot10")

        self.vLayout_view_filter.addWidget(self.checkBox_plot10)


        self.horizontalLayout_4.addLayout(self.vLayout_view_filter)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.label_16 = QLabel(self.tab_loading)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font2)

        self.verticalLayout_6.addWidget(self.label_16)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.tabWidget.addTab(self.tab_loading, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1031, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.openAct)
        self.menuFile.addAction(self.saveAct)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAct)
        self.toolBar.addAction(self.openAct)
        self.toolBar.addAction(self.saveAct)
        self.toolBar.addAction(self.exitAct)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.analyseAct)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hollow section analysis tool", None))
        self.openAct.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.openAct.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.saveAct.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.saveAct.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.exitAct.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(tooltip)
        self.exitAct.setToolTip(QCoreApplication.translate("MainWindow", u"Exit application", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.exitAct.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.analyseAct.setText(QCoreApplication.translate("MainWindow", u"Analyse", None))
#if QT_CONFIG(shortcut)
        self.analyseAct.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.label_heading.setText(QCoreApplication.translate("MainWindow", u"General Design of Hollow RC Sections under Combined Actions", None))
        self.label_left_text.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">About</span></p><p><span style=\" font-size:8pt;\">This is an easy to use design tool for analysis of hollow reinforced concrete sections under combined loading, fully embracing the interactions between bending and shear behaviour.<br/>To propor describe the interaction between the flow of normal stesses and shear stress and to fully utilize the capacity of the cross-section one must leave the simplfied approach of the diagonal truss model.<br/>For a linear-elastic material one could apply the Grashof's formula, similar to analysis of thin-walled steel-sections, to determining shear flow etc. <br/>However, with the basic assumption of linear-elastic material behaviour being unsuitable for reinforced concrete, a more numerical extensive approach involving a series of optimization routines needs to be adopted.<br/>To make this analysis method more approachable, this easy to use application has been developed.</span></p><p><span style=\" font-size:8pt;\">Thi"
                        "s design tool will provide designers with a superior insight into the actual stress state during Service Limit State (SLS), including the shear or torsion induced stresses in the transverse reinforcement (in the circumferential direction), and will completely avoid any superposition of plastic lower bound methods from the diagonal truss model, additional shear-induced demand for longitudinal reinforcement and the corresponding strain incompatibilities introduced by separating shear and bending analysis.<br/>For SLS the actual shear flow is determined based on a plane dual-section analysis, which just means that two nabouring plane-sections are analysed and from their differences in normal flow, simple equilibrium yields the corresponding shear flow distribution.<br/>So only by applying the fundamental flexural member assumption of plane sections must remain plane combined with basic equilibrium equations can the actual normal and shear flow distributions be determined.<br/>From this an in-plane membrane analys"
                        "is is used to determined the reinforcement stresses etc. by choosing the resulting compressive stress direction / strut angle such that it minimizes the complementary strain energy (similar to fulfilling compatibility).</span></p><p><span style=\" font-size:8pt;\">For Ultimate Limit State (ULS) this design tool will allow designers to push the capacity of the cross-section even further, as it by use of mathematical optimization algorithms are able to identify the true optimal plastic lower-bound solution that fully utilize the strength of the materials.<br/>For ULS a classic plane section analysis is performed and from its normal flow distribution, an in-plane membrane analysis considering the yield conditions determines the leftover shear flow capacity at any given point along the cross-section, which then is integrated into a shear force capacity for each of the cross-sectional wall elements. Finally this is followed up by solving the optimization problem of maximizing the load-factor while maintaining equal"
                        "ibrium between the wall shear forces and the user specified global sectional forces.</span></p><p><span style=\" font-weight:600;\">Assumptions and limitations:</span></p><p><span style=\" font-size:8pt;\">- The span to depth ratio of the section is sufficient for beam theory to be applicable where plane section analysis approach is considered.<br/>- The walls are sufficient thin, compared to the cross-section dimensions, for a thin-walled approach to be applicable.<br/>- Normal stresses in the circumferential direction are neglected even though equilibrium in principle requires the presence of these. This is a very common approach when analysing thin-walled sections..</span></p></body></html>", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0", None))
        self.label_right_text.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Sign convention</span></p><p><span style=\" font-size:8pt;\">The sign convention generally follows a right hand system (RHS). See illustration in figure below.</span></p><p><span style=\" font-size:8pt; text-decoration: underline;\">Geometry</span><span style=\" font-size:8pt;\"><br/>- All dimensions are in millimeters<br/>- The section walls must be defined in the clock-wise direction<br/>- Angles are taken positive in the counter-clockwise direction starting from the y-axis<br/>- Reinforcement ratios are defined as the steel-to-concrete ratio (e.g. 0.01 = 1%)</span></p><p><span style=\" font-size:8pt; text-decoration: underline;\">Flows &amp; Stresses</span><span style=\" font-size:8pt;\"><br/>- Normal flow and normal stress are positive for tension<br/>- Shear flow is positive in the counter-clockwise direction</span></p><p><span style=\" font-size:8pt; text-decoration: underline;\">Section forces</span><span style=\" font-size:8pt;\"><br/>- Positive M"
                        "y moment yields compression in the top<br/>- Positive Mz moment yields compression on the right side<br/>- Negative N (normal force) yields compression<br/>- Positive Vy yields shear in the y-direction (right)<br/>- Positive Vz yields shear in the z-direction (upward)<br/>- Positive T (torsion) yields counter-clockwise shear flow</span></p></body></html>", None))
        self.label_24.setText("")
        self.label_author.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">by Kenneth C. Kleissl<br/><a href=\"https://github.com/Kleissl/HollowRC\"><span style=\" text-decoration: underline; color:#0000ff;\">www.github.com/Kleissl/HollowRC</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), QCoreApplication.translate("MainWindow", u"About", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Define starting coordinates and properties of each wall element here:</p></body></html>", None))
        ___qtablewidgetitem = self.geometry_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Y-coordinate [mm]", None));
        ___qtablewidgetitem1 = self.geometry_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Z-coordinate [mm]", None));
        ___qtablewidgetitem2 = self.geometry_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Wall thickness [mm]", None));
        ___qtablewidgetitem3 = self.geometry_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Reinf. ratio long. [-]", None));
        ___qtablewidgetitem4 = self.geometry_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Reinf. ratio trans. [-]", None));
        ___qtablewidgetitem5 = self.geometry_table.verticalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Node no. 1", None));
        ___qtablewidgetitem6 = self.geometry_table.verticalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Node no. 2", None));
        ___qtablewidgetitem7 = self.geometry_table.verticalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Node no. 3", None));
        ___qtablewidgetitem8 = self.geometry_table.verticalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Node no. 4", None));

        __sortingEnabled = self.geometry_table.isSortingEnabled()
        self.geometry_table.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.geometry_table.item(0, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem10 = self.geometry_table.item(0, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"2000", None));
        ___qtablewidgetitem11 = self.geometry_table.item(0, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"300", None));
        ___qtablewidgetitem12 = self.geometry_table.item(0, 3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem12.setToolTip(QCoreApplication.translate("MainWindow", u"3000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem13 = self.geometry_table.item(0, 4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem13.setToolTip(QCoreApplication.translate("MainWindow", u"3000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem14 = self.geometry_table.item(1, 0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"1500", None));
        ___qtablewidgetitem15 = self.geometry_table.item(1, 1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"2000", None));
        ___qtablewidgetitem16 = self.geometry_table.item(1, 2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"200", None));
        ___qtablewidgetitem17 = self.geometry_table.item(1, 3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem17.setToolTip(QCoreApplication.translate("MainWindow", u"2000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem18 = self.geometry_table.item(1, 4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem18.setToolTip(QCoreApplication.translate("MainWindow", u"2000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem19 = self.geometry_table.item(2, 0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"1500", None));
        ___qtablewidgetitem20 = self.geometry_table.item(2, 1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem21 = self.geometry_table.item(2, 2)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"300", None));
        ___qtablewidgetitem22 = self.geometry_table.item(2, 3)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem22.setToolTip(QCoreApplication.translate("MainWindow", u"3000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem23 = self.geometry_table.item(2, 4)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
        ___qtablewidgetitem24 = self.geometry_table.item(3, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem25 = self.geometry_table.item(3, 1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem26 = self.geometry_table.item(3, 2)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"200", None));
        ___qtablewidgetitem27 = self.geometry_table.item(3, 3)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem27.setToolTip(QCoreApplication.translate("MainWindow", u"2000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem28 = self.geometry_table.item(3, 4)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"0.01", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem28.setToolTip(QCoreApplication.translate("MainWindow", u"2000 mm2/m", None));
#endif // QT_CONFIG(tooltip)
        self.geometry_table.setSortingEnabled(__sortingEnabled)

#if QT_CONFIG(tooltip)
        self.addRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Insert new row at the bottom", None))
#endif // QT_CONFIG(tooltip)
        self.addRowButton.setText(QCoreApplication.translate("MainWindow", u"add", None))
#if QT_CONFIG(tooltip)
        self.removeRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected row", None))
#endif // QT_CONFIG(tooltip)
        self.removeRowButton.setText(QCoreApplication.translate("MainWindow", u"remove", None))
#if QT_CONFIG(tooltip)
        self.moveUpRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Move selected row up", None))
#endif // QT_CONFIG(tooltip)
        self.moveUpRowButton.setText(QCoreApplication.translate("MainWindow", u"move up", None))
#if QT_CONFIG(tooltip)
        self.moveDownRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Move selected row down", None))
#endif // QT_CONFIG(tooltip)
        self.moveDownRowButton.setText(QCoreApplication.translate("MainWindow", u"move down", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cross-section nodes can be moved by click & drag", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_geometry), QCoreApplication.translate("MainWindow", u"Geometry", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Material properties:", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"MPa", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">cm</span> = </p></body></html>", None))
        self.lineEdit_f_yk.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.lineEdit_f_ck.setText(QCoreApplication.translate("MainWindow", u"45", None))
        self.lineEdit_E_cm.setText(QCoreApplication.translate("MainWindow", u"35", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>f<span style=\" vertical-align:sub;\">ck</span> = </p></body></html>", None))
        self.lineEdit_E_s.setText(QCoreApplication.translate("MainWindow", u"210", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>f<span style=\" vertical-align:sub;\">yk</span> = </p></body></html>", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">s</span> = </p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"MPa", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"GPa", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lineEdit_alpha_cc.setText(QCoreApplication.translate("MainWindow", u"0.85", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-family:'Symbol'; font-size:large;\">a</span><span style=\" vertical-align:sub;\">cc</span> = </p></body></html>", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-family:'Symbol'; font-size:large;\">n</span><span style=\" vertical-align:sub;\"></span> = </p></body></html>", None))
        self.comboBox_nu.setItemText(0, QCoreApplication.translate("MainWindow", u"0.6 ( 1 - f_ck / 250 )", None))

        self.label_10.setText(QCoreApplication.translate("MainWindow", u"comp. strength eff. factor", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Analysis:", None))
        self.comboBox_concrete.setItemText(0, QCoreApplication.translate("MainWindow", u"EN Parabolic-rectangular", None))
        self.comboBox_concrete.setItemText(1, QCoreApplication.translate("MainWindow", u"EN Bi-linear", None))
        self.comboBox_concrete.setItemText(2, QCoreApplication.translate("MainWindow", u"EN Nonlinear", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Reinforcement", None))
        self.comboBox_reinf.setItemText(0, QCoreApplication.translate("MainWindow", u"Elastic-plastic", None))

        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Concrete", None))
        self.lineEdit_gamma_c.setText(QCoreApplication.translate("MainWindow", u"1.5", None))
        self.lineEdit_gamma_s.setText(QCoreApplication.translate("MainWindow", u"1.15", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-family:'Symbol'; font-size:large;\">g</span><span style=\" vertical-align:sub;\">s</span> = </p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-family:'Symbol'; font-size:large;\">g</span><span style=\" vertical-align:sub;\">c</span> = </p></body></html>", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"-       ", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"-       ", None))
#if QT_CONFIG(statustip)
        self.checkBox_analSLS_1.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.checkBox_analSLS_1.setText(QCoreApplication.translate("MainWindow", u"Plane dual-section && sigma-tau equilibrium (SLS)", None))
        self.checkBox_analULS_1.setText(QCoreApplication.translate("MainWindow", u"Plane section && optimizing tau (ULS)", None))
        self.checkBox_analULS_2.setText(QCoreApplication.translate("MainWindow", u"Optimizing sigma && tau (extreme ULS)", None))
        self.checkBox_analSLS_2.setText(QCoreApplication.translate("MainWindow", u"Minimizing comp. elastic energy for sigma && tau (extreme SLS)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_materials), QCoreApplication.translate("MainWindow", u"Materials && Analysis", None))
        ___qtablewidgetitem29 = self.SectionForces_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"N [kN]", None));
        ___qtablewidgetitem30 = self.SectionForces_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"My [kNm]", None));
        ___qtablewidgetitem31 = self.SectionForces_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"Mz [kNm]", None));
        ___qtablewidgetitem32 = self.SectionForces_tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"Vy [kN]", None));
        ___qtablewidgetitem33 = self.SectionForces_tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"Vz [kN]", None));
        ___qtablewidgetitem34 = self.SectionForces_tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"T [kNm]", None));
        ___qtablewidgetitem35 = self.SectionForces_tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"UR_bendig", None));
        ___qtablewidgetitem36 = self.SectionForces_tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"UR_shear", None));
        ___qtablewidgetitem37 = self.SectionForces_tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"LC", None));

        __sortingEnabled1 = self.SectionForces_tableWidget.isSortingEnabled()
        self.SectionForces_tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem38 = self.SectionForces_tableWidget.item(0, 0)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"-17000", None));
        ___qtablewidgetitem39 = self.SectionForces_tableWidget.item(0, 1)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"21000", None));
        ___qtablewidgetitem40 = self.SectionForces_tableWidget.item(0, 2)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem41 = self.SectionForces_tableWidget.item(0, 3)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem42 = self.SectionForces_tableWidget.item(0, 4)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"2000", None));
        ___qtablewidgetitem43 = self.SectionForces_tableWidget.item(0, 5)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"0", None));
        self.SectionForces_tableWidget.setSortingEnabled(__sortingEnabled1)

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"No. of points pr. wall element:", None))
        self.lineEdit_wallNodeN.setText(QCoreApplication.translate("MainWindow", u"25", None))
        self.load_fac_label.setText(QCoreApplication.translate("MainWindow", u"No load-factor currently applied", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">View filter</span></p></body></html>", None))
        self.checkBox_plot1.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot2.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot3.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot4.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot5.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot6.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot7.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot8.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot9.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.checkBox_plot10.setText(QCoreApplication.translate("MainWindow", u"no plot data available", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Positive value drawn on the outside of the section. Click to read values in statusbar.", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_loading), QCoreApplication.translate("MainWindow", u"Loading && Results", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

