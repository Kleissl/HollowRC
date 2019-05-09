# -*- coding: utf-8 -*-
"""
Main executable for the "Hollow section analysis tool" GUI 

This code execute the GUI application ...

History log:
Version 0.1 - first working build based on UI from Qt Designer
Version 0.2 - moved MainWindow class into separate file
Version 0.3 - Now compatible with Python3 & PyQt5

Author: Kenneth C. Kleissl
"""
# Standard library modules
import sys  # We need sys so that we can pass argv to QApplication
# Third-party library modules
from PySide2 import QtWidgets, QtGui
# Local source tree modules
from HollowWindow import HollowWindow  # import the MainWindow class


def main():
    # Create an instance of QApplication (Qt's application object).
    app = QtWidgets.QApplication(sys.argv)

    # Splash screen
    pixmap = QtGui.QPixmap(":/Icons/resources/Icon.png")
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()  
    app.processEvents()

    # The QWidget widget is the base class of all user interface objects in Qt.
    window = HollowWindow()  # We set the form to be our ExampleApp (design)
    window.show()  # Show the window/form

    # Finished starting up the application, so hide the splash icon
    splash.finish(window)

    # Exception handling
    sys.excepthook = my_exception_hook      # overwrite the sys exception hook with custom wrapping function

    # Execute app
    sys.exit(app.exec_())

# example of better excepthook:
# https://stackoverflow.com/questions/45787237/exception-handled-surprisingly-in-pyside-slots
def my_exception_hook(type_, value, traceback_):   # if QtCore.QT_VERSION >= 0x50501:
    # Print the error and traceback
    print(type_, value, traceback_)

    # window.indicate_fail(type, value)

    # Call the default exception hook
    sys.__excepthook__(type_, value, traceback_)  # no need to save original excepthook as __excepthook__ contains it
    sys.exit(1)  # Exit Python by raising the SystemExit exception with nonzero exit status


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

# example with a QDialog being passed into the MainWindow class:
# http://projects.skylogic.ca/blog/how-to-install-pyqt5-and-build-your-first-gui-in-python-3-4/
