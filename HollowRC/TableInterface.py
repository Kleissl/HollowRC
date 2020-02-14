'''
New Class for QT tables adding useful methods
'''
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtCore import Signal


class MyTable(QTableWidget):

    status_msg = Signal(object)  # prepare "status_msg" signal
    error_msg = Signal(object)   # prepare "error_msg" signal
    awaits_click = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_row(self):
        self.blockSignals(True)
        row_count = self.rowCount()         # get number of rows
        self.insertRow(row_count)           # insert new row at the end

        # fill new row with items
        col_count = self.columnCount()      # get number of columns
        for col in range(2):  # loop over columns
            item = QTableWidgetItem('click')
            item.setToolTip('Click on geometry plot to load coordinates')
            self.setItem(row_count, col, item)  # set item to row below

        # copy values from previous row
        row_values = self.get_table_row(row_count - 1)  # get values from previous/above row
        for col in range(2, col_count):  # loop over non-coordinates columns
            value = row_values[col]
            item = QTableWidgetItem('{:.6g}'.format(value))
            self.setItem(row_count, col, item)  # set item to row below

        self.blockSignals(False)
        self.awaits_click = True  # will allow for scene_clicked signals
        self.status_msg.emit('Recent action: row added - Click on geometry plot to load coordinates into the newly added row')  # emit status_msg signal

    def remove_row(self):
        self.blockSignals(True)
        select_row = self.currentRow()  # get selected row
        if select_row == -1:
            self.statusbar.showMessage('Error: no row selected')
            return
        self.removeRow(select_row)  # remove current row

        self.blockSignals(False)
        self.itemChanged.emit(QTableWidgetItem())
        self.status_msg.emit('Recent action: row removed')  # emit status_msg signal

    def move_row_up(self):
        select_row = self.currentRow()  # get selected row
        if select_row == 0:
            self.status_msg.emit('Error: cannot move first row up')  # emit status_msg signal
        elif select_row == -1:
            self.status_msg.emit('Error: no row selected')  # emit status_msg signal
        else:
            self.blockSignals(True)
            self.insertRow(select_row + 1)  # insert new row below selected row
            col_count = self.columnCount()  # get number of columns

            for col in range(col_count):                                # loop over columns
                moving_item = self.takeItem(select_row - 1, col)  # take item from row above
                self.setItem(select_row + 1, col, moving_item)    # set item to row below

            self.removeRow(select_row - 1)      # remove original row
            self.blockSignals(False)
            self.itemChanged.emit(QTableWidgetItem())
            self.status_msg.emit('Recent action: row moved up')  # emit status_msg signal

    def move_row_down(self):
        ''' Move selected row down '''
        select_row = self.currentRow()      # get selected row
        row_count = self.rowCount()         # get number of rows
        if select_row == row_count - 1:     # check if last row
            self.status_msg.emit('Error: cannot move last row down')  # emit status_msg signal
        elif select_row == -1:
            self.status_msg.emit('Error: no row selected')  # emit status_msg signal
        else:
            self.blockSignals(True)
            self.insertRow(select_row)      # insert new row above selected row
            select_row += 1
            col_count = self.columnCount()  # get number of columns

            for col in range(col_count):                                # loop over columns
                moving_item = self.takeItem(select_row + 1, col)  # take item from row below
                self.setItem(select_row - 1, col, moving_item)    # set item to row above

            self.removeRow(select_row + 1)      # remove original row
            self.blockSignals(False)
            self.itemChanged.emit(QTableWidgetItem())
            self.status_msg.emit('Recent action: row moved down')  # emit status_msg signal

    def get_table_row(self, row, replace_invalid=True):
        ''' Extract values from a specified row id '''
        self.awaits_click = False  # properly triggered by manual change in geometry table thus no longer awaits node_coords_by_click
        col_count = self.columnCount()                         # get number of columns
        row_values = []
        for col in range(col_count):
            item = self.item(row, col)                         # Retrieve item from the cell
            if item:
                try:
                    row_values.append(float(item.text()))           # Add item text to list as float
                except ValueError:
                    if replace_invalid:
                        header = self.horizontalHeaderItem(col).text()
                        self.error_msg.emit(['Table input error',
                                            f'Input value "{item.text()}" for row index {row} in {header} column not valid. Value set to zero.'])
                        item.setText('0')                               # Replace bad item content
                        row_values.append(0.0)                          # Add zero to list
        return row_values

    def node_coords_by_click(self, signal_value):
        if self.awaits_click:
            self.awaits_click = False  # stop more click signals from being send
            x = signal_value['x']
            y = signal_value['y']
            self.blockSignals(True)           # block signals
            row_index = self.rowCount() - 1   # get index of last row
            x_item = self.item(row_index, 0)  # Retrieve item from the cell
            x_item.setText(str(x))             # Replace bad item content
            y_item = self.item(row_index, 1)
            y_item.setText(str(-y))            # Replace bad item content
            self.blockSignals(False)
            self.itemChanged.emit(QTableWidgetItem())

    def set_cell_value(self, row, col, value, flag=None, background=False):
        ''' Assign a value to a specified cell '''
        item = self.item(row, col)
        if item:
            # only edit text such that properties like ItemIsEnabled is maintained
            item.setText(str(value))
        else:
            item = QTableWidgetItem(str(value))
            self.setItem(row, col, item)
        if flag:
            item.setFlags(flag)
        if background:
            item.setBackground(background)
