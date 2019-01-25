import math
from PySide2 import QtGui, QtWidgets, QtCore, QtCharts  # Import the Qt modules we'll need

# New Classes for my plot scenes
class MyGeometryView(QtWidgets.QGraphicsView, QtCore.QObject):
    # def __init__(self):
    #     # super(TableInterface, self).__init__()  # use super so we return parent object of this class
    #     super().__init__()  # initialize the QMainWindow parent object from the Qt Designer file
        # QMainWindow.__init__(self)
    new_section = QtCore.Signal(object)  # prepare "new_section" signal

    def __init__(self, *args, **kwargs):
        """
        ...
        """
        QtWidgets.QGraphicsView.__init__(self, *args, **kwargs)
        # QtCore.QObject.__init__(self)  # the QQbject is for the signal            <---- RuntimeError: You can't initialize an object twice!

        # setup graphics scene
        self.scene = QtWidgets.QGraphicsScene()     # creates a scene
        self.setScene(self.scene)                   # set the created scene

    def clear_scene(self):
            self.scene.clear()                          # Clear scene
            # scene.clear()  # Clear
            # view.scene().disconnect()
            # view.close()

    def update_section(self, value): # signal function
        dx, dy, wall_id = value
        X = self.section.get_X()
        Y = self.section.get_Y()
        X[wall_id] += dx
        Y[wall_id] -= dy
        self.section.set_XY(X, Y)   
        # self.setGeometry(section)
        # print('Geometry set completed')
        # self.geometry_plot() # this will delete the MyEllipse instances
        # print('plot refresh completed')
        self.new_section.emit(self.section)  # emit new_section signal
        self.scene_backup = self.scene # have to store a copy of the scene to avoid RuntimeError: Internal C++ object (MyEllipse) already deleted.
        self.scene = QtWidgets.QGraphicsScene()     # creates a scene
        self.setScene(self.scene)                   # set the created scene
        self.plot_all(self.section)

    def plot_all(self, section):
        # original way of plotting all
        self.section = section
        self.clear_scene()

        try:
            # unpack geometry properties
            X = self.section.get_X()
            Y = self.section.get_Y()
            T = self.section.get_thick()
            centreX, centreY = self.section.get_centre()
            wallAngle = self.section.get_angle()
        except:
            print('Cannot read geometry')
            return

        # connect itemChange signal with method
        # scene.changed.connect(self.node_moved)
        # self.graphicsViewGeometry.scene().changed.connect(self.node_moved)
        # scene.blockSignals(True)
        # self.graphicsViewGeometry.blockSignals(True)

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
        self.shade_rects = []
        centre_lines = []
        self.node_circles = []
        # node_rects = []
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
            self.shade_rects.append(rect)

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
            # circle = QtWidgets.QGraphicsEllipseItem(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0)
            # circle = MyEllipse(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0, self, self.section, i)
            circle = MyEllipse(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0)
            circle.set_wall_id(i)
            
            circle.setPen(thin_pencil)
            circle.setBrush(blue_fill)
            circle.node_moved.connect(self.update_section)  # call update_section method if a node_moved signal is received
            self.node_circles.append(circle)

            # preb. node texts
            point = QtCore.QPointF(X1, -Y1)
            text = QtWidgets.QGraphicsTextItem()
            text.setPos(point)
            text.setPlainText("Node " + str(i+1))
            text.setFont(font)
            node_texts.append(text)

        # plot the shaded rectangles
        for rect in self.shade_rects:
            self.scene.addPolygon(rect, pen=no_pencil, brush=grey_fill)

        # plot centre lines
        for line in centre_lines:
            self.scene.addLine(line, bold_pencil)
        
        # plot node circles
        for circle in self.node_circles:
            self.scene.addItem(circle)

        # plot node texts
        for text in node_texts:
            self.scene.addItem(text)

        # plot centre text
        point = QtCore.QPointF(centreX, -centreY)
        text = QtWidgets.QGraphicsTextItem()
        text.setPlainText("CG")
        text.setFont(font)
        text.setPos(point)
        self.scene.addItem(text)

        # fit view to make sure that QGraphics view have no scrollbars
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        # unblock scene change signals again
        # scene.blockSignals(False)




    # use this to set the ZValue instead of dealing with plot sequence!
    # class GraphicsItemSet:
    #     """
    #     A set of QGraphicsItem elements.
    #     Some collective actions are possible like setting a Z-value to each of them.
    #     """
    
    #     def __init__(self):
    #         self._content = set()
    
    #     def add_item(self, item: QtWidgets.QGraphicsItem):
    #         """
    #         Adds an item to the content list. Should be
    
    #         :param item:
    #         """
    #         if not isinstance(item, QtWidgets.QGraphicsItem):
    #             raise RuntimeError('Expected instance of QGraphicsItem!')
    #         self._content.add(item)
    
    #     def set_zvalue(self, level):
    #         """
    #         Sets the z value of all items in the set.
    
    #         :param level:
    #         :return:
    #         """
    #         for item in self._content:
    #             item.setZValue(level)






 # Example with own signal emit from https://programtalk.com/vs2/python/13311/imperialism-remake/source/lib/qt.py/
    # def make_GraphicsItem_draggable(parent):
    #     """
    #     Takes a QtWidgets.QGraphicsItem and adds signals for dragging the object around. For this the item must have the
    #     ItemIsMovable and ItemSendsScenePositionChanges flags set. Only use it when really needed because there is
    #     some performance hit attached.
    #     """
    
    #     # noinspection PyPep8Naming
    #     class DraggableGraphicsItem(parent, QtCore.QObject):
    #         """
    #         Draggable GraphicsItem.
    #         """
    #         changed = QtCore.pyqtSignal(object)
    
    #         def __init__(self, *args, **kwargs):
    #             """
    #             By default QGraphicsItems are not movable and also do not emit signals when the position is changed for
    #             performance reasons. We need to turn this on.
    #             """
    #             parent.__init__(self, *args, **kwargs)
    #             self.parent = parent
    #             QtCore.QObject.__init__(self)
    
    #             self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
    
    #         def itemChange(self, change, value):
    #             """
    #             Catch all item position changes and emit the changed signal with the value (which will be the position).
    
    #             :param change:
    #             :param value:
    #             """
    #             if change == QtWidgets.QGraphicsItem.ItemPositionChange:
    #                 self.changed.emit(value)
    
    #             return parent.itemChange(self, change, value)
    
    #     return DraggableGraphicsItem

