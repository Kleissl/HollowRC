# -*- coding: utf-8 -*-
"""
Class definition of a container for material properties

History log:
Version 0.1 - first working build

Author: Kenneth C. Kleissl (KEKL)
Last edited: May 2018
"""


class MatProp:
    """
    A container for material properties by Kenneth C. Kleissl.

    Attributes:
        f_ck: Characteristic strength of concrete cylinder
        f_yk: Characteristic yield strength of reinforcement
        ...
    """
    # Class variables defaults
    # limit_state = 'ULS'
    f_ck = 45
    E_cm = 35
    f_yk = 500
    E_s = 210
    alpha_cc = 0.85
    gamma_c = 1.5
    gamma_s = 1.15
    conc_method = 'EN Parabolic-rectangular'
    reinf_method = 'Elastic-plastic'
    conc_method_options = ['EN Parabolic-rectangular', 'EN Bi-linear', 'EN Nonlinear', 'Linear elastic', 'Elastic-plastic', 'Sudden plastic']
    reinf_method_options = ['Elastic-plastic', 'Bi-linear hardening', 'Linear elastic', 'Elastic-plastic (no comp.)']
    # hidden values
    f_ct = 2.5

    def __init__(self):
        # Instance variables
        # self.setLimitState(self.limit_state)
        self.update_strengths()
        # self.tensile_strength()

    def setMethods(self, conc_method, reinf_method):
        self.conc_method = conc_method
        self.reinf_method = reinf_method

    def update_strengths(self):
        self.f_cd = self.alpha_cc * self.f_ck / self.gamma_c
        self.f_yd = self.f_yk / self.gamma_s
        self.f_ct = 0.7 * 0.3 * self.f_ck ** (2 / 3)

    # def setLimitState(self, limit_state):
    #     self.limit_state = limit_state
    #     if limit_state == 'SLS':
    #         self.f_cd = self.f_ck
    #         self.f_yd = self.f_yk
    #     elif limit_state == 'ULS':
    #         self.f_cd = self.f_ck / self.gamma_c
    #         self.f_yd = self.f_yk / self.gamma_s
    #     else:
    #         print('NOT VALID LIMIT STATE!')

    # def tensile_strength(self):
    #     self.f_ct = 0.7 * 0.3 * self.f_ck ** (2 / 3)
    #     return self.f_ct

    # Function for converting concrete strain to stress
    def concreteStress(self, strain):
        # input parameters
        f_cd = self.f_cd
        E_cm = self.E_cm * 1000  # converting from GPa to MPa
        eps_c2 = 0.002
        n = 2
        eps_cu2 = 0.0035

        # convert sign of strain so positive strain corresponds to compression vice versa.
        eps_c = -strain

        # calculate concrete compressive stress
        if eps_c < 0:  # is in tension
            sigma_c = 0
        elif eps_c <= eps_c2:
            sigma_c = f_cd * (1 - (1 - eps_c / eps_c2) ** n)
        elif eps_c <= eps_cu2:
            sigma_c = f_cd
        else:
            sigma_c = 0

        ConcreteStress = -sigma_c # convert sign back before returning value

        # check if to overrule with EN Bi-linear behaviour
        if self.conc_method == "EN Bi-linear":

            # load input parameters
            eps_c3 = 0.00175
            eps_cu3 = 0.0035

            # overwrite concrete stiffness
            E_cm = f_cd / eps_c3
            ConcreteStress = E_cm * strain
            if ConcreteStress < -f_cd:
                if eps_c < eps_cu3:
                    ConcreteStress = -f_cd
                else:
                    ConcreteStress = 0
            elif ConcreteStress > 0:
                ConcreteStress = 0

        # check if to overrule with EN Nonlinear behaviour:
        if self.conc_method == "EN Nonlinear":

            # load input parameters
            eps_c1 = 0.0022
            eps_cu1 = 0.0035
            f_cm = f_cd + 8  # what about safety factor?

            eta = eps_c / eps_c1
            k = 1.05 * E_cm * abs(eps_c1) / f_cm
            ConcreteStress = -f_cm * (k * eta - eta ** 2) / (1 + (k - 2) * eta)
            if eps_c > eps_cu1 or eps_c < 0:
                ConcreteStress = 0

        # check if to overrule with linear elastic behaviour
        if self.conc_method == "Linear elastic":
            ConcreteStress = E_cm * strain

        # check if to overrule with elastic-plastic behaviour
        if self.conc_method == "Elastic-plastic":
            ConcreteStress = E_cm * strain
            if ConcreteStress < -f_cd:
                ConcreteStress = -f_cd
            elif ConcreteStress > 0:
                ConcreteStress = 0

        # check if to overrule with sudden plastic behaviour
        if self.conc_method == "Sudden plastic":
            eps_c_pl = 0.002
            if eps_c >= eps_c_pl:
                ConcreteStress = -f_cd
            else:
                ConcreteStress = 0

        return ConcreteStress

    # Function for converting reinforcement strain to stress
    def reinforcementStress(self, eps_s):

        # load input parameters
        f_yd = self.f_yd
        E_s = self.E_s * 1000  # converting from GPa to MPa
        eps_y = f_yd / E_s
        eps_su = 0.05

        # calculate reinforcement stress for elastic-plastic behaviour
        if abs(eps_s) < eps_y: # is elastic
            sigma_s = E_s * eps_s
        elif abs(eps_s) <= eps_su:
            sigma_s = eps_s / abs(eps_s) * f_yd
        else:
            sigma_s = 0

        ReinforcementStress = sigma_s

        # check if to overrule with bi-linear hardening behaviour
        if self.reinf_method == "Bi-linear hardening":
            if abs(eps_s) > eps_y and abs(eps_s) <= eps_su:
                # load input parameters
                k = 1.08
                f_td = k*f_yd

                # adjust k-factor to reflect the given strain
                k = 1 + (k - 1) * (abs(eps_s) - eps_y) / (eps_su - eps_y)

                # calculate reinforcement stress
                ReinforcementStress = k * ReinforcementStress
                # sigma_s = k * f_yd
                # ReinforcementStress = eps_s / Abs(eps_s) * sigma_s

        # check if to overrule with linear elastic behaviour
        if self.reinf_method == "Linear elastic":
            ReinforcementStress = E_s * eps_s

        # check if to overrule with elastic-plastic (no comp.) behaviour
        if self.reinf_method == "Elastic-plastic (no comp.)":
            if ReinforcementStress < 0:
                ReinforcementStress = 0

        return ReinforcementStress


# For when this script is excetuted on its own
if __name__ == '__main__':

    Mat = MatProp()
    print(Mat.f_ck, Mat.f_ct, Mat.f_yk, Mat.concreteStress(-0.002), Mat.reinforcementStress(-0.002))

