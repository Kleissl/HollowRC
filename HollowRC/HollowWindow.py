# -*- coding: utf-8 -*-
"""
This module containes all the GUI application window classes for HollowRC

Author: Kenneth C. Kleissl
"""
# Standard library modules
import math

# Third-party library modules
from PySide2 import QtGui, QtWidgets, QtCore, QtCharts  # Import the Qt modules we'll need
import numpy as np

# Local source tree modules
from . import Analysis
from . import hollow_window  # load the window design incl. events etc. defined in Qt Designer
from .SectionForces import SectionForces
from . import Material
# import .Results
from . import Geometry
import pickle
from . import Plots
from .TableInterface import MyTable


class HollowWindow(QtWidgets.QMainWindow, hollow_window.Ui_MainWindow):
    '''
    HollowRC window class
    '''
    Res = None

    def __init__(self):
        super().__init__()  # initialize the QMainWindow parent object from the Qt Designer file
        self.setupUi(self)  # setup layout and widgets defined in Qt Designer

        # version tag and label
        self.tag = 'v1.5'
        self.label_version.setText(self.tag)

        # initiate key parameters
        self.section = self.get_geometry()
        self.SF = self.get_SF()
        self.mat = self.get_material()

        # initiate plots
        self.graphicsViewGeometry.plot(self.section)

        # --- Triggers ---
        # Connect the interactive elements with a custom method)
        self.exitAct.triggered.connect(self.exit_app)
        self.saveAct.triggered.connect(self.save_file)
        self.openAct.triggered.connect(self.load_file)
        self.analyseAct.triggered.connect(self.initiate_analysis)
        self.addRowButton.clicked.connect(self.geometry_table.add_row)
        self.removeRowButton.clicked.connect(self.geometry_table.remove_row)
        self.moveUpRowButton.clicked.connect(self.geometry_table.move_row_up)
        self.moveDownRowButton.clicked.connect(self.geometry_table.move_row_down)

        # --- Signals ---
        self.geometry_table.itemChanged.connect(self.geometry_table_changed)  # update geometry plot if table item changes
        self.graphicsViewGeometry.new_section.connect(self.set_geometry_table)  # call set_geometry method if a new_section signal is received
        self.graphicsViewGeometry.scene_clicked.connect(self.geometry_table.node_coords_by_click)  # pass clicked coordinates to table object
        self.tabWidget.currentChanged.connect(self.tab_changed)

        # connect the status message signals with the update_statusline method
        self.graphicsViewResults.status_str.connect(self.update_statusline)
        self.geometry_table.status_msg.connect(self.update_statusline)
        self.SectionForces_tableWidget.status_msg.connect(self.update_statusline)

        # connect the error message signals with the show_msg_box method
        self.geometry_table.error_msg.connect(self.show_msg_box)
        self.SectionForces_tableWidget.error_msg.connect(self.show_msg_box)

        # result signals
        check_boxes = []
        for j in range(10):  # update result plot if plot checkbox is changed
            check_box = getattr(self, 'checkBox_plot' + str(j+1))
            check_box.stateChanged.connect(self.graphicsViewResults.refresh_plot)
            check_boxes.append(check_box)
        self.graphicsViewResults.set_check_boxes(check_boxes)

        # material signals
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s',
                    'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            # get e.g. obj = self.lineEdit_f_ck
            obj = getattr(self, 'lineEdit_' + string)
            # update material plot if any of the inputs changes
            obj.textEdited.connect(self.material_changed)
            obj.editingFinished.connect(self.material_editingFinished)  # textChanged/textEdited/editingFinished?
        self.comboBox_nu.currentIndexChanged.connect(self.material_changed)
        self.comboBox_concrete.currentIndexChanged.connect(self.material_changed)
        self.comboBox_reinf.currentIndexChanged.connect(self.material_changed)

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

        # Fix QT Designer bug where table headers sometimes goes invisible
        self.geometry_table.horizontalHeader().setVisible(True)             # show hor. header
        self.SectionForces_tableWidget.horizontalHeader().setVisible(True)  # show hor. header
        self.SectionForces_tableWidget.verticalHeader().setVisible(True)    # show vert. header
        self.SectionForces_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # uniform column width when stretching
        for col in [6, 7]:
            self.SectionForces_tableWidget.set_cell_value(0, col, '', flag=QtCore.Qt.ItemIsEnabled, background=QtGui.QColor(240, 240, 240))  # locks an item

        # Fix UI conversion error where table cell tooltips goes missing
        self.update_rho_tooltips()

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
        # if self.checkBox_analSLS_1.isChecked():
        #     self.analyseAct.setText('Analyse SLS')
        # elif self.checkBox_analULS_1.isChecked():
        #     self.analyseAct.setText('Analyse ULS')
        # else:
        #     self.analyseAct.setText('Analyse')
        self.refresh_visible_plots()

    def refresh_visible_plots(self):  # signal/normal function
        if self.tabWidget.currentIndex() == 1:
            self.graphicsViewGeometry.refresh_plot()
        elif self.tabWidget.currentIndex() == 2:
            self.material_plot()
        elif self.tabWidget.currentIndex() == 3:
            self.graphicsViewResults.refresh_plot()

    def save_file(self):
        '''
        Save to pickle file
        '''
        try:
            # save file dialog
            openfile = QtWidgets.QFileDialog.getSaveFileName(filter='*.pkj')
            filename = openfile[0]
            # Load analysis status from GUI
            Analysis = {'checkBox_analSLS_1': self.checkBox_analSLS_1.isChecked(),
                        'checkBox_analULS_1': self.checkBox_analULS_1.isChecked()}
            # open file for writing
            with open(filename, 'wb') as f:
                # dump objects to file
                pickle.dump([self.section, self.SF, self.mat, Analysis], f)
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
                self.section, self.SF, self.mat, Analysis = pickle.load(f)
            #  insert variables in GUI
            self.set_geometry_table(self.section)
            self.set_SF_table(self.SF)
            self.set_material(self.mat)
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
        self.graphicsViewResults.plot(self.Res)  # use plot() to reset Res attribute

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
        self.SF = self.get_SF()

        # check if geometry is valid
        valid, msg = self.section.valid()
        if not valid:
            self.show_msg_box(['The defined geometry is not valid', msg])
            self.Res = None
            self.graphicsViewResults.plot(self.Res)
            return

        print('---------- Analysis inputs ----------')
        print(self.section)
        print(self.mat)
        print(self.SF)

        # switch to Loading & Result tab
        self.tabWidget.setCurrentIndex(3)

        # set mouse cursor to WaitCursor
        self.setCursor(QtCore.Qt.WaitCursor)
        try:
            # Call analysis
            if self.checkBox_analSLS_1.isChecked():
                # execute SLS analysis
                string = self.checkBox_analSLS_1.text().replace('&&', '&')
                self.statusbar.showMessage(string + ' analysis initiated')
                self.Res = Analysis.SLS_analysis(self.section, self.SF, self.mat)
                error_msg = None  # errors are now passed as exceptions
                self.load_fac_label.setText('No load-factor currently applied')  # <-- might not be needed
                self.statusbar.showMessage(string + ' analysis completed')
            elif self.checkBox_analULS_1.isChecked():
                # execute ULS analysis
                string = self.checkBox_analULS_1.text().replace('&&', '&')
                self.statusbar.showMessage(string + ' analysis initiated')
                self.Res, error_msg = Analysis.ULS_analysis(self.section, self.SF, self.mat)
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
        self.graphicsViewResults.plot(self.Res)

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

    def get_geometry(self):
        '''
        Build section instance from geometry table
        '''
        X, Y, T, rho_long, rho_trans = [], [], [], [], []
        table = self.geometry_table
        row_count = table.rowCount()         # get number of rows
        for row in range(row_count):
            row_values = self.geometry_table.get_table_row(row)
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
            self.show_msg_box(['Geometry input error',
                               f'Input value "{obj.text()}" for no. of data points is not valid. No. of data points returned to default value.'])
            value = Geometry.Wall.wallNodeN  # set value back to class default
            obj.setText(str(value))  # Replace bad item content

        return section

    def set_geometry_table(self, section):
        '''
        Populate table with section instance attributes
        '''
        table = self.geometry_table
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
                item = QtWidgets.QTableWidgetItem('{:.6g}'.format(value))
                if col > 2:
                    item.setToolTip(f'{value*T*10**3} mm2/m')  # reinforcement amount
                else:
                    item.setToolTip('')  # reset all tool tips
                table.setItem(row_count, col, item)  # set item to row below
        table.blockSignals(False)

        obj = self.lineEdit_wallNodeN
        value = wall.wallNodeN          # get value from last wall instance
        obj.setText(str(value))         # Replace bad item content
        self.geometry_table_changed()

    def geometry_table_changed(self):
        self.section = self.get_geometry()            # Load geometry data
        self.update_rho_tooltips()                    # update tooltips after get_geometry have checked the inputs
        self.graphicsViewGeometry.plot(self.section)  # update plot
        self.Res = None
        self.graphicsViewResults.plot(self.Res)

    def update_rho_tooltips(self):
        table = self.geometry_table
        table.blockSignals(True)
        for row in range(table.rowCount()):
            T = float(table.item(row, 2).text())
            for col in range(3, 5):
                rho = float(table.item(row, col).text())
                table.item(row, col).setToolTip(f'{rho*T*10**3} mm2/m')
        table.blockSignals(False)

    def get_SF(self):
        table = self.SectionForces_tableWidget
        row_values = table.get_table_row(0, replace_invalid=False)  # avoid replacing URs
        N, My, Mz, Vy, Vz, T = row_values[:6]

        # Dump into SectionForces class
        SF = SectionForces(N, My, Mz, Vy, Vz, T)
        return SF

    def set_SF_table(self, SF):
        table = self.SectionForces_tableWidget
        # table.removeRow(0)       # The row header "LC" is lost if the row is removed/inserted
        # table.insertRow(0)
        N, My, Mz, Vy, Vz, T = SF.N, SF.My, SF.Mz, SF.Vy, SF.Vz, SF.T
        for col, value in enumerate([N, My, Mz, Vy, Vz, T]):
            # table.setItem(0, col, QtWidgets.QTableWidgetItem(str(value)))  # set item to row below
            table.setItem(0, col, QtWidgets.QTableWidgetItem('{:.6g}'.format(value)))  # set item to row below
        self.SF_table_changed()

    def SF_table_changed(self):
        self.SF = self.get_SF()
        # clear result plot
        self.Res = None
        self.graphicsViewResults.plot(self.Res)

        # clear UR
        for col in [6, 7]:
            self.SectionForces_tableWidget.set_cell_value(0, col, "")

    def material_changed(self, signal_value):
        '''
        This method is executed when the material inputs are changed.
        Live update the plots when positive floats are provided
        '''
        try:
            value = float(signal_value)   # convert item text to float
            if value > 0:
                self.mat = self.get_material()
                self.material_plot()
        except Exception as e:
            pass

        # reset results and result plot
        self.Res = None
        self.graphicsViewResults.plot(self.Res)

    def material_editingFinished(self):
        '''
        This method is executed when a material input is finished editing.
        Thorough check of all material inputs + resets invalid inputs
        '''
        # getting the ext inputs or overwriting bad content
        string_list = ['f_ck', 'E_cm', 'f_yk', 'E_s',
                       'alpha_cc', 'gamma_c', 'gamma_s']

        # get e.g. obj = self.lineEdit_f_ck
        obj_list = [getattr(self, 'lineEdit_' + s) for s in string_list]

        # changing focus to another tracked input yields double exec
        # All objects are therefore initially blocked
        for obj in obj_list:
            obj.blockSignals(True)

        for obj, string in zip(obj_list, string_list):
            try:
                value = float(obj.text())   # convert item text to float
                if value <= 0:
                    raise ValueError
                # setattr(Mat, string, value)  # Send input value to class
            except Exception as e:
                self.show_msg_box(['Material input error',
                                   f'Input value "{obj.text()}" for {string} is not valid. {string} returned to default value.'])
                mat_default = Material.MatProp()
                value = getattr(mat_default, string)  # Get default value from material class
                obj.setText(str(value))  # Replace bad item content

        for obj in obj_list:
            obj.blockSignals(False)

        # update material instance and plot
        self.mat = self.get_material()
        self.material_plot()  # plot default value

    def get_material(self):
        '''
        Build material instance from material input cells
        '''
        # initiate material instance
        Mat = Material.MatProp()

        # getting the ext inputs or overwriting bad content     <-- OVERWRITES SHOULD HAPPEN ON CHANGED-SIGNAL
        obj_list = ['f_ck', 'E_cm', 'f_yk', 'E_s',
                    'alpha_cc', 'gamma_c', 'gamma_s']
        for string in obj_list:
            # get e.g. obj = self.lineEdit_f_ck
            obj = getattr(self, 'lineEdit_' + string)
            value = float(obj.text())   # convert item text to float
            setattr(Mat, string, value)  # Send input value to class  <-- should use setter-method

        Mat.update_strengths()  # need to update as f_ck attribute could have been changed

        # set combobox selections (must be after strength update as it updates the stiffnesses)
        conc_method = self.comboBox_concrete.currentText()
        reinf_method = self.comboBox_reinf.currentText()
        Mat.set_methods(conc_method, reinf_method)
        # Mat.set_nu_method = self.comboBox_nu.currentText()

        # check if stiffness is assignable and update window accordingly
        assignable, E_cm = Mat.is_conc_stiffness_assignable()
        if not assignable:
            self.lineEdit_E_cm.setDisabled(True)
            # self.stored_E_cm = self.lineEdit_E_cm.text()
            self.lineEdit_E_cm.setText(str(round(E_cm, 4)))
        elif not self.lineEdit_E_cm.isEnabled():
            E_cm = Material.MatProp.E_cm  # load class default E_cm
            Mat.E_cm = E_cm
            self.lineEdit_E_cm.setText(str(E_cm))
            self.lineEdit_E_cm.setDisabled(False)

        return Mat

    def set_material(self, Mat):
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

    def material_plot(self):
        # generate plot series
        seriesC = QtCharts.QtCharts.QLineSeries()
        seriesR = QtCharts.QtCharts.QLineSeries()
        for strain in np.linspace(-0.0035, 0.003, num=200):
            seriesC.append(strain, self.mat.concreteStress(strain))
            seriesR.append(strain, self.mat.reinforcementStress(strain))

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
        viewC = self.graphicsViewConcrete       # define view from gui widget
        viewR = self.graphicsViewReinforcement  # define view from gui widget
        chartViewC = QtCharts.QtCharts.QChartView(self.chartC, viewC)  # graphicsView -> chartView
        chartViewR = QtCharts.QtCharts.QChartView(self.chartR, viewR)  # graphicsView -> chartView
        chartViewC.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.white))
        chartViewR.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.white))
        chartViewC.setRenderHint(QtGui.QPainter.Antialiasing)
        chartViewR.setRenderHint(QtGui.QPainter.Antialiasing)
        chartViewC.show()  # cannot get the chart to fit without this
        chartViewR.show()  # cannot get the chart to fit without this
        # chartView.fitInView(self.chart.Geometry(), QtCore.Qt.KeepAspectRatio)

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
                msg_info_str = f'There is a newer release ({latest_tag}) from {published} available for download at https://github.com/Kleissl/HollowRC/releases/latest'
            print(msg_str)
            self.show_msg_box([msg_str, msg_info_str], title='Information')
        else:
            print('Github API requests returned statuscode', r.status_code)
