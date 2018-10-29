# New Class for QT tables adding useful methods
class TableInterface(object):
    def __init__(self):
        # super(TableInterface, self).__init__()  # use super so we return parent object of this class
        super().__init__()  # initialize the QMainWindow parent object from the Qt Designer file
        # QMainWindow.__init__(self)
    #
    # def __init__(self, filename):
    #     self.file = open(filename)
    #
    # def __enter__(self):
    #     return self.file
    #
    # def __exit__(self, ctx_type, ctx_value, ctx_traceback):
    #     self.file.close()