class MyEllipse(QtWidgets.QGraphicsEllipseItem, QtCore.QObject):
    """
    Takes a QtWidgets.QGraphicsEllipseItem and adds signals for dragging the object around.
    Usage:
    item = MyEllipse(x, y, w, h)
    item.setPen(pen)
    item.setBrush(brush)
    self.scene().addItem(item)
    """
    node_moved = QtCore.Signal(object)  # prepare "changed" signal
    wall_id = None

    # def __init__(self, parent=None):
    #     super(MyEllipse, self).__init__(parent)
    def __init__(self, *args, **kwargs):
        """
        By default QGraphicsItems are not movable and also do not emit signals when the position is changed for
        performance reasons. We need to turn this on.
        """
        QtWidgets.QGraphicsEllipseItem.__init__(self, *args, **kwargs)
        QtCore.QObject.__init__(self)  # the QQbject is for the signal
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        # self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        # self.setAcceptHoverEvents(True)

    def set_wall_id(self, wall_id):
        self.wall_id = wall_id

    # def itemChange(self, change, value):
    #     if change == QtWidgets.QGraphicsItem.ItemPositionChange: # && QtWidgets.QGraphicsScene():
    #         # value is the new position.
    #         print("item's scene position changed: ", value)
    #         # print(value)
    #         # self.node_moved.emit(value)  # emit "changed" signal
    #         # rect = QtWidgets.QGraphicsScene().sceneRect()
    #         # if not rect.contains(value):
    #         #     # Keep the item inside the scene rect.
    #         #     value.setX(qMin(rect.right(), qMax(value.x(), rect.left())))
    #         #     value.setY(qMin(rect.bottom(), qMax(value.y(), rect.top())))
    #         #     return value
    #     return QtWidgets.QGraphicsItem.itemChange(self, change, value)
    # def itemChange(self, change, value):
    #     """
    #     Catch all item position changes and emit the changed signal with the value (which will be the position).
    #     :param change:
    #     :param value:
    #     """
    #     if change == QtWidgets.QGraphicsItem.ItemPositionChange:
    #         print("item's scene position changed!")
    #         self.changed.emit(value)  # emit "changed" signal
    #     return super().itemChange(self, change, value)

    def mousePressEvent(self, event):
    #     super().mousePressEvent(event)
        # print('mousePressEvent')
        self.x0 = event.scenePos().x()
        self.y0 = event.scenePos().y()
    #     # print('item_mousePressEvent x,y= ', self.x0, self.y0)
        return QtWidgets.QGraphicsEllipseItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        # print('mouseReleaseEvent')
        x1 = event.scenePos().x()
        y1 = event.scenePos().y()
    #     # print('mouseReleaseEvent x,y= ', self.x1, self.y1)
        dx = round(x1 - self.x0)
        dy = round(y1 - self.y0)
    #     print('item moved dx,dy= ', self.dx, self.dy)
        self.node_moved.emit([dx, dy, self.wall_id])  # emit node_moved signal
        
        # self.myTimer = QtCore.QTimer() # instantiate a new timer and store a reference to it in 'myTimer'
        # self.myTimer.setInterval(1000) # set the delay to 1 second
        # self.myTimer.setSingleShot(True)
        # self.myTimer.timeout.connect(self.node_changed.emit([dx, dy, self.wall_id])) # once the timer runs out, run someOtherFunction
        # self.myTimer.start(1000) 
        return QtWidgets.QGraphicsEllipseItem.mouseReleaseEvent(self, event)  # important for error handling!

    # def hoverEnterEvent(self, event):
        # self.setCursor(Qt.OpenHandCursor)
        # show node number and coordinates at node while hovering
    
    # def hoverLeaveEvent(self, event):





class MyResultView(QtWidgets.QGraphicsView):
    pass



