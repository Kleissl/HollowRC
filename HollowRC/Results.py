# -*- coding: utf-8 -*-
"""
Class definition of a container for material properties

Author: Kenneth C. Kleissl
"""


class Results:
    """
    A container for results

    Attributes:
        ...
    """

    def __init__(self, x, y, wallAngles):
        # Instance variables
        self.x = x
        self.y = y
        self.wallAngles = wallAngles

        self.plot_count = 0
        self.plot_data = []
        self.plot_names = []
        self.plot_units = []
        self.plot_scale = []

        self.info_msg = None
        self.load_factors = {'bending': None, 'shear': None}

    def add_plot(self, data, name=None, unit='', scale=0.10):
        if self.plot_count == 10:
            print('Plot not added. Maximum 10 results plots supported')
        else:
            self.plot_data.append(data)
            self.plot_names.append(name)
            self.plot_units.append(unit)
            self.plot_scale.append(scale)
            self.plot_count += 1

    def clear_plot_data(self):
        self.plot_count = 0
        self.plot_data = []
        self.plot_names = []
        self.plot_units = []
        self.plot_scale = []


# For when this script is excetuted on its own
if __name__ == '__main__':

    Res = Results(0, 0, 0)
    print(Res)
