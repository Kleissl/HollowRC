# -*- coding: utf-8 -*-
"""
Class definition of a container for material properties

Author: Kenneth C. Kleissl
"""
import nlopt


class MatProp:
    """
    A container for material properties

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
    conc_method_options = ['EN Parabolic-rectangular',
                           'EN Bi-linear',
                           'EN Nonlinear',
                           'Linear elastic',
                           'Linear elastic (no ten.)',
                           'Elastic-plastic',
                           'Sudden plastic']
    reinf_method_options = ['Elastic-plastic',
                            'Bi-linear hardening',
                            'Linear elastic',
                            'Elastic-plastic (no comp.)']

    # hidden values
    f_ct = 2.5

    def __repr__(self):
        return f'MatProp(f_ck={self.f_ck}, E_cm={self.E_cm}, f_yk={self.f_yk}, E_s={self.E_s}, ' + \
               f'alpha_cc={self.alpha_cc}, gamma_c={self.gamma_c}, gamma_s={self.gamma_s}, ' + \
               f'conc_method={self.conc_method}, reinf_method={self.reinf_method})'

    def __init__(self):
        # Instance variables
        # self.setLimitState(self.limit_state)
        self.update_strengths()
        # self.tensile_strength()

    def update_strengths(self):
        self.f_cd = self.alpha_cc * self.f_ck / self.gamma_c
        self.f_yd = self.f_yk / self.gamma_s
        self.f_ct = 0.7 * 0.3 * self.f_ck ** (2 / 3)

    def set_methods(self, conc_method, reinf_method):
        self.conc_method = conc_method
        self.reinf_method = reinf_method
        self.update_conc_stiffness()  # some methods overrules the concrete stiffness

    def update_conc_stiffness(self):
        if self.conc_method == 'EN Bi-linear':
            eps_c3 = 0.00175
            self.E_cm = self.f_cd / eps_c3 / 1000
        elif self.conc_method == 'EN Parabolic-rectangular':
            eps = -0.00001
            stress = self.concreteStress(eps)
            self.E_cm = stress / eps / 1000  # calculate initial tanget stiffness
        elif self.conc_method == 'Sudden plastic':
            self.E_cm = 9999

    def is_conc_stiffness_assignable(self):
        """
        This method is used by the GUI to grey out the concrete stiffness input cell if not applicable
        """
        if self.conc_method in ['EN Bi-linear', 'EN Parabolic-rectangular', 'Sudden plastic']:
            assignable = False
        else:
            assignable = True

        return assignable, self.E_cm

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
        E_cm = self.E_cm * 1000  # converting from GPa to MPa
        eps_c2 = 0.002
        n = 2
        eps_cu2 = 0.0035

        # convert sign of strain such that positive eps_c corresponds to compression vice versa.
        eps_c = -strain

        # calculate concrete compressive stress
        if eps_c < 0:  # is in tension
            sigma_c = 0
        elif eps_c <= eps_c2:
            sigma_c = self.f_cd * (1 - (1 - eps_c / eps_c2) ** n)
        elif eps_c <= eps_cu2:
            sigma_c = self.f_cd
        else:
            sigma_c = 0

        ConcreteStress = -sigma_c  # convert sign back before returning value

        # check if to overrule with EN Bi-linear behaviour
        if self.conc_method == "EN Bi-linear":

            # load input parameters
            eps_c3 = 0.00175
            eps_cu3 = 0.0035

            # overwrite concrete stiffness
            E_cm = self.f_cd / eps_c3                # <--- overwrites the user specified stiffness!

            ConcreteStress = E_cm * strain
            if ConcreteStress < -self.f_cd:
                if eps_c <= eps_cu3:  # avoids the vertical part near eps_cu3
                    ConcreteStress = -self.f_cd
                else:
                    ConcreteStress = 0
            elif ConcreteStress > 0:
                ConcreteStress = 0

        # check if to overrule with EN Nonlinear behaviour:
        if self.conc_method == "EN Nonlinear":

            # load input parameters
            eps_c1 = 0.0022
            eps_cu1 = 0.0035
            f_cm = self.f_cd + 8  # what about safety factor?

            eta = eps_c / eps_c1
            k = 1.05 * E_cm * abs(eps_c1) / f_cm
            ConcreteStress = -f_cm * (k * eta - eta ** 2) / (1 + (k - 2) * eta)
            if eps_c > eps_cu1 or eps_c < 0:
                ConcreteStress = 0

        # check if to overrule with linear elastic behaviour
        if self.conc_method == "Linear elastic":
            ConcreteStress = E_cm * strain

        # check if to overrule with linear elastic (no tens.) behaviour
        if self.conc_method == "Linear elastic (no ten.)":
            ConcreteStress = E_cm * strain
            if ConcreteStress > 0:
                ConcreteStress = 0

        # check if to overrule with elastic-plastic behaviour
        if self.conc_method == "Elastic-plastic":
            ConcreteStress = E_cm * strain
            if ConcreteStress < -self.f_cd:
                ConcreteStress = -self.f_cd
            elif ConcreteStress > 0:
                ConcreteStress = 0

        # check if to overrule with sudden plastic behaviour
        if self.conc_method == "Sudden plastic":
            eps_c_pl = 0.002
            if eps_c >= eps_c_pl:
                ConcreteStress = -self.f_cd
            else:
                ConcreteStress = 0

        return ConcreteStress

    # Function for converting reinforcement strain to stress
    def reinforcementStress(self, eps_s):

        # load input parameters
        E_s = self.E_s * 1000  # converting from GPa to MPa
        eps_y = self.f_yd / E_s
        eps_su = 0.05

        # calculate reinforcement stress for elastic-plastic behaviour
        if abs(eps_s) < eps_y:  # is elastic
            sigma_s = E_s * eps_s
        elif abs(eps_s) <= eps_su:
            sigma_s = eps_s / abs(eps_s) * self.f_yd
        else:
            sigma_s = 0

        ReinforcementStress = sigma_s

        # check if to overrule with bi-linear hardening behaviour
        if self.reinf_method == "Bi-linear hardening":
            if abs(eps_s) > eps_y and abs(eps_s) <= eps_su:
                # load input parameters
                k = 1.08
                f_td = k * self.f_yd

                # adjust k-factor to reflect the given strain
                k = 1 + (k - 1) * (abs(eps_s) - eps_y) / (eps_su - eps_y)

                # calculate reinforcement stress
                ReinforcementStress = k * ReinforcementStress
                # sigma_s = k * self.f_yd
                # ReinforcementStress = eps_s / Abs(eps_s) * sigma_s

        # check if to overrule with linear elastic behaviour
        if self.reinf_method == "Linear elastic":
            ReinforcementStress = E_s * eps_s

        # check if to overrule with elastic-plastic (no comp.) behaviour
        if self.reinf_method == "Elastic-plastic (no comp.)":
            if ReinforcementStress < 0:
                ReinforcementStress = 0

        return ReinforcementStress

    def composite_stress(self, rho, eps):
        reinf_stress = self.reinforcementStress(eps)
        concrete_stress = self.concreteStress(eps)
        return concrete_stress * (1 - rho) + reinf_stress * rho

    def composite_strain(self, rho, sigma):
        """
        determine strain for given composite stress with reinforcement ratio of rho
        """
        if sigma > 0:
            eps_0 = [sigma/rho/self.E_s/1000]  # initial guess for tension
        else:
            eps_0 = [-0.001]  # initial guess for compression
        # print(f'eps_0 = {eps_0[0]}')
        opt = nlopt.opt(nlopt.LN_NELDERMEAD, len(eps_0))
        opt.set_min_objective(lambda eps, grad: (sigma - self.composite_stress(rho, eps[0]))**2)
        opt.set_xtol_rel(1e-4)  # stress error tolerance
        eps = opt.optimize(eps_0)
        return eps[0]


# For when this script is excetuted on its own
if __name__ == '__main__':

    Mat = MatProp()
    print(Mat.f_ck, Mat.f_ct, Mat.f_yk, Mat.concreteStress(-0.002), Mat.reinforcementStress(-0.002), Mat.E_cm)

    rho = 0.01
    strain = Mat.composite_strain(rho, -25)
    print(f'strain = {strain}')
    composite_stress = Mat.composite_stress(rho, strain)
    print(f'composite_stress = {composite_stress}')
    concrete_stress = Mat.concreteStress(strain)
    print(f'concrete_stress = {concrete_stress}')
    reinf_stress = Mat.reinforcementStress(strain)
    print(f'reinf_stress = {reinf_stress}')
