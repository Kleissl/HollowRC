# -*- coding: utf-8 -*-
"""
Main executable for the "Hollow section analysis tool" GUI 

This code execute the GUI application ...

History log:
Version 0.1 - first working build based on UI from Qt Designer
Version 0.2 - moved MainWindow class into separate file
Version 0.3 - Now compatible with Python3 & PyQt5

Author: Kenneth C. Kleissl (KEKL)
Last edited: May 2018
"""
# Standard library modules
import sys  # We need sys so that we can pass argv to QApplication
# Third-party library modules
from PyQt5 import QtWidgets
# Local source tree modules
from MyMainWindow import MyMainWindow  # import the MainWindow class


def main():
    # Create a new instance of QApplication (PyQT5 application object).
    app = QtWidgets.QApplication(sys.argv)  # PyQT5 compatible

    # The QWidget widget is the base class of all user interface objects in PyQt4.
    window = MyMainWindow()  # We set the form to be our ExampleApp (design)
    window.show()  # Show the window/form

    # Exception handling
    sys.excepthook = my_exception_hook      # overwrite the sys exception hook with custom wrapping function

    # Execute app
    sys.exit(app.exec_())


def my_exception_hook(type_, value, traceback_):   # if QtCore.QT_VERSION >= 0x50501:
    # Print the error and traceback
    print(type_, value, traceback_)

    # window.indicate_fail(type, value)

    # Call the default exception hook
    sys.__excepthook__(type_, value, traceback_)  # no need to save original excepthook as __excepthook__ contains it
    sys.exit(1)


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

# example with a QDialog being passed into the MainWindow class
# http://projects.skylogic.ca/blog/how-to-install-pyqt5-and-build-your-first-gui-in-python-3-4/
