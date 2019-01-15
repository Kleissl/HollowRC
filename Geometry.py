# -*- coding: utf-8 -*-
"""
Class definitions for geometry properties

History log:
Version 0.1 - first working build

Author: Kenneth C. Kleissl
"""
import math
import numpy as np


class CrossSection:
    """
    A container for the cross section properties

    Attributes:
        ...
    """
    # Class variables defaults
    instance_count = 0

    @classmethod
    def count_instances(cls):
        cls.instance_count += 1

    @classmethod
    def get_instance_count(cls):
        return cls.instance_count

    def __init__(self):
        # Instance variables
        self.walls = []  # list of wall instances

        # Class variables

        # Class methods
        self.count_instances()

    def add_wall(self, wall):
        self.walls.append(wall)

    def set_wallNodeN(self, wallNodeN):
        for wall in self.walls:
            wall.wallNodeN = wallNodeN

    def get_X(self):
        X = []
        for wall in self.walls:
            X.append(wall.X[0])
        return X

    def get_Y(self):
        Y = []
        for wall in self.walls:
            Y.append(wall.Y[0])
        return Y

    def get_dX(self):
        dX = []
        for wall in self.walls:
            dX.append(wall.dX)
        return dX

    def get_dY(self):
        dY = []
        for wall in self.walls:
            dY.append(wall.dY)
        return dY

    def get_wallLength(self):
        wallLength = []
        for wall in self.walls:
            wallLength.append(wall.length)
        return wallLength

    def get_thick(self):
        thick = []
        for wall in self.walls:
            thick.append(wall.thick)
        return thick

    def get_rho_long(self):
        rho_long = []
        for wall in self.walls:
            rho_long.append(wall.rho_long)
        return rho_long

    def get_angle(self, local_data=False):
        angle = []
        for wall in self.walls:
            angle.append(wall.angle)
        if local_data:
            return np.repeat(angle, self.walls[0].wallNodeN)
        else:
            return angle

    def get_centre(self):
        wallArea = []
        wallSx = []
        wallSy = []
        for wall in self.walls:
            wallArea.append(wall.area)
            wallSx.append(wall.Sx)
            wallSy.append(wall.Sy)

        # Sum wall contributions
        Area = sum(wallArea)
        Sx = sum(wallSx)
        Sy = sum(wallSy)

        # Concrete centre (Center of gravity is used as SF reference point)
        centreX = Sy / Area
        centreY = Sx / Area
        return [centreX, centreY]

    def get_enclosed_area(self):
        enclosed_area = []
        for wall in self.walls:
            enclosed_area.append(wall.enclosed_area)
        # Sum wall contributions
        return sum(enclosed_area)

    def get_e(self, local_data=False):
        e = []
        for wall in self.walls:
            # pointLineDistance
            centreX, centreY = self.get_centre()
            e.append(self.point_line_dist(centreX, centreY, wall.X[0], wall.Y[0], wall.X[1], wall.Y[1]))
        if local_data:
            return np.repeat(e, self.walls[0].wallNodeN)
        else:
            return e

    # Second Moment of Area
    #Ix.append(wallLength[i]*T[i]/12 * ( wallLength[i]**2 * math.cos(wallAngle[i])**2 + T[i]**2 * math.sin(wallAngle[i])**2 ))
    #Ix.append(wallLength[i] * T[i] / 12 * (
    #            T[i] ** 2 * math.cos(wallAngle[i]) ** 2 + wallLength[i] ** 2 * math.sin(wallAngle[i]) ** 2)) + wallArea[i] *

    @staticmethod
    def point_line_dist(x0, y0, x1, y1, x2, y2):
        # The perpendicular distance from a point to a line (defined by two points)
        # point defined by (x0, y0)
        # line defined from (x1, y1) to (x2, y2)

        # check if (x1, y1) and (x2, y2) is coinciding
        if x1 == x2 and y1 == y2:
            distance = 0
        else:
            distance = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        # print("point defined by (x0, y0) =", x0, y0)
        # print(" line defined from (x1, y1) =", x1, y1, "to (x2, y2) =", x2, y2)
        # print(distance)
        return distance


class Wall:
    """
    A container for wall segment/element properties

    Attributes:
        ...
    """
    # Class variables defaults
    wallNodeN = 25  # number of nodes per wall

    def __init__(self, X, Y, thick, rho_long, rho_trans):
        self.X = X
        self.Y = Y
        self.thick = thick
        self.rho_long = rho_long
        self.rho_trans = rho_trans

        # variables calculated during initiation
        self.dX = X[1] - X[0]
        self.dY = Y[1] - Y[0]
        self.length = math.sqrt(self.dX**2 + self.dY**2)
        self.ds = self.length / (self.wallNodeN - 1)
        self.angle = math.atan2(self.dY, self.dX)  # in radians
        self.area = self.length * thick
        self.midX = (X[0] + X[1]) / 2  # wall mid point
        self.midY = (Y[0] + Y[1]) / 2
        self.Sx = self.midY * self.area  # 1st moment of area
        self.Sy = self.midX * self.area  # 1st moment of area
        self.enclosed_area = 0.5 * (X[0] * Y[1] - X[1] * Y[0]) / 1000000  # enclosed area

    def integrate_dist(self, dist):
        # # define weights/eff. length for each node
        # ds_list = [0.5 * self.ds if i in (0, self.wallNodeN - 1) else self.ds for i in range(self.wallNodeN)]
        # # Integrate distribution
        # integration = sum(ds_list * np.array(dist))
        if not self.wallNodeN == len(dist):
            print('warning: dist to be integrated does not have the expected size!')
        # Integrate distribution
        integration = sum([0.5 * self.ds * dist[i] if i in (0, self.wallNodeN - 1) else self.ds * dist[i] for i, value in enumerate(dist)])
        return integration

# For when this script is excetuted on its own
if __name__ == '__main__':
    thick = 200
    rho_long = 0.02
    rho_trans = 0.01

    section = CrossSection()
    wall_1 = Wall([1, 2], [1, 2], thick, rho_long, rho_trans)
    wall_2 = Wall([1, 2], [1, 2], thick, rho_long, rho_trans)
    wall_3 = Wall([1, 2], [1, 2], thick, rho_long, rho_trans)

    section.add_wall(wall_1)
    section.add_wall(wall_2)
    section.add_wall(wall_3)

    print('number of sections = ', section.get_instance_count())
    print('number of walls in section = ', len(section.walls))

    print('section centre: ', section.get_centre())
