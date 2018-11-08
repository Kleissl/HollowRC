# -*- coding: utf-8 -*-
"""
Class definition of a container for sectional forces

History log:
Version 0.1 - first working build

Author: Kenneth C. Kleissl (KEKL)
Last edited: May 2018
"""


class SectionForces:
    """
    A container for sectional forces by Kenneth C. Kleissl.

    Attributes:
        N:  Normal force (neg. = compression)
        Mx: Bending moment about the x-axis
        My: Bending moment about the y-axis
        Vx: Shear force in the x-axis
        Vy: Shear force in the y-axis
        T:  Torsional moment
    """
    # Class variables
    count = 0
    load_factor = 1.0
    fac_bending = load_factor
    fac_shear = load_factor

    def __init__(self, N, Mx, My, Vx=None, Vy=None, T=None):
        # Instance variables
        self.N = N * self.fac_bending
        self.Mx = Mx * self.fac_bending
        self.My = My * self.fac_bending

        if Vx:
            self.Vx = Vx * self.fac_shear
        else:
            self.Vx = Vx

        if Vy:
            self.Vy = Vy * self.fac_shear
        else:
            self.Vy = Vy

        if T:
            self.T = T * self.fac_shear
        else:
            self.T = T

        SectionForces.count += 1

    def set_load_factor(self, fac):
        self.load_factor = fac

    def print_str(self):
        string = 'N=' + str(self.N) + ', Mx=' + str(self.Mx) + ', My=' + str(self.My) \
                 + ', Vx=' + str(self.Vx) + ', Vy=' + str(self.Vy) + ', T=' + str(self.T)
        return string


# For when this script is excetuted on its own
if __name__ == '__main__':
    N = -20000
    Mx = 60000
    My = -10000
    Vx = 0
    Vy = 2000
    T = 0
    SF = SectionForces(N, Mx, My, Vx, Vy, T)
    print(SF.My)

