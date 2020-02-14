import math
from PySide2 import QtGui, QtWidgets, QtCore, QtCharts  # Import the Qt modules we'll need


class MyGraphicsView(QtWidgets.QGraphicsView):
    '''
    Custom QGraphicsView used as abstract base class for the MyGeometryView and MyResultView.
    This is an extension of QGraphicsView that incorporated some of the shared features of the graphics views.
    This also ensures to fit the scene rectangle of the scene into the view when the view is resized (fitInView).
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup graphics scene
        self.scene = QtWidgets.QGraphicsScene()     # creates a scene
        self.setScene(self.scene)                   # set the created scene

    def clear_scene(self):
        # self.scene.clear()                     # clear scene throws an RuntimeError: Internal C++ object (MyEllipse) already deleted
        self._old_scene = self.scene             # RuntimeError is avoided by keeping the old scene instance alive
        self.scene = QtWidgets.QGraphicsScene()  # creates a new scene instance
        self.setScene(self.scene)                # set the created scene

    def resizeEvent(self, event):
        """
        Extend the resizeEvent method so it now also calls fitInView.
        fitInView fits the scene rectangle into the view without distorting the scene proportions
        """
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)


class MyGeometryView(MyGraphicsView):
    '''
    Custom MyGraphicsView class for the geometry graphics view
    '''

    # Signals
    new_section = QtCore.Signal(object)  # prepare "new_section" signal
    scene_clicked = QtCore.Signal(object)  # prepare "scene_clicked" signal

    def update_section(self, signal_value):  # signal receiver
        dx, dy, wall_id = signal_value
        X = self.section.get_X()
        Y = self.section.get_Y()
        X[wall_id] += dx
        Y[wall_id] -= dy
        self.section.set_XY(X, Y)                # update current section instance with the new coordinates
        self.new_section.emit(self.section)      # emit new_section signal for the window class to catch

    def plot(self, section):
        self.section = section
        self.refresh_plot()

    def refresh_plot(self):
        self.clear_scene()

        # unpack geometry properties
        X = self.section.get_X()
        Y = self.section.get_Y()
        T = self.section.get_thick()
        centreX, centreY = self.section.get_centre()
        wallAngles = self.section.get_angles()

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
        shade_rects = []
        centre_lines = []
        node_circles = []
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
            PX1 = X1 + T[i] / 2 * math.sin(-wallAngles[i])
            PY1 = Y1 + T[i] / 2 * math.cos(-wallAngles[i])
            PX2 = X1 - T[i] / 2 * math.sin(-wallAngles[i])
            PY2 = Y1 - T[i] / 2 * math.cos(-wallAngles[i])
            PX3 = X2 - T[i] / 2 * math.sin(-wallAngles[i])
            PY3 = Y2 - T[i] / 2 * math.cos(-wallAngles[i])
            PX4 = X2 + T[i] / 2 * math.sin(-wallAngles[i])
            PY4 = Y2 + T[i] / 2 * math.cos(-wallAngles[i])
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
            # circle = QtWidgets.QGraphicsEllipseItem(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0)
            # circle = MyEllipse(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0, self, self.section, i)
            circle = MyEllipse(X1 - radi, -(Y1 + radi), radi * 2.0, radi * 2.0)
            circle.setAcceptHoverEvents(True)
            circle.set_wall_id(i)

            circle.setPen(thin_pencil)
            circle.setBrush(blue_fill)
            circle.node_moved.connect(self.update_section)  # call update_section method if a node_moved signal is received
            # circle.setZValue(10)  # higher Z values will always be drawn on top of lower Z values
            node_circles.append(circle)

            # preb. node texts
            point = QtCore.QPointF(X1, -Y1)
            text = QtWidgets.QGraphicsTextItem()
            text.setPos(point)
            text.setFont(font)
            text.setPlainText("Node " + str(i+1))
            # text.setZValue(8)  # higher Z values will always be drawn on top of lower Z values
            node_texts.append(text)

        # plot the shaded rectangles
        for rect in shade_rects:
            self.scene.addPolygon(rect, pen=no_pencil, brush=grey_fill)

        # plot centre lines
        for line in centre_lines:
            self.scene.addLine(line, bold_pencil)

        # plot node circles
        for circle in node_circles:
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
        self.scene.mousePressEvent = self.scene_mousePressEvent  # overrule QGraphicsSceneEvent
        # unblock scene change signals again
        # scene.blockSignals(False)

    def scene_mousePressEvent(self, event):  # when user clicks on result the values are listed in the status line
        # include custom signal containing coordinates
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.scene_clicked.emit({'x': round(x), 'y': round(y)})  # emit scene_clicked signal
        return QtWidgets.QGraphicsScene.mousePressEvent(self.scene, event)


class MyEllipse(QtWidgets.QGraphicsEllipseItem, QtCore.QObject):
    """
    Takes a QtWidgets.QGraphicsEllipseItem and adds signals for dragging the object around.
    Usage:
    item = MyEllipse(x, y, w, h)
    item.setPen(pen)
    item.setBrush(brush)
    self.scene().addItem(item)
    """
    node_moved = QtCore.Signal(object)  # prepare "node_moved" signal
    wall_id = None

    def __init__(self, *args, **kwargs):
        """
        By default QGraphicsItems are not movable and also do not emit signals when the position is changed for
        performance reasons. We need to turn this on.
        """
        QtWidgets.QGraphicsEllipseItem.__init__(self, *args, **kwargs)
        QtCore.QObject.__init__(self)  # the QQbject is for the signal
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable)
        # self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def set_wall_id(self, wall_id):
        self.wall_id = wall_id

    # def itemChange(self, change, value):
    # """
    # Catch all item position changes and emit the changed signal with the value (which will be the position).
    # :param change:
    # :param value:
    # """
    #     if change == QtWidgets.QGraphicsItem.ItemPositionChange:
    #         # value is the new position.
    #         print("item's scene position changed: ", value)
    #         # print(value)
    #         # self.node_moved.emit(value)  # emit "changed" signal
    #     return QtWidgets.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        # super().mousePressEvent(event)
        self.setCursor(QtCore.Qt.ClosedHandCursor)  # update cursor
        self.x0 = event.scenePos().x()
        self.y0 = event.scenePos().y()
        return QtWidgets.QGraphicsEllipseItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)  # update cursor
        x1 = event.scenePos().x()
        y1 = event.scenePos().y()
        dx = round(x1 - self.x0)
        dy = round(y1 - self.y0)
        self.node_moved.emit([dx, dy, self.wall_id])  # emit node_moved signal
        return QtWidgets.QGraphicsEllipseItem.mouseReleaseEvent(self, event)  # important for error handling!


# New Classes for my plot scenes
class MyResultView(MyGraphicsView):
    """
    Custom MyGraphicsView class for the result graphics view
    """

    status_str = QtCore.Signal(object)  # prepare "status_str" signal
    Res = None

    def __init__(self, *args, **kwargs):

        QtWidgets.QGraphicsView.__init__(self, *args, **kwargs)

        # setup graphics scene
        self.scene = QtWidgets.QGraphicsScene()     # creates a scene
        self.setScene(self.scene)                   # set the created scene

    def show_result_values(self, signal_value):  # signal receiver
        pass

    def set_check_boxes(self, checkbox_list):
        self.check_boxes = checkbox_list

    def plot(self, Res):
        self.Res = Res
        self.refresh_plot()

    def refresh_plot(self):
        self.clear_scene()

        # check for empty result
        if not self.Res:
            return

        # unpack results dictionary
        x = self.Res.x
        y = self.Res.y
        wallAngles = self.Res.wallAngles

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

        for j in range(self.Res.plot_count):  # looping over the different result distributions
            # select styles
            pencil = QtGui.QPen(colour_list[j])  # create pen with next colour
            fill = QtGui.QBrush(colour_list[j])  # create brush with same colour
            pencil.setWidth(10)

            check_box = self.check_boxes[j]
            # check_box = getattr(self, 'checkBox_plot' + str(j+1))

            # update checkbox visibility
            if not check_box.isVisible():
                check_box.setVisible(True)
            check_box.setText(self.Res.plot_names[j])
            check_box.setStyleSheet("color: " + colour_list[j].name.decode())

            # plot if checked
            if check_box.isChecked():
                scale = self.Res.plot_scale[j] * section_dim / max(1e-12, max(abs(self.Res.plot_data[j])))
                rect = QtGui.QPolygonF()  # outline polygon
                for i in range(len(self.Res.x)):
                    PX = self.Res.x[i] + scale * self.Res.plot_data[j][i] * math.sin(-wallAngles[i])
                    PY = self.Res.y[i] + scale * self.Res.plot_data[j][i] * math.cos(-wallAngles[i])
                    if self.Res.x[i] == self.Res.x[i - 1] and self.Res.y[i] == self.Res.y[i - 1]:  # new wall element started
                        rect.append(QtCore.QPointF(self.Res.x[i], -self.Res.y[i]))  # add plot point at geometric corner
                        # prepare/plot shading
                        if i > 0:
                            # plot shading
                            rect2.append(QtCore.QPointF(self.Res.x[i], -self.Res.y[i]))  # add plot point at geometric corner
                            poly_item = QtWidgets.QGraphicsPolygonItem(rect2)
                            poly_item.setBrush(fill)
                            poly_item.setOpacity(0.2)
                            self.scene.addItem(poly_item)
                            # self.scene.addPolygon(rect2, brush=fill)

                        rect2 = QtGui.QPolygonF()  # shading polygon
                        rect2.append(QtCore.QPointF(self.Res.x[i], -self.Res.y[i]))  # add plot point at geometric corner
                        rect2.append(QtCore.QPointF(PX, -PY))
                    else:
                        # add point for shading polygon
                        rect2.append(QtCore.QPointF(PX, -PY))
                    rect.append(QtCore.QPointF(PX, -PY))

                    # prepare line for mouse clicks
                    line = QtCore.QLineF(PX, -PY, self.Res.x[i], -self.Res.y[i])  # x pos. right, y pos. down
                    # line_item = QtWidgets.QGraphicsLineItem(line)
                    line_item = myLine(line)
                    line_item.setPen(pencil)
                    line_item.set_data_str('{}: {:.2f} {}'.format(self.Res.plot_names[j], self.Res.plot_data[j][i], self.Res.plot_units[j]))  # string for click ev.
                    line_item.setAcceptHoverEvents(True)
                    self.scene.addItem(line_item)

                # plot shading
                rect2.append(QtCore.QPointF(self.Res.x[i], -self.Res.y[i]))  # add plot point at geometric corner
                poly_item = QtWidgets.QGraphicsPolygonItem(rect2)
                poly_item.setBrush(fill)
                poly_item.setOpacity(0.2)
                self.scene.addItem(poly_item)
                # plot result outline
                self.scene.addPolygon(rect, pen=pencil)

        # Hide the remaining unneeded check boxes
        for j in range(self.Res.plot_count, 10):
            # check_box = getattr(self, 'checkBox_plot' + str(j + 1))
            check_box = self.check_boxes[j]
            check_box.setVisible(False)

        # Fit plottet items in view
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        # ui->graphicsView->fitInView(_scene->itemsBoundingRect(),Qt::KeepAspectRatio);   # consider changing to itemsBoundingRect when sceneRect not updating!!
        self.scene.mousePressEvent = self.scene_mousePressEvent  # overrule QGraphicsSceneEvent

    def scene_mousePressEvent(self, event):  # when user clicks on result the values are listed in the status line
        # x = event.scenePos().x()
        # y = event.scenePos().y()
        # print('scene press event (x,y) = ({}, {})'.format(x, y))
        # print('view rect ', view.rect())
        # print('view-scene rect ', view.sceneRect())
        # print('scene panel rect ', self.scene.mousePressEvent())
        # print('onItemClick')
        items_clicked = self.scene.items(event.scenePos())
        msg = 'Point data: '
        for item in items_clicked:
            if hasattr(item, 'data_str'):
                msg += "{}, ".format(item.data_str)
        if len(msg) > 13:
            # self.statusbar.showMessage(msg[:-2])
            self.status_str.emit(msg[:-2])  # emit status_str signal
            print(msg[:-2])
        return QtWidgets.QGraphicsScene.mousePressEvent(self.scene, event)

# # # Creating my own line item class so I can overwrite its mousePressEvent
# # line_item = QtWidgets.QGraphicsLineItem(line)


class myLine(QtWidgets.QGraphicsLineItem):
    '''
    A customized QGraphicsLineItem that reimplements the hovering events so
    '''
    def set_data_str(self, string):
        self.data_str = string
        self.setToolTip(string)

    def hoverEnterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)  # update cursor
        pen = self.pen()
        self.original_width = pen.width()
        pen.setWidth(20)
        self.setPen(pen)
        return QtWidgets.QGraphicsLineItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        pen = self.pen()
        pen.setWidth(self.original_width)
        self.setPen(pen)
        return QtWidgets.QGraphicsLineItem.hoverLeaveEvent(self, event)
