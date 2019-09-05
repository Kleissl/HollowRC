# -*- coding: utf-8 -*-
"""
This module containes all the application window classes for HollowRC

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
import hollow_window  # load the window design incl. events etc. defined in Qt Designer
import SectionForces
import Material
# import Results
import Geometry
import pickle
import Plots
# import TableInterface


class HollowWindow(QtWidgets.QMainWindow, hollow_window.Ui_MainWindow):
    '''
    HollowRC window class
    '''
    def __init__(self):
        super().__init__()  # initialize the QMainWindow parent object from the Qt Designer file
        self.setupUi(self)  # setup layout and widgets defined in Qt Designer
        # self.geometry_table = TableInterface.MyTable(self.coordinates_tableWidget)

        # version tag and label
        self.tag = 'v1.3'
        self.label_version.setText(self.tag)

        # --- Triggers ---
        # Connect the interactive elements with a custom method)
        self.exitAct.triggered.connect(self.exit_app)
        self.saveAct.triggered.connect(self.save_file)
        self.openAct.triggered.connect(self.load_file)
        self.analyseAct.triggered.connect(self.initiate_analysis)
        self.addRowButton.clicked.connect(self.add_row)
        self.removeRowButton.clicked.connect(self.remove_row)
        self.moveUpRowButton.clicked.connect(self.move_row_up)
        self.moveDownRowButton.clicked.connect(self.move_row_down)
        # self.pushButton_calcSLS.clicked.connect(self.calculateSLS)
        # self.pushButton_calcULS.clicked.connect(self.calculateULS)
        self.Res = None

        # --- Signals ---
        # update geometry plot if table item changes
        self.coordinates_tableWidget.itemChanged.connect(
            self.geometry_plot)
        # call setGeometry method if a new_section signal is received
        self.graphicsViewGeometry.new_section.connect(
            self.setGeometry)

        self.graphicsViewGeometry.scene_clicked.connect(
            self.node_coords_by_click)

        # connect the status_str signal with the update_statusline method
        self.graphicsViewResults.status_str.connect(
            self.update_statusline)

        # self.graphicsViewGeometry.itemChanged.connect(self.node_moved)
        self.tabWidget.currentChanged.connect(self.tab_changed)

        check_boxes = []
        for j in range(10):  # update result plot if plot checkbox is changed
            check_box = getattr(self, 'checkBox_plot' + str(j+1))
            check_box.stateChanged.connect(self.refresh_visible_plots)
            check_boxes.append(check_box)
        self.graphicsViewResults.set_check_boxes(check_boxes)
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s',
                    'alpha_cc', 'gamma_c', 'gamma_s']

        for string in obj_list:
            # get e.g. obj = self.lineEdit_f_ck
            obj = getattr(self, 'lineEdit_' + string)
            # update material plot if any of the inputs changes
            obj.textChanged.connect(self.material_plot)
        self.comboBox_nu.currentIndexChanged.connect(self.material_plot)
        self.comboBox_concrete.currentIndexChanged.connect(self.material_plot)
        self.comboBox_reinf.currentIndexChanged.connect(self.material_plot)

        # analysis checkboxes interaction
        self.checkBox_analSLS_1.toggled.connect(
            lambda checked: checked and self.checkBox_analULS_1.setChecked(False))
        self.checkBox_analULS_1.toggled.connect(
            lambda checked: checked and self.checkBox_analSLS_1.setChecked(False))

        # App window size, location and title
        self.center()
        self.title_str = 'HollowRC section analysis tool'
        self.setWindowTitle(self.title_str)  # overwrites Qt Designer
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

    def tab_changed(self):  # signal function
        pass
        # if self.checkBox_analSLS_1.isChecked():
        #     self.analyseAct.setText('Analyse SLS')
        # elif self.checkBox_analULS_1.isChecked():
        #     self.analyseAct.setText('Analyse ULS')
        # else:
        #     self.analyseAct.setText('Analyse')
        self.refresh_visible_plots()

    def refresh_visible_plots(self):  # signal/normal function
        # self.chart.setGeometry(self.graphicsViewConcrete.frameRect())
        # self.graphicsViewConcrete.resize(??)
        if self.tabWidget.currentIndex() == 1:
            self.geometry_plot()
        elif self.tabWidget.currentIndex() == 2:
            self.material_plot()
        elif self.tabWidget.currentIndex() == 3:
            # update result plot
            try:
                self.result_plot(self.Res)
            except:
                pass

    def save_file(self):
        '''
        Save to pickle file
        '''
        try:
            # save file dialog
            openfile = QtWidgets.QFileDialog.getSaveFileName(filter='*.pkj')
            filename = openfile[0]
            # Load input objects from GUI
            section = self.getGeometry()
            SF = self.getSF()
            Mat = self.getMaterial()
            Analysis = {'checkBox_analSLS_1': self.checkBox_analSLS_1.isChecked(),
                        'checkBox_analULS_1': self.checkBox_analULS_1.isChecked()}
            # open file for writing
            with open(filename, 'wb') as f:
                # dump objects to file
                pickle.dump([section, SF, Mat, Analysis], f)
            print('File saved to ' + filename)
            # update window title
            title = self.title_str + (f' ({filename})')
            self.setWindowTitle(title)
        except FileNotFoundError:
            pass  # do nothing when user press cancel
        except Exception as e:
            print(e)
            self.show_msg_box('Failed to save file')

    def load_file(self):
        '''
        Load pickle file
        '''
        try:
            # Open file dialog
            openfile = QtWidgets.QFileDialog.getOpenFileName(filter='*.pkj')
            filename = openfile[0]
            # open file for reading
            with open(filename, 'rb') as f:
                # Getting back the objects
                section, SF, Mat, Analysis = pickle.load(f)
            #  insert variables in GUI
            self.setGeometry(section)
            self.setSF(SF)
            self.setMaterial(Mat)
            self.checkBox_analSLS_1.setChecked(Analysis['checkBox_analSLS_1'])
            self.checkBox_analULS_1.setChecked(Analysis['checkBox_analULS_1'])
            print('File opened from ' + filename)
            # update window title
            title = self.title_str + (f' ({filename})')
            self.setWindowTitle(title)
        except FileNotFoundError:
            pass  # do nothing when user press cancel
        except Exception as e:
            print(e)
            self.show_msg_box('Failed to open file')

            # clear results and plot of results
            self.Res = None
            self.result_plot(self.Res)
            self.refresh_visible_plots()                #  <---- NONE OF THIS SEEMS TO WORK !!!
            self.graphicsViewResults.clear_scene()

    def show_msg_box(self, msg_str, title="Error Message",
                     set_load_fac_label=False):
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
        return retval

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
        valid, msg = section.valid()
        if not valid:
            self.show_msg_box(['The defined geometry is not valid', msg])
            self.Res = None
            self.refresh_visible_plots()
            return

        # print(Geometry)
        print('SF: ' + SF.print_str())

        # switch to Loading & Result tab
        self.tabWidget.setCurrentIndex(3)

        # set mouse cursor to WaitCursor
        self.setCursor(QtCore.Qt.WaitCursor)
        try:
            # Call analysis
            if self.checkBox_analSLS_1.isChecked():
                # execute SLS analysis
                string = self.checkBox_analSLS_1.text()
                self.statusbar.showMessage(string + ' analysis initiated')
                self.Res = Analysis.SLS_analysis(section, SF, Mat)
                error_msg = None  # errors are now passed as exceptions
                self.load_fac_label.setText('No load-factor currently applied')  # <-- might not be needed
                self.statusbar.showMessage(string + ' analysis completed')
            elif self.checkBox_analULS_1.isChecked():
                # execute ULS analysis
                string = self.checkBox_analULS_1.text()
                self.statusbar.showMessage(string + ' analysis initiated')
                self.Res, error_msg = Analysis.ULS_analysis(section, SF, Mat)
                self.statusbar.showMessage(string + ' analysis completed')
            else:
                self.Res = None
                error_msg = 'No analysis method is checked'
                self.load_fac_label.setText('')
        except Analysis.MyOptimizerError as e:
            # caught a MyOptimizerError exception
            self.show_msg_box([str(e), e.discription])
            error_msg = None
        else:
            # no MyOptimizerError exception
            self.load_fac_label.setText('No load-factor currently applied')

        # Show message
        if error_msg:
            self.show_msg_box(error_msg, set_load_fac_label=True)
        else:
            self.load_fac_label.setText('No load-factor currently applied')

        # update result plot
        self.refresh_visible_plots()

        # return mouse cursor to normal ArrowCursor
        self.setCursor(QtCore.Qt.ArrowCursor)

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

    def node_coords_by_click(self, signal_value):
        x = signal_value['x']
        y = signal_value['y']
        self.graphicsViewGeometry.awaits_click = False  # stop further click signals from being send
        table = self.coordinates_tableWidget
        table.blockSignals(True)                # block signals
        row_index = table.rowCount() - 1        # get index of last row
        x_item = table.item(row_index, 0)       # Retrieve item from the cell
        x_item.setText(str(x))                  # Replace bad item content
        y_item = table.item(row_index, 1)
        table.blockSignals(False)               # turn signals back on before last change to trigger update
        y_item.setText(str(-y))                 # Replace bad item content

    def add_row(self):
        self.coordinates_tableWidget.blockSignals(True)
        row_count = self.coordinates_tableWidget.rowCount()         # get number of rows
        self.coordinates_tableWidget.insertRow(row_count)           # insert new row at the end
        # insert items?
        col_count = self.coordinates_tableWidget.columnCount()      # get number of columns
        for col in range(2):  # loop over columns
            self.coordinates_tableWidget.setItem(row_count, col, QtWidgets.QTableWidgetItem('click'))  # set item to row below
        # copy values from previous row
        row_values = self.get_table_row(self.coordinates_tableWidget, row_count - 1)
        for col in range(2, col_count):  # loop over non-coordinates columns
            value = row_values[col]
            self.coordinates_tableWidget.setItem(row_count, col, QtWidgets.QTableWidgetItem('{:.6g}'.format(value)))  # set item to row below
        self.statusbar.showMessage('Recent action: row added - Click on geometry plot scene to load coordinates into the newly added row')
        self.coordinates_tableWidget.blockSignals(False)
        self.graphicsViewGeometry.awaits_click = True       # will allow for scene_clicked signals

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
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s',
                    'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            # get e.g. obj = self.lineEdit_f_ck
            obj = getattr(self, 'lineEdit_' + string)
            try:
                value = float(obj.text())   # convert item text to float
                if value == 0:
                    raise ValueError
                setattr(Mat, string, value)  # Send input value to class
            except ValueError:
                self.show_msg_box(['Material input error', 'Input value "{}" for {} is not valid. {} returned to default value.'.format(obj.text(), string, string)])
                value = getattr(Mat, string)   # Get default value from class
                obj.setText(str(value))     # Replace bad item content

        Mat.update_strengths()
        return Mat

    def setMaterial(self, Mat):
        '''
        Populate material input cells with material instance attributes
        '''
        # set combobox selections
        self.comboBox_concrete.setEditText(Mat.conc_method)
        self.comboBox_reinf.setEditText(Mat.reinf_method)
        # Mat.nu_method

        # set the ext inputs
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s',
                    'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            # get e.g. obj = self.lineEdit_f_ck
            obj = getattr(self, 'lineEdit_' + string)
            value = getattr(Mat, string)   # Get value from class
            obj.setText(str(value))     # Replace text in lineEdit item

    def getGeometry(self):
        '''
        Build section instance from geometry table
        '''
        X, Y, T, rho_long, rho_trans = [], [], [], [], []
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
            if value == 0:
                raise ValueError
            section.set_wallNodeN(value)  # Send input value to section class
        except ValueError:
            # value = 25  # set value back to default
            self.show_msg_box(['Geometry input error', 'Input value "{}" for {} is not valid. {} returned to default value.'.format(obj.text(), 'no. of data points', 'No. of data points')])
            value = Geometry.Wall.wallNodeN  # set value back to class default
            obj.setText(str(value))  # Replace bad item content

        self.statusbar.showMessage('Geometry table data loaded')

        # return Geometry
        return section

    def setGeometry(self, section):
        '''
        Populate table with section instance attributes
        '''
        table = self.coordinates_tableWidget
        table.blockSignals(True)
        # delete all rows
        row_count = table.rowCount()
        for _ in range(row_count):
            table.removeRow(0)
        # add new rows
        for wall in section.walls:
            row_count = table.rowCount()         # get number of rows
            table.insertRow(row_count)           # insert new row at the end
            # insert items
            X, Y, T, rho_long, rho_trans = wall.X[0], wall.Y[0], wall.thick, wall.rho_long, wall.rho_trans
            # loop over columns
            for col, value in enumerate([X, Y, T, rho_long, rho_trans]):
                table.setItem(row_count, col, QtWidgets.QTableWidgetItem('{:.6g}'.format(value)))  # set item to row below
        table.blockSignals(False)

        obj = self.lineEdit_wallNodeN
        value = wall.wallNodeN          # get value from last wall instance
        obj.setText(str(value))         # Replace bad item content

    def getSF(self):
        table = self.SectionForces_tableWidget
        row_values = self.get_table_row(table, 0)

        N, My, Mz, Vy, Vz, T = row_values

        # Dump into SectionForces class
        SF = SectionForces.SectionForces(N, My, Mz, Vy, Vz, T)

        # print("Section forces table data loaded")
        self.statusbar.showMessage('Section forces table data loaded')
        return SF

    def setSF(self, SF):
        table = self.SectionForces_tableWidget
        # table.removeRow(0)       # The row header "LC" is lost if the row is removed/inserted
        # table.insertRow(0)
        N, My, Mz, Vy, Vz, T = SF.N, SF.My, SF.Mz, SF.Vy, SF.Vz, SF.T
        for col, value in enumerate([N, My, Mz, Vy, Vz, T]):
                # table.setItem(0, col, QtWidgets.QTableWidgetItem(str(value)))  # set item to row below
                table.setItem(0, col, QtWidgets.QTableWidgetItem('{:.6g}'.format(value)))  # set item to row below

    def get_table_row(self, table, row):
        col_count = table.columnCount()                         # get number of columns
        row_values = []
        for col in range(col_count):
            item = table.item(row, col)                         # Retrieve item from the cell
            try:
                row_values.append(float(item.text()))           # Add item text to list as float
            except ValueError:
                header = table.horizontalHeaderItem(col).text()
                self.show_msg_box(['Table input error', 'Input value "{}" for row index {} in {} column not valid. Value set to zero.'.format(item.text(), row, header)])
                item.setText('0')                               # Replace bad item content
                row_values.append(0.0)                          # Add zero to list
        return row_values

    def geometry_plot(self): 
        self.graphicsViewGeometry.awaits_click = False          # properly triggered by manual change in geometry table thus no longer awaits node_coords_by_click
        section = self.getGeometry()                            # Load geometry data
        self.graphicsViewGeometry.plot_all(section)             # update plot

    def material_plot(self):
        # Load material data
        Mat = self.getMaterial()

        # generate plot series
        seriesC = QtCharts.QtCharts.QLineSeries()
        seriesR = QtCharts.QtCharts.QLineSeries()
        for strain in np.linspace(-0.0035, 0.003, num=200):
            seriesC.append(strain, Mat.concreteStress(strain))
            seriesR.append(strain, Mat.reinforcementStress(strain))

        # Setup concrete chart area
        self.chartC = QtCharts.QtCharts.QChart()
        self.chartC.addSeries(seriesC)
        self.chartC.createDefaultAxes()
        # self.chartC.axes(orientation=QtCore.Qt.Horizontal)
        # self.chartC.addAxis(QtCharts.QtCharts.QAbstractAxis, QtCore.Qt.Horizontal)
        self.chartC.setTitle('Concrete')
        self.chartC.legend().hide()
        self.chartC.setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.chartC.setGeometry(self.graphicsViewConcrete.frameRect())
        self.chartC.setBackgroundRoundness(0)

        # Setup reinforcement chart area
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
        chartViewC.show()  # cannot get the chart to fit without this
        chartViewR.show()  # cannot get the chart to fit without this
        # chartView.fitInView(self.chart.Geometry(), QtCore.Qt.KeepAspectRatio)

    def result_plot(self, Res):
        # print('calling result plot class')
        self.graphicsViewResults.plot_all(Res)             # update plot
        # print('finished calling result plot class')

    # class FitSceneInViewGraphicsView(QtWidgets.QGraphicsView):
    #     """
    #     Extension of QGraphicsView that fits the scene rectangle of the scene into the view when the view is shown.
    #     This avoids problems with the size of the view different before any layout can take place and therefore
    #     fitInView failing.
    #     """
    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #     def showEvent(self, event):
    #         """
    #         The view is shown (and therefore has correct size). We fit the scene rectangle into the view without
    #         distorting the scene proportions.
    #         """
    #         self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
    #         super().showEvent(event)

    def resizeEvent(self, event):  # overwrites the resizeEvent
        self.refresh_visible_plots()
        return QtWidgets.QMainWindow.resizeEvent(self, event)

    def update_statusline(self, string):
        self.statusbar.showMessage(string)

    def keyPressEvent(self, event):
        '''
        Reimplementation of the QWidget keyPressEvent() event handler.
        Allow the user to exit app from escape key.
        '''
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()  # Initiate QCloseEvent

    def exit_app(self):
        '''
        Method for when the user clicks the "Exit" bottom
        (not executed if user exit by clicking on upper right cross).
        '''
        self.close()  # Initiate QCloseEvent

    def closeEvent(self, event):
        '''
        Reimplementation of the QWidget closeEvent() event handler
        with a QMessage confirmation
        If accepted this will stop the active QApplication instance
        '''
        QMessageBox = QtWidgets.QMessageBox
        reply = QMessageBox.question(self, 'Exit confirmation',
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('CloseEvent accepted')
            # Schedule objects for deletion (avoids nonzero exit code)
            self.deleteLater()
            event.accept()
        else:
            print('CloseEvent ignored')
            event.ignore()

    def version_check(self):
        '''
        This method retreives the latest release version from GitHub
        '''
        import requests
        url = 'https://api.github.com/repos/Kleissl/HollowRC/releases/latest'
        r = requests.get(url)
        if r.status_code == 200:
            # print(r.headers['content-type'])
            data = r.json()
            # print(data.keys())
            # for key in data:
            #     print(key, 'corresponds to', data[key])
            latest_tag = data['tag_name']
            published = data['published_at']
            print('The latest release (' + latest_tag + ') was published at ' + published)
            if latest_tag == self.tag:
                msg_str = 'Version up-to-date'
                msg_info_str = 'The current version (' + self.tag + ') matches the latest release from https://github.com/Kleissl/HollowRC/releases/latest'
            else:
                msg_str = 'The application (' + self.tag + ') is NOT up-to-date!'
                msg_info_str = 'There is a newer release (' + latest_tag + ') from ' + published + ' available for download at https://github.com/Kleissl/HollowRC/releases/latest'
            print(msg_str)
            self.show_msg_box([msg_str, msg_info_str], title='Information')
        else:
            print('Github API requests returned statuscode', r.status_code)
