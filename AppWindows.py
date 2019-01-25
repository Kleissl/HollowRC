# -*- coding: utf-8 -*-
"""
This module containes all the application window classes for the "Hollow section analysis tool" GUI

History log:
Version 0.1 - first working build based on UI from Qt Designer
Version 0.2 - moved MainWindow class into separate file
Version 0.3 - Now compatible with Python3 & PyQt5

Author: Kenneth C. Kleissl
"""
# Standard library modules
import math

# Third-party library modules
from PySide2 import QtGui, QtWidgets, QtCore, QtCharts  # Import the Qt modules we'll need
import numpy as np

# Local source tree modules
import Analysis
import design  # load the MainWindow design incl. events etc. defined in Qt Designer
import SectionForces
import Material
import Results
import Geometry
import pickle
#import TableInterface

class HollowRCWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):  # PyQt5 compatible
    def __init__(self):
        super().__init__()  # initialize the QMainWindow parent object from the Qt Designer file
        self.setupUi(self)  # setup layout and widgets defined in design.py by Qt Designer
        #self.geometry_table = TableInterface.MyTable(self.coordinates_tableWidget)

        # version tag and label
        self.tag = 'v1.1'
        self.label_version.setText(self.tag)

        # --- Triggers --- (interactive elements such as actions and buttons with a custom function)
        self.exitAct.triggered.connect(self.exit_app)
        self.saveAct.triggered.connect(self.save_file)
        self.openAct.triggered.connect(self.load_file)
        self.addRowButton.clicked.connect(self.add_row)
        self.removeRowButton.clicked.connect(self.remove_row)
        self.moveUpRowButton.clicked.connect(self.move_row_up)
        self.moveDownRowButton.clicked.connect(self.move_row_down)
        self.pushButton_analyse.clicked.connect(self.initiate_analysis)
        # self.pushButton_calcSLS.clicked.connect(self.calculateSLS)
        # self.pushButton_calcULS.clicked.connect(self.calculateULS)
        self.Res = None

        # --- Signals --- (e,g, change signals from check box state, drop down selection and editable values)
        self.coordinates_tableWidget.itemChanged.connect(self.geometry_plot)
        self.tabWidget.currentChanged.connect(self.tab_changed)
        for j in range(10):  # update result plot if plot checkbox is changed
            check_box = getattr(self, 'checkBox_plot' + str(j+1))
            check_box.stateChanged.connect(self.refresh_plots)
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s', 'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            obj = getattr(self, 'lineEdit_' + string)   # e.g. obj = self.lineEdit_f_ck
            obj.textChanged.connect(self.material_plot)
        self.comboBox_nu.currentIndexChanged.connect(self.material_plot)
        self.comboBox_concrete.currentIndexChanged.connect(self.material_plot)
        self.comboBox_reinf.currentIndexChanged.connect(self.material_plot)
        # analysis checkboxes interaction
        self.checkBox_analSLS_1.toggled.connect(
            lambda checked: checked and self.checkBox_analULS_1.setChecked(False))
        self.checkBox_analULS_1.toggled.connect(
            lambda checked: checked and self.checkBox_analSLS_1.setChecked(False))

        # --- Events ---
        # self.graphicsViewResults.mouseMoveEvent = self.hoverShow
        # self.graphicsViewResults.mousePressEvent = self.onClick

        # App window size, location and title
        self.center()
        self.setWindowTitle('HollowRC section analysis tool')  # overwrites the title from Qt Designer
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        # App menu and status line
        viewMenu = self.menuBar().addMenu('View')
        viewStatusAct = QtWidgets.QAction('View statusbar', self)
        viewStatusAct.setCheckable(True)
        viewStatusAct.setChecked(True)
        viewStatusAct.triggered.connect(self.toggle_menu)
        viewMenu.addAction(viewStatusAct)
        
        aboutMenu = self.menuBar().addMenu('About')
        aboutVersionAct = QtWidgets.QAction('Check version', self)
        aboutVersionAct.triggered.connect(self.version_check)
        aboutMenu.addAction(aboutVersionAct)

        #  Correcting QT Designer bug sometimes making table headers invisible
        self.coordinates_tableWidget.horizontalHeader().setVisible(True)    # show horizontal header in Geometry table
        self.SectionForces_tableWidget.horizontalHeader().setVisible(True)  # show horizontal header in SF table
        self.SectionForces_tableWidget.verticalHeader().setVisible(True)    # show vertical header in SF table

        # initiate material comboboxes based on class defaults
        self.comboBox_concrete.clear()
        self.comboBox_concrete.addItems(Material.MatProp.conc_method_options)
        self.comboBox_concrete.setCurrentIndex(0)
        self.comboBox_reinf.clear()
        self.comboBox_reinf.addItems(Material.MatProp.reinf_method_options)
        self.comboBox_reinf.setCurrentIndex(0)

        # make sure to start at first tab (overrules Qt designer)
        self.tabWidget.setCurrentIndex(0)

    def tab_changed(self): # signal function
        if self.checkBox_analSLS_1.isChecked():
            self.pushButton_analyse.setText('Analyse SLS')
        elif self.checkBox_analULS_1.isChecked():
            self.pushButton_analyse.setText('Analyse ULS')
        else:
            self.pushButton_analyse.setText('Analyse')
        self.refresh_plots()

    def refresh_plots(self): # signal/normal function
        #self.chart.setGeometry(self.graphicsViewConcrete.frameRect())
        #self.graphicsViewConcrete.resize(??)
        if self.tabWidget.currentIndex() == 1:
            self.geometry_plot()
        elif self.tabWidget.currentIndex() == 2:
            self.material_plot()
        elif self.tabWidget.currentIndex() == 3:
            # update result plot
            try:
                self.scene.clear()  # clearing the plot if there's no results or latest analysis failed
            except:
                None
            try:
                self.result_plot(self.Res)
            except:
                None

    def save_file(self):
        try:    # try to save file 
            openfile = QtWidgets.QFileDialog.getSaveFileName(filter='*.pkj')  # save file dialog
            filename = openfile[0]
            # Load input objects from GUI
            section = self.getGeometry()
            SF = self.getSF()
            Mat = self.getMaterial()
            # open file for writing
            with open(filename, 'wb') as f:
                pickle.dump([section, SF, Mat], f) # dump objevts to file
            print('file saved')
        except FileNotFoundError:
            pass  # do nothing when user press cancel
        except Exception as e:
            print(e)
            self.show_msg_box('Failed to save file')

    def load_file(self):
        try:    # try to open file 
            openfile = QtWidgets.QFileDialog.getOpenFileName(filter='*.pkj')  # Open file dialog
            filename = openfile[0]
            # open file for reading
            with open(filename, 'rb') as f:
                section, SF, Mat = pickle.load(f) # Getting back the objects
            #  insert variables in GUI
            self.setGeometry(section)
            self.setSF(SF)
            self.setMaterial(Mat)
            print('file opened')
        except FileNotFoundError:
            pass  # do nothing when user press cancel
        except Exception as e:
            print(e)
            self.show_msg_box('Failed to open file')

    def show_msg_box(self, msg_str, title="Error Message", set_load_fac_label=False):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setWindowTitle(title)
        if isinstance(msg_str, str):
            msg.setText(msg_str)
            if set_load_fac_label:
                self.load_fac_label.setText(msg_str)
        elif isinstance(msg_str, list):                # if a list
            msg.setText(msg_str[0])                    # set text in msg box
            print(msg_str) 
            if set_load_fac_label:
                self.load_fac_label.setText(msg_str[0])    # update label
            if len(msg_str) > 1:
                msg.setInformativeText(msg_str[1])     # set info text
                if set_load_fac_label:
                    self.load_fac_label.setText(msg_str[0] + ' ' + msg_str[1])

        # msg.setDetailedText("The details are as follows: ")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()

    # a = QtWidgets.QMessageBox.critical(None, 'Error!', "Error Message!", QtWidgets.QMessageBox.Abort)
    # QtCore.qFatal('')
    # dialog = Dialog()
    #  error_dialog = QtWidgets.QErrorMessage()
    # error_dialog.showMessage('Oh no!')

    # def hoverShow(self, event):
    #     print('hover event (x,y) = ({}, {})'.format(event.x(), event.y()))

    def initiate_analysis(self):
        # Load input data from tables
        section = self.getGeometry()
        SF = self.getSF()
        Mat = self.getMaterial()

        # check if geometry is valid
        if not section.valid():
            self.show_msg_box(['Geometry error', 'The defined geometry is not valid'])
            self.Res = None
            self.refresh_plots()
            return

        # print(Geometry)
        print('SF: ' + SF.print_str())

        # Call analysis
        if self.checkBox_analSLS_1.isChecked():
            string = self.checkBox_analSLS_1.text()
            self.statusbar.showMessage(string + ' analysis initiated')
            self.Res, error_msg = Analysis.dualSection(section, SF, Mat)
            self.load_fac_label.setText('No load-factor currently applied')  # <-- might not be needed
            self.statusbar.showMessage(string + ' analysis completed')
        elif self.checkBox_analULS_1.isChecked():
            string = self.checkBox_analULS_1.text()
            self.statusbar.showMessage(string + ' analysis initiated')
            self.Res, error_msg = Analysis.planeSection(section, SF, Mat)
            self.statusbar.showMessage(string + ' analysis completed')
        else:
            self.Res = None
            error_msg = 'No analysis method is checked'
            self.load_fac_label.setText('')

        # Show message
        if error_msg:
            self.show_msg_box(error_msg, set_load_fac_label=True)
        else:
            self.load_fac_label.setText('No load-factor currently applied')

        # update result plot
        self.refresh_plots()

    def toggle_menu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def center(self):  # Move the window to the centre of the screen
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_row(self):
        self.coordinates_tableWidget.blockSignals(True)
        row_count = self.coordinates_tableWidget.rowCount()         # get number of rows
        self.coordinates_tableWidget.insertRow(row_count)           # insert new row at the end
        # insert items?
        col_count = self.coordinates_tableWidget.columnCount()      # get number of columns
        for col in range(col_count):  # loop over columns
            self.coordinates_tableWidget.setItem(row_count, col, QtWidgets.QTableWidgetItem())  # set item to row below
        self.statusbar.showMessage('Recent action: row added')
        self.coordinates_tableWidget.blockSignals(False)

    def remove_row(self):
        self.coordinates_tableWidget.blockSignals(True)
        select_row = self.coordinates_tableWidget.currentRow()      # get selected row
        # print(currentRow)
        if select_row == -1:
            self.statusbar.showMessage('Error: no row selected')
            return
        self.coordinates_tableWidget.removeRow(select_row)          # remove current row
        self.statusbar.showMessage('Recent action: row removed')
        self.coordinates_tableWidget.blockSignals(False)
        self.geometry_plot()

    def move_row_up(self):
        self.coordinates_tableWidget.blockSignals(True)
        select_row = self.coordinates_tableWidget.currentRow()      # get selected row
        if select_row == 0:
            self.statusbar.showMessage('Error: cannot move first row up')
            return
        elif select_row == -1:
            self.statusbar.showMessage('Error: no row selected')
            return
        self.coordinates_tableWidget.insertRow(select_row + 1)      # insert new row below selected row
        col_count = self.coordinates_tableWidget.columnCount()      # get number of columns

        for col in range(col_count):                                # loop over columns
            moving_item = self.coordinates_tableWidget.takeItem(select_row - 1, col)  # take item from row above
            self.coordinates_tableWidget.setItem(select_row + 1, col, moving_item)    # set item to row below

        self.coordinates_tableWidget.removeRow(select_row - 1)      # remove original row
        self.statusbar.showMessage('Recent action: row moved up')
        self.coordinates_tableWidget.blockSignals(False)
        self.geometry_plot()

    def move_row_down(self):
        self.coordinates_tableWidget.blockSignals(True)
        select_row = self.coordinates_tableWidget.currentRow()      # get selected row
        row_count = self.coordinates_tableWidget.rowCount()         # get number of rows
        if select_row == row_count - 1:                             # check if last row
            self.statusbar.showMessage('Error: cannot move last row down')
            return
        elif select_row == -1:
            self.statusbar.showMessage('Error: no row selected')
            return
        self.coordinates_tableWidget.insertRow(select_row)          # insert new row above selected row
        select_row = select_row + 1
        col_count = self.coordinates_tableWidget.columnCount()      # get number of columns

        for col in range(col_count):                                # loop over columns
            moving_item = self.coordinates_tableWidget.takeItem(select_row + 1, col)  # take item from row below
            self.coordinates_tableWidget.setItem(select_row - 1, col, moving_item)    # set item to row above

        self.coordinates_tableWidget.removeRow(select_row + 1)      # remove original row
        self.statusbar.showMessage('Recent action: row moved down')
        self.coordinates_tableWidget.blockSignals(False)
        self.geometry_plot()

    def getMaterial(self):
        # initiate material instance
        Mat = Material.MatProp()

        # get combobox selections
        Mat.conc_method = self.comboBox_concrete.currentText()
        Mat.reinf_method = self.comboBox_reinf.currentText()
        # Mat.nu_method = self.comboBox_nu.currentText()

        # getting the ext inputs or overwriting bad content     <-- OVERWRITES SHOULD HAPPEN ON CHANGED-SIGNAL
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s', 'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            # obj = self.lineEdit_f_ck
            obj = getattr(self, 'lineEdit_' + string)   # e.g.: obj = self.lineEdit_f_ck
            try:
                value = float(obj.text())   # convert item text to float
                setattr(Mat, string, value)  # Send input value to class
            except ValueError:
                value = getattr(Mat, string)   # Get default value from class
                #obj.setText(value.str())     # Replace bad item content
                obj.setText(str(value))     # Replace bad item content
        Mat.update_strengths()
        return Mat

    def setMaterial(self, Mat):
        # set combobox selections
        self.comboBox_concrete.setEditText(Mat.conc_method)
        self.comboBox_reinf.setEditText(Mat.reinf_method)
        # Mat.nu_method

        # set the ext inputs
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s', 'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            obj = getattr(self, 'lineEdit_' + string)   # e.g.: obj = self.lineEdit_f_ck
            value = getattr(Mat, string)   # Get value from class
            obj.setText(str(value))     # Replace text in lineEdit item
        # Mat.update_strengths()

    def getGeometry(self):
        X, Y, T, rho_long, rho_trans = [], [], [], [], []           # initiate lists
        table = self.coordinates_tableWidget
        row_count = table.rowCount()         # get number of rows
        for row in range(row_count):
            row_values = self.get_table_row(table, row)
            X.append(row_values[0])
            Y.append(row_values[1])
            T.append(row_values[2])
            rho_long.append(row_values[3])
            rho_trans.append(row_values[4])
        # Geometry = {'X': X, 'Y': Y, 'T': T, 'rho_long': rho_long, 'rho_trans': rho_trans}

        # initiate cross-section instances
        section = Geometry.CrossSection()
        # Loop over geometry nodes to calculate geometric properties
        for i in range(len(X)):
            X0, Y0 = X[i], Y[i]  # start node
            if i + 1 == len(X):  # if last node
                X1, Y1 = X[0], Y[0]  # end node
            else:
                X1, Y1 = X[i + 1], Y[i + 1]
            wall = Geometry.Wall([X0, X1], [Y0, Y1], T[i], rho_long[i], rho_trans[i])
            section.add_wall(wall)

        obj = self.lineEdit_wallNodeN
        try:
            value = int(obj.text())  # convert item text to integer
            # Geometry['wallNodeN'] = value  # Send input value to class
            section.set_wallNodeN(value)  # Send input value to class
        except ValueError:
            # value = 25  # set value back to default
            value = Geometry.Wall.wallNodeN  # set value back to class default
            obj.setText(str(value))  # Replace bad item content

        self.statusbar.showMessage('Geometry table data loaded')

        # return Geometry
        return section

    def setGeometry(self, section):
        table = self.coordinates_tableWidget
        table.blockSignals(True)
        # delete all rows
        row_count =table.rowCount()
        for rows in range(row_count):
            table.removeRow(0)
        # add new rows
        for wall in section.walls:
            row_count = table.rowCount()         # get number of rows
            table.insertRow(row_count)           # insert new row at the end
            # insert items
            X, Y, T, rho_long, rho_trans = wall.X[0], wall.Y[0], wall.thick, wall.rho_long, wall.rho_trans
            #for col in range(col_count):  # loop over columns
            for col, value in enumerate([X, Y, T, rho_long, rho_trans]):
                table.setItem(row_count, col, QtWidgets.QTableWidgetItem(str(value)))  # set item to row below
        table.blockSignals(False)

        obj = self.lineEdit_wallNodeN   
        value = wall.wallNodeN          # get value from last wall instance
        obj.setText(str(value))         # Replace bad item content

    def getSF(self):
        table = self.SectionForces_tableWidget
        row_values = self.get_table_row(table, 0)

        N, Mx, My, Vx, Vy, T = row_values

        # Dump into SectionForces class
        SF = SectionForces.SectionForces(N, Mx, My, Vx, Vy, T)

        # print("Section forces table data loaded")
        self.statusbar.showMessage('Section forces table data loaded')
        return SF

    def setSF(self, SF):
        table = self.SectionForces_tableWidget
        table.removeRow(0)                      # are lossing the row name 'LC' to the left!!!!
        table.insertRow(0)
        N, Mx, My, Vx, Vy, T = SF.N, SF.Mx, SF.My, SF.Vx, SF.Vy, SF.T
        for col, value in enumerate([N, Mx, My, Vx, Vy, T]):
                table.setItem(0, col, QtWidgets.QTableWidgetItem(str(value)))  # set item to row below

    def get_table_row(self, table, row):
        col_count = table.columnCount()                         # get number of columns
        row_values = []
        for col in range(col_count):
            item = table.item(row, col)                         # Retrieve item from the cell
            try:
                row_values.append(float(item.text()))           # Add item text to list as float
            except ValueError:
                item.setText('0')                               # Replace bad item content
                row_values.append(0.0)                          # Add zero to list
        return row_values

    def geometry_plot(self):
        # Load geometry data
        section = self.getGeometry()

        try:
            # unpack geometry properties
            X = section.get_X()
            Y = section.get_Y()
            T = section.get_thick()
            centreX, centreY = section.get_centre()
            wallAngle = section.get_angle()
        except:
            print('Cannot print geometry')
            view = self.graphicsViewGeometry       # define view from gui widget
            scene = QtWidgets.QGraphicsScene()     # creates a scene?
            view.setScene(scene)                   # set the created scene
            scene.clear()                          # Clear scene
            return

        # setup graphics scene
        view = self.graphicsViewGeometry       # define view from gui widget
        scene = QtWidgets.QGraphicsScene()     # creates a scene?
        view.setScene(scene)                   # set the created scene
        # scene.clear()  # Clear
        # view.scene().disconnect()
        # view.scene().clear()                 # clear scene
        # view.close()

        # Styles
        bold_pencil = QtGui.QPen(QtCore.Qt.DashLine)
        bold_pencil.setColor(QtCore.Qt.black)
        bold_pencil.setWidth(10)
        no_pencil = QtGui.QPen(QtCore.Qt.NoPen)
        thin_pencil = QtGui.QPen(QtCore.Qt.black)  # create a black pen
        blue_fill = QtGui.QBrush(QtCore.Qt.blue)   # create a blue brush
        grey_fill = QtGui.QBrush(QtCore.Qt.lightGray)  # create a light gray brush

        font = QtGui.QFont()
        font.setPixelSize(120)
        font.setBold(False)
        font.setFamily("Calibri")

        # Initiate item lists
        shade_rects = []
        centre_lines = []
        node_circles = []
        node_rects = []
        node_texts = []

        # Loop over geometry nodes to preb. for geometry plots
        for i in range(len(X)):
            X1, Y1 = X[i], Y[i]  # start node
            if i + 1 == len(X):  # if last node
                X2, Y2 = X[0], Y[0]  # end node
            else:
                X2, Y2 = X[i + 1], Y[i + 1]

            # prep. shaded geometry Periphery
            PX1 = X1 + T[i] / 2 * math.sin(-wallAngle[i])
            PY1 = Y1 + T[i] / 2 * math.cos(-wallAngle[i])
            PX2 = X1 - T[i] / 2 * math.sin(-wallAngle[i])
            PY2 = Y1 - T[i] / 2 * math.cos(-wallAngle[i])
            PX3 = X2 - T[i] / 2 * math.sin(-wallAngle[i])
            PY3 = Y2 - T[i] / 2 * math.cos(-wallAngle[i])
            PX4 = X2 + T[i] / 2 * math.sin(-wallAngle[i])
            PY4 = Y2 + T[i] / 2 * math.cos(-wallAngle[i])
            rect = QtGui.QPolygonF()
            rect.append(QtCore.QPointF(PX1, -PY1))
            rect.append(QtCore.QPointF(PX2, -PY2))
            rect.append(QtCore.QPointF(PX3, -PY3))
            rect.append(QtCore.QPointF(PX4, -PY4))
            shade_rects.append(rect)

            # # add outline on top
            # scene.addLine(QtCore.QLineF(PX1, -PY1, PX2, -PY2), thin_pencil)
            # scene.addLine(QtCore.QLineF(PX2, -PY2, PX3, -PY3), thin_pencil)
            # scene.addLine(QtCore.QLineF(PX3, -PY3, PX4, -PY4), thin_pencil)
            # scene.addLine(QtCore.QLineF(PX4, -PY4, PX1, -PY1), thin_pencil)

            # prep. centre line
            line = QtCore.QLineF(X1, -Y1, X2, -Y2)  # x pos. right, y pos. down
            centre_lines.append(line)

            # preb. node circles
            radi = 0.01 * max([max(X)-min(X), max(Y)-min(Y)])  # radius of node circles
            circle = QtWidgets.QGraphicsEllipseItem(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0)
            circle.setPen(thin_pencil)
            circle.setBrush(blue_fill)
            #circle.setAcceptDrops(True)
            #circle.dragMoveEvent = self.onItemDrag
            #circle.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
            node_circles.append(circle)

            # preb. node texts
            point = QtCore.QPointF(X1, -Y1)
            text = QtWidgets.QGraphicsTextItem()
            text.setPos(point)
            text.setPlainText("Node "+str(i+1))
            text.setFont(font)
            node_texts.append(text)

        # plot the shaded rectangles
        for rect in shade_rects:
            scene.addPolygon(rect, pen=no_pencil, brush=grey_fill)

        # plot centre lines
        for line in centre_lines:
            scene.addLine(line, bold_pencil)
        
        # plot node circles
        for circle in node_circles:
            scene.addItem(circle)

        # plot node texts
        for text in node_texts:
            scene.addItem(text)

        # plot centre text
        point = QtCore.QPointF(centreX, -centreY)
        text = QtWidgets.QGraphicsTextItem()
        text.setPlainText("CG")
        text.setFont(font)
        text.setPos(point)
        scene.addItem(text)

        # fit view to make sure that QGraphics view have no scrollbars
        view.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def material_plot(self):
        # Load material data
        Mat = self.getMaterial()

        # generate plot series
        seriesC = QtCharts.QtCharts.QLineSeries()
        seriesR = QtCharts.QtCharts.QLineSeries()
        for strain in np.linspace(-0.0035, 0.003, num=50):
            seriesC.append(strain, Mat.concreteStress(strain))
            seriesR.append(strain, Mat.reinforcementStress(strain))
        
        # Setup chart area
        self.chartC = QtCharts.QtCharts.QChart()
        self.chartC.addSeries(seriesC)
        self.chartC.createDefaultAxes()
        self.chartC.setTitle('Concrete')
        self.chartC.legend().hide()
        self.chartC.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.chartC.setGeometry(self.graphicsViewConcrete.frameRect())
        self.chartC.setBackgroundRoundness(0)

        self.chartR = QtCharts.QtCharts.QChart()
        self.chartR.addSeries(seriesR)
        self.chartR.createDefaultAxes()
        self.chartR.setTitle('Reinforcement')
        self.chartR.legend().hide()
        self.chartR.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.chartR.setGeometry(self.graphicsViewReinforcement.frameRect())
        self.chartR.setBackgroundRoundness(0)
        
        # Setup view
        viewC = self.graphicsViewConcrete        # define view from gui widget
        viewR = self.graphicsViewReinforcement        # define view from gui widget
        chartViewC = QtCharts.QtCharts.QChartView(self.chartC, viewC) # turn graphicsView object into a chartView object
        chartViewR = QtCharts.QtCharts.QChartView(self.chartR, viewR) # turn graphicsView object into a chartView object
        chartViewC.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.white))
        chartViewR.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.white))
        chartViewC.setRenderHint(QtGui.QPainter.Antialiasing)
        chartViewR.setRenderHint(QtGui.QPainter.Antialiasing)
        chartViewC.show() # cannot get the chart to fit without this
        chartViewR.show() # cannot get the chart to fit without this
        #chartView.fitInView(self.chart.Geometry(), QtCore.Qt.KeepAspectRatio)

    def result_plot(self, Res):
        # setup graphics scene
        view = self.graphicsViewResults        # define view from gui widget
        # self.scene = MyGraphicsScene()     # creates a scene?
        # self.scene.clear()
        self.scene = QtWidgets.QGraphicsScene()  # creates a scene?
        view.setScene(self.scene)                   # set the created scene

        if not self.Res:
            self.scene.clear()  # clearing the plot if there's no results or latest analysis failed
            return
        
        # unpack results dictionary
        x = Res.x
        y = Res.y
        wallAngle = Res.wallAngle
        # print(wallAngle)

        # self.scene.mousePressEvent = self.onSceneClick
        # self.scene.selectionChanged = self.selectedItem

        # Styles
        bold_pencil = QtGui.QPen(QtCore.Qt.DashLine)
        bold_pencil.setColor(QtCore.Qt.black)
        bold_pencil.setWidth(10)

        # colour list for plotting pens
        colour_list = [QtCore.Qt.darkGray,
                       QtCore.Qt.blue,
                       QtCore.Qt.red,
                       QtCore.Qt.green,
                       QtCore.Qt.darkRed,
                       QtCore.Qt.darkMagenta,
                       QtCore.Qt.darkBlue,
                       QtCore.Qt.darkCyan,
                       QtCore.Qt.darkGreen,
                       QtCore.Qt.darkYellow,  # for some reason the checkbox label goes black with this color
                       QtCore.Qt.gray,
                       QtCore.Qt.lightGray,  # too light
                       QtCore.Qt.cyan]

        # plot geometry centre line
        rect = QtGui.QPolygonF()
        for i in range(len(x)):
            rect.append(QtCore.QPointF(x[i], -y[i]))
        self.scene.addPolygon(rect, pen=bold_pencil)

        # calculate largest dimension of cross-section
        section_dim = max(max(y) - min(y), max(x) - min(x))

        # self.checkBox_plot1.isVisible()
        for j in range(Res.plot_count): # looping over the different result distributions
            pencil = QtGui.QPen(colour_list[j]) # create pen with next colour
            fill = QtGui.QBrush(colour_list[j]) # create brush with same colour
            
            pencil.setWidth(10)
            check_box = getattr(self, 'checkBox_plot' + str(j+1))
            # update checkbox visibility
            if not check_box.isVisible():
                check_box.setVisible(True)
            check_box.setText(Res.plot_names[j])
            check_box.setStyleSheet("color: " + colour_list[j].name.decode())
            
            # plot if checked
            if check_box.isChecked():
                scale = Res.plot_scale[j] * section_dim / max(1e-12, max(abs(Res.plot_data[j])))
                rect = QtGui.QPolygonF() # outline polygon
                for i in range(len(Res.x)):
                    PX = Res.x[i] + scale * Res.plot_data[j][i] * math.sin(-Res.wallAngle[i])
                    PY = Res.y[i] + scale * Res.plot_data[j][i] * math.cos(-Res.wallAngle[i])
                    if Res.x[i] == Res.x[i - 1] and Res.y[i] == Res.y[i - 1]:  # new wall element started
                        rect.append(QtCore.QPointF(Res.x[i], -Res.y[i]))  # add plot point at geometric corner
                        # prepare/plot shading
                        if i>0:
                            # plot shading
                            rect2.append(QtCore.QPointF(Res.x[i], -Res.y[i]))  # add plot point at geometric corner
                            poly_item = QtWidgets.QGraphicsPolygonItem(rect2)
                            poly_item.setBrush(fill)
                            poly_item.setOpacity(0.2)
                            self.scene.addItem(poly_item)
                            # self.scene.addPolygon(rect2, brush=fill)

                        rect2 = QtGui.QPolygonF() # shading polygon
                        rect2.append(QtCore.QPointF(Res.x[i], -Res.y[i]))  # add plot point at geometric corner
                        rect2.append(QtCore.QPointF(PX, -PY))
                    else:
                        # add point for shading polygon
                        rect2.append(QtCore.QPointF(PX, -PY))
                    rect.append(QtCore.QPointF(PX, -PY))

                    # prepare line for mouse clicks
                    line = QtCore.QLineF(PX, -PY, Res.x[i], -Res.y[i])  # x pos. right, y pos. down
                    line_item = QtWidgets.QGraphicsLineItem(line)
                    line_item.setPen(pencil)
                    line_item.data_str = '{}: {:.3f} {}'.format(Res.plot_names[j], Res.plot_data[j][i], Res.plot_units[j])  # string for click ev.
                    line_item.setAcceptHoverEvents(True)
                    line_item.mousePressEvent = self.onItemClick
                    # line_item.mouseMoveEvent = self.onItemClick
                    # self.scene.addLine(line, pencil)
                    self.scene.addItem(line_item)
                # plot shading
                rect2.append(QtCore.QPointF(Res.x[i], -Res.y[i]))  # add plot point at geometric corner
                poly_item = QtWidgets.QGraphicsPolygonItem(rect2)
                poly_item.setBrush(fill)
                poly_item.setOpacity(0.2)
                self.scene.addItem(poly_item)
                # plot result outline
                self.scene.addPolygon(rect, pen=pencil)

        # Hide the remaining unneeded check boxes
        for j in range(Res.plot_count, 10):
            check_box = getattr(self, 'checkBox_plot' + str(j + 1))
            check_box.setVisible(False)

        # Fit plottet items in view
        view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    # def selectedItem(self):
    #     print('selection changed')
    #     print(self.scene.selectedItems())

    def exit_app(self):  # not executed if user exit by clicking on upper right cross
        # root.destroy()  # destroy all windows (parent, child) within the root instance
        print("Terminated")
        self.close()  # stop the active QApplication instance and sends a QCloseEvent

    def resizeEvent(self, event): # Event
        self.refresh_plots()

    def onItemDrag(self, event):
        print('onItemDrag event activated')
        print(event)

    # def onSceneClick(self, event):
    #     x = event.scenePos().x()
    #     y = event.scenePos().y()
    #     print('press event (x,y) = ({}, {})'.format(x, y))
    #     # view = self.graphicsViewResults
    #     # print('view rect ', view.rect())
    #     # print('view-scene rect ', view.sceneRect())
    #     # print('scene panel rect ', self.scene.mousePressEvent())
    #     items = self.scene.items(event.scenePos())
    #     print(items)
    #     # for item in items:
    #         # item.is

    def onItemClick(self, event): # when user clicks on result the values are listed in the status line
        # x = event.scenePos().x()
        # y = event.scenePos().y()
        # print('Item press event (x,y) = ({}, {})'.format(x, y))
        # print('data string: ', data_str)
        # view = self.graphicsViewResults
        # print('view rect ', view.rect())
        # print('view-scene rect ', view.sceneRect())
        # print('scene panel rect ', self.scene.mousePressEvent())
        items = self.scene.items(event.scenePos())
        msg = 'Point data: '
        for item in items:
            if hasattr(item, 'data_str'):
                msg += "{}, ".format(item.data_str)
        if len(msg) > 13:
            self.statusbar.showMessage(msg[:-2])
            print(msg[:-2])

    # def mousePressEvent(self, event):
    #     # pen = QPen(QtCore.Qt.black)
    #     # brush = QBrush(QtCore.Qt.black)
    #     x = event.scenePos().x()
    #     y = event.scenePos().y()
    #     # if self.opt == "Generate":
    #     #     self.addEllipse(x, y, 4, 4, pen, brush)
    #     # elif self.opt == "Select":
    #     print('from pressevent ', x, y)
    #     print('view rect ', self.graphicsViewResults.rect())

    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()    # sends a QCloseEvent

    def closeEvent(self, event):  # reimplementing the QWidget closeEvent() event handler.
        QMessageBox = QtWidgets.QMessageBox
        reply = QMessageBox.question(self, 'Exit confirmation',
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.deleteLater()  # Schedule objects for deletion (to avoid nonzero exit code)
            event.accept()
        else:
            event.ignore()

    def version_check(self):
        # This method retreivings the latest release version from GitHub
        import requests
        r = requests.get('https://api.github.com/repos/Kleissl/HollowRC/releases/latest')
        # print(r)
        if r.status_code == 200:
            # print(r.headers['content-type'])
            data = r.json()
            # print(data.keys())
            # for key in data:
            #     print(key, 'corresponds to', data[key])
            latest_tag = data['tag_name']
            published = data['published_at']
            print('The latest release (' + latest_tag +') was published at ' + published)
            if latest_tag == self.tag:
                print('version up-to-date')
                msg_str = 'version up-to-date'
                msg_info_str = 'The current version ('+ self.tag +') matches the latest release'
            else:
                msg_str = 'The application ('+ self.tag +') is NOT up-to-date!'
                msg_info_str = 'There is a newer release (' + latest_tag + ') from ' + published + ' available for download at https://github.com/Kleissl/HollowRC/releases/latest'
            print(msg_str)
            self.show_msg_box([msg_str, msg_info_str], title='Information')
        else:
            print('Github API requests returned statuscode', r.status_code)

# # Creating my own GraphicsScene class so I can overwrite its mousePressEvent
# class MyGraphicsScene(QtWidgets.QGraphicsScene):
#     def __init__(self, parent=None):
#         # QtWidgets.QGraphicsScene.__init__(self, parent)
#         # super(MyGraphicsScene, self).__init__(parent)
#         super().__init__()
#         # self.setSceneRect(-100, -100, 200, 200)

#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)
#         print(event.pos())
#         x = event.scenePos().x()
#         y = event.scenePos().y()
#         print('mousepressevent x,y= ', x, y)
#         # items = QtWidgets.QGraphicsItem.scene().items(event.scenePos())
#         # QtWidgets.QGraphicsItem.item
#         # items = self.scene().items(event.scenePos())
#         # print('Plots:', [x for x in items if isinstance(x, pg.PlotItem)]
#         # self.items()
#         # item = QtWidgets.QGraphicsTextItem("CLICK")
#         # item.setPos(event.scenePos())
#         # self.addItem(item)

# # # Creating my own line item class so I can overwrite its mousePressEvent
# # line_item = QtWidgets.QGraphicsLineItem(line)
# class myQGraphicsLineItem(QtWidgets.QGraphicsLineItem):
#     def __init__(self, parent=None):
#         # QtWidgets.QGraphicsScene.__init__(self, parent)
#         # super(MyGraphicsScene, self).__init__(parent)
#         super().__init__()
#         # self.setSceneRect(-100, -100, 200, 200)
#
#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)
#         print(event.pos())
#         x = event.scenePos().x()
#         y = event.scenePos().y()
#         print('item_mousePressEvent x,y= ', x, y)
#         # items = QtWidgets.QGraphicsItem.scene().items(event.scenePos())
#         # QtWidgets.QGraphicsItem.item
#         # items = self.scene().items(event.scenePos())
#         # print('Plots:', [x for x in items if isinstance(x, pg.PlotItem)]
#         # self.items()
#         # item = QtWidgets.QGraphicsTextItem("CLICK")
#         # item.setPos(event.scenePos())
#         # self.addItem(item)
