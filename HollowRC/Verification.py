# -*- coding: utf-8 -*-
"""
Class definition of an in-plane verification of a concrete disk

Author: Kenneth C. Kleissl
"""
import math
import nlopt


class Verify:  # consider renaming to DiskRC or similar
    """
    A point verification of in-plane loaded reinforced concrete disk

    Inputs:
        stress: the three stress components
        Mat: a material instance
        rho_sx: reinforcement ratio in the x-direction
        rho_sy: reinforcement ratio in the y-direction

    Attributes:
        sigma_min: Minimal principal stress (largest compression / least tension).
        sigma_max: Maximum principal stress (largest tension / least compression).
        tau_max: Maximum shear stress.
        theta_uncracked: Angle of principal compressive stress to the x-axis in un-cracked elastic analysis.
    """

    # Class variables defaults
    # nu method...
    # material defaults?

    def __init__(self, stress, Mat, rho_sx, rho_sy):
        # stress components
        self.sigma_x = stress[0]
        self.sigma_y = stress[1]
        self.tau = stress[2]
        if abs(self.tau) < 1e-6:  # set near zero tau values to zero to ensure exception triggering
            self.tau = 0.0

        # Material parameters
        self.Mat = Mat
        self.rho_sx = rho_sx
        self.rho_sy = rho_sy
        self.rho_c_eq = None  # This is the equivalent reinforcement ratio in the direction of the concrete strut

        # calculate efficiency factor for concrete
        self.nu = self.concrete_efficiency()

    def concrete_efficiency(self):
        # not corrected for plastic rotation, wholly in compression etc.
        nu = 0.6 * (1 - self.Mat.f_ck / 250)
        return nu

    def principal_stresses(self):
        self.sigma_min = (self.sigma_x + self.sigma_y) / 2 - math.sqrt(((self.sigma_x - self.sigma_y) / 2)**2
                                                                       + self.tau**2)
        self.sigma_max = (self.sigma_x + self.sigma_y) / 2 + math.sqrt(((self.sigma_x - self.sigma_y) / 2)**2
                                                                       + self.tau**2)
        self.tau_max = (self.sigma_max - self.sigma_min) / 2
        if self.sigma_x == self.sigma_y:
            if self.tau < 0:
                self.theta_uncracked = 135
            else:
                self.theta_uncracked = 45
        else:
            self.theta_uncracked = math.degrees(0.5 * math.atan(-2 * self.tau / (self.sigma_x - self.sigma_y)))
            if self.sigma_x - self.sigma_y > 0:
                self.theta_uncracked += 90
        return self.sigma_min, self.sigma_max, self.theta_uncracked

    def utilization(self):
        f_ycd = self.Mat.f_yd - self.Mat.f_cd  # yield stress for compression reinf. (no need for nu here)
        # print('sigma_x, sigma_y, f_yd, rho_sx', self.sigma_x, self.sigma_y, self.Mat.f_yd, self.rho_sx)
        try:
            # utilization of each of the yield conditions
            f = [self.sigma_x / (self.rho_sx * self.Mat.f_yd),                                  # σx ≤ ρsx fyd
                 self.sigma_y / (self.rho_sy * self.Mat.f_yd),                                  # σy ≤ ρsy fyd,
                 self.sigma_x / (-self.Mat.f_cd - self.rho_sx * f_ycd),                         # σx ≥ -(fcd + ρsx fycd)
                 self.sigma_y / (-self.Mat.f_cd - self.rho_sy * f_ycd),                         # σy ≥ -(fcd + ρsy fycd)
                 self.tau**2 / ((self.rho_sx * self.Mat.f_yd - self.sigma_x) *                  # τxy2 ≤ (ρsx fyd - σx)
                                (self.rho_sy * self.Mat.f_yd - self.sigma_y) + 1e-12),          # *(ρsy fyd - σy)
                 self.tau**2 / ((self.Mat.f_cd + self.rho_sx * f_ycd + self.sigma_x) *          # τxy2 ≤ (fcd + ρsx fycd + σx)
                                (self.Mat.f_cd + self.rho_sy * f_ycd + self.sigma_y) + 1e-12),  # *(fcd + ρsy fycd + σy)
                 self.tau / (0.5 * self.nu * self.Mat.f_cd)]                                    # | τxy | ≤ 0.5 υ fcd

            # Governing failure mechanism
            if max(f) == max([f[i] for i in [0, 1, 4]]):
                self.mechanism = 'Shear - tension failure'
            elif max(f) == max([f[i] for i in [2, 3, 5]]):
                self.mechanism = 'Shear - compression failure'
            elif max(f) == f[6]:
                self.mechanism = 'Shear - crushing failure'
            else:
                print('error in determining the governing failure mechanism!')
                self.mechanism = None

            # return maximum utilization
            return max(f)
        except ZeroDivisionError:
            return 99

    def tau_yielding(self):
        f_ycd = self.Mat.f_yd - self.Mat.f_cd  # yield stress for compression reinf. (no need for nu here)
        try:
            # tau stress to reach yielding
            tau_y = [math.sqrt((self.rho_sx * self.Mat.f_yd - self.sigma_x) *                   # τxy2 ≤ (ρsx fyd - σx)*
                               (self.rho_sy * self.Mat.f_yd - self.sigma_y)),                   # (ρsy fyd - σy)
                     math.sqrt((self.Mat.f_cd + self.rho_sx * f_ycd + self.sigma_x) *      # τxy2 ≤ (fcd + ρsx fycd + σx)*
                               (self.Mat.f_cd + self.rho_sy * f_ycd + self.sigma_y)),      # (fcd + ρsy fycd + σy)
                     0.5 * self.nu * self.Mat.f_cd]                                             # | τxy | ≤ 0.5 υ fcd
            # return minimum tau to reach yielding
            # print('min tay_y: ', min(tau_y))
            return min(tau_y)
        except ValueError:
            print("tau_yielding could not be evaluated as long. stress was above yielding")
            # print('sx={}, sy={}, tau={}'.format(sigma_x, sigma_y, tau))
            return 0

    def is_yielding(self):
        yielding = False
        f_ycd = self.Mat.f_yd - self.Mat.f_cd  # yield stress for compression reinf. (no need for nu here)

        # Tension criteria in x - direction
        if self.sigma_x > self.rho_sx * self.Mat.f_yd:  # σx ≤ ρsx fyd
            yielding = True
        # Tension criteria in y - direction
        if self.sigma_y > self.rho_sy * self.Mat.f_yd:  # σy ≤ ρsy fyd
            yielding = True
        # Compression criteria in x - direction
        if self.sigma_x < -(self.Mat.f_cd + self.rho_sx * f_ycd):  # σx ≥ -(fcd + ρsx fycd)
            yielding = True
        # Compression criteria in y - direction
        if self.sigma_y < -(self.Mat.f_cd + self.rho_sy * f_ycd):  # σy ≥ -(fcd + ρsy fycd)
            yielding = True
        # Shear - tension criteria
        if self.tau**2 > (self.rho_sx * self.Mat.f_yd - self.sigma_x) * (self.rho_sy * self.Mat.f_yd - self.sigma_y):  # τxy2 ≤ (ρsx fyd - σx)(ρsy fyd - σy)
            yielding = True
        # Shear - compression criteria
        if self.tau**2 > (self.Mat.f_cd + self.rho_sx * f_ycd + self.sigma_x) * (self.Mat.f_cd + self.rho_sy * f_ycd + self.sigma_y):  # τxy2 ≤ (fcd + ρsx fycd + σx)(fcd + ρsy fycd + σy)
            yielding = True
        # Shear criteria
        if self.tau > 0.5 * self.nu * self.Mat.f_cd:  # | τxy | ≤ 0.5 υ fcd
            yielding = True
        return yielding

    def optimal_reinforcement(self):
        # Reinforcement formulas          <-- not yet implemented
        pass

    def is_cracked(self):
        # Check for initial cracking
        # Initial cracking occurs when the sigma_max reaches f_ct,eff
        self.principal_stresses()  # recalculate the principal stresses
        f_ct = self.Mat.f_ct
        f_ct_eff = 0.5 * f_ct
        if self.sigma_max > f_ct_eff:
            return True  # Initially cracked
        else:
            return False  # Uncracked

    # def min_comp_energy(self, x0=[-10, 0, 0, 45]):
    #     # [sigma_c, sigma_sx, sigma_sy, theta]
    #     # initiate optimization instance
    #     opt = nlopt.opt(nlopt.LN_COBYLA, len(x0))
    #     opt.set_lower_bounds([-float('inf'), -float('inf'), -float('inf'), 0])
    #     opt.set_upper_bounds([0, float('inf'), float('inf'), 90])
    #     opt.set_min_objective(lambda x, grad: self.comp_energy_objective(x, grad))
    #     opt.add_equality_mconstraint(lambda result, x, grad: self.equilibrium_constraint(result, x, grad), [1e-6, 1e-6, 1e-6])  # feasible if func < tol
    #     opt.set_xtol_rel(1e-4)
    #     # solve
    #     x = opt.optimize(x0)
    #     # print("result code = ", opt.last_optimize_result())
    #     print("last_optimum_value = ", opt.last_optimum_value())
    #     return x

    # def comp_energy_objective(self, x, grad):
    #     # unload variables
    #     sigma_c = x[0]
    #     sigma_sx = x[1]
    #     sigma_sy = x[2]
    #     # sigma_c, sigma_sx, sigma_sy = x[0:2]
    #     if grad.size > 0:
    #         # grad[:] = [0] * len(grad)
    #         # grad[-1] = 1
    #         print('gradient requested!')
    #     stresses = {'sigma_c': sigma_c, 'sigma_sx': sigma_sx, 'sigma_sy': sigma_sy}
    #     return self.complementary_energy(stresses)

    # def equilibrium_constraint(self, result, x, grad):
    #     # unload variables
    #     sigma_c = x[0]
    #     sigma_sx = x[1]
    #     sigma_sy = x[2]
    #     theta = x[3]
    #     # equilibrium error
    #     self.rho_c_eq = self.rho_sx * cos_deg(theta)**2 + self.rho_sy * sin_deg(theta)**2
    #     result[0] = -self.sigma_x + (1 - self.rho_c_eq) * sigma_c * cos_deg(theta) ** 2 + self.rho_sx * sigma_sx
    #     result[1] = -self.sigma_y + (1 - self.rho_c_eq) * sigma_c * sin_deg(theta) ** 2 + self.rho_sy * sigma_sy
    #     result[2] = -abs(self.tau) - (1 - self.rho_c_eq) * sigma_c * sin_deg(theta) * cos_deg(theta)
    #     return result

    def cracked_strut_angle(self, initial_guess=45.0):
        """
        Find the theta angle that minimize the strain energy
        """
        # slope of cracks/concrete compression
        theta_0 = [initial_guess]  # initial guess of 45 degrees
        opt = nlopt.opt(nlopt.LN_NELDERMEAD, len(theta_0))
        opt.set_lower_bounds([0])  # the bounding speeds up the solver time
        opt.set_upper_bounds([180])  # using [180 - 10**-12] significantly slows the solver
        opt.set_min_objective(lambda theta, grad: self.complementary_energy(self.cracked_equilibrium(theta[0])))
        opt.set_xtol_rel(1e-6)  # theta error tolerance
        theta = opt.optimize(theta_0)
        return theta[0]

    def cracked_equilibrium(self, theta):
        """
        Computes concrete and reinforcement stress for given strut angle theta
        should not be used if section is not cracked
        """
        float_tol = 10**-12  # floats less than this tolerance is considered equal zero

        # check for bi-axial compression (not relevant for HollowRC)
        if abs(self.tau) < float_tol and self.sigma_x < 0 and self.sigma_y < 0:
            print('Bi-axial compression with no shear detected when calculating cracked equilibrium!')
            raise Exception('Bi-axial compression not accounted for!')

        # equivalent reinf ratio in direction of strut
        self.rho_c_eq = self.rho_sx * cos_deg(theta)**2 + self.rho_sy * sin_deg(theta)**2

        # check for horizontal (x-direction) strut
        if abs(sin_deg(theta)) < float_tol:
            # print('horizontal strut detected')
            if abs(self.tau) > float_tol:
                # print(f'tau={self.tau} while having horizontal strut')
                # Equilibrium error
                return {'sigma_c': 10**99, 'sigma_sx': 10**99, 'sigma_sy': 10**99}
            # concrete strut stress
            if self.sigma_x < 0:
                # sigma_c = self.sigma_x / (1 - self.rho_sx + self.rho_sx * self.Mat.E_s / self.Mat.E_cm)  # only linear elastic range!
                eps = self.Mat.composite_strain(self.rho_sx, self.sigma_x)
                sigma_c = self.Mat.concreteStress(eps)
            else:
                sigma_c = 0
            # reinforcement stress by equilibrium
            sigma_sx = (self.sigma_x - (1 - self.rho_sx) * sigma_c) / self.rho_sx
            sigma_sy = self.sigma_y / self.rho_sy

        # check for vertical (y-direction) strut
        elif abs(cos_deg(theta)) < float_tol:
            # print('vertical strut detected')
            if abs(self.tau) > float_tol:
                # print(f'tau={self.tau} while having vertical strut')
                # Equilibrium error
                return {'sigma_c': 10**99, 'sigma_sx': 10**99, 'sigma_sy': 10**99}
            # concrete strut stress
            if self.sigma_y < 0:
                # sigma_c = self.sigma_y / (1 - self.rho_sy + self.rho_sy * self.Mat.E_s / self.Mat.E_cm)  # only linear elastic range!
                eps = self.Mat.composite_strain(self.rho_sy, self.sigma_y)
                sigma_c = self.Mat.concreteStress(eps)
            else:
                sigma_c = 0
            # reinforcement stress by equilibrium
            sigma_sx = self.sigma_x / self.rho_sx
            sigma_sy = (self.sigma_y - (1 - self.rho_sy) * sigma_c) / self.rho_sy

        # diagonal strut
        else:
            # Diagonal concrete stress (negative = compression)
            sigma_c = -abs(self.tau) * (tan_deg(theta) + 1 / tan_deg(theta)) / (1 - self.rho_c_eq)

            # Horizontal reinforcement stress by equilibrium (positive = tension)
            sigma_sx = (self.sigma_x - (1 - self.rho_c_eq) * sigma_c * cos_deg(theta)**2) / self.rho_sx

            # Vertical reinforcement stress by equilibrium (positive = tension)
            sigma_sy = (self.sigma_y - (1 - self.rho_c_eq) * sigma_c * sin_deg(theta)**2) / self.rho_sy

        # try:
        #     # print('stresses: ', self.sigma_x, self.sigma_y, self.tau)
        #     sigma_c = -abs(self.tau) * (tan_deg(theta) + 1 / tan_deg(theta)) / (1 - self.rho_c_eq)  # Diagonal concrete stress (negative = compression)
        #     # sigma_c = -abs(self.tau) / sin_deg(theta) / cos_deg(theta) / (1 - rho_c_eq)  # this version triggers double scalar divide by zero exception...
        #     # sigma_sx = 1 / self.rho_sx * (self.sigma_x + abs(self.tau) / tan_deg(theta))     # Horizontal reinforcement stress (positive = tension)
        #     # sigma_sy = 1 / self.rho_sy * (self.sigma_y + abs(self.tau) * tan_deg(theta))     # Vertical reinforcement stress (positive = tension)
        #     sigma_sx = 1 / self.rho_sx * (self.sigma_x - (1 - self.rho_c_eq) * sigma_c * cos_deg(theta) ** 2)
        #     sigma_sy = 1 / self.rho_sy * (self.sigma_y - (1 - self.rho_c_eq) * sigma_c * sin_deg(theta) ** 2)
        #     if theta == 0.0 or theta == 90.0:
        #         raise ZeroDivisionError   # num. rounding sometimes fails to raise error
        # except ZeroDivisionError:
        #     if self.tau == 0:
        #         # for no shear the diagonal strut should be aligned with possible uniaxial compression
        #         if theta == 0 or abs(sin_deg(theta)) < 10**-12:
        #             if self.sigma_x < 0 and self.sigma_x < self.sigma_y:
        #                 sigma_c = self.sigma_x / (1 - self.rho_sx + self.rho_sx * self.Mat.E_s / self.Mat.E_cm)  # only linear elastic range!
        #             else:
        #                 sigma_c = 0
        #             sigma_sx = (self.sigma_x - (1 - self.rho_sx) * sigma_c) / self.rho_sx
        #             sigma_sy = self.sigma_y / self.rho_sy
        #         elif theta == 90 or abs(cos_deg(theta)) < 10**-12:
        #             if self.sigma_y < 0 and self.sigma_y < self.sigma_x:
        #                 sigma_c = self.sigma_y / (1 - self.rho_sy + self.rho_sy * self.Mat.E_s / self.Mat.E_cm)  # only linear elastic range!
        #             else:
        #                 sigma_c = 0
        #             sigma_sx = self.sigma_x / self.rho_sx
        #             sigma_sy = (self.sigma_y - (1 - self.rho_sy) * sigma_c) / self.rho_sy
        #         else:
        #             sigma_c, sigma_sx, sigma_sy = 10 ** 99, 10 ** 99, 10 ** 99  # should never be reached
        #     else:
        #         # return very large stresses if equilibrium is not possible
        #         sigma_c, sigma_sx, sigma_sy = 10**99, 10**99, 10**99
        #         # print('No equilibrium for vertical/horizontal strut under shear loading')
        return {'sigma_c': sigma_c, 'sigma_sx': sigma_sx, 'sigma_sy': sigma_sy}

    def complementary_energy(self, stresses):  # only linear elastic energy!
        E_c = self.Mat.E_cm * 10**3  # [MPa] Young's modulus (Modulus of Elasticity) of concrete
        E_s = self.Mat.E_s * 10**3   # [MPa]
        # nu = 0.2  # Poisson's ratio of reinforced concrete
        # G = E_c / (2 * (1 + nu))  # Shear Modulus (Modulus of Rigidity) of reinforced concrete
        # Calculate complementary elastic energy (under linear elastic assumption!)
        W_ec = 10**6 * 1 / (2 * E_c) * stresses['sigma_c']**2 * (1 - self.rho_c_eq)
        W_es = 10**6 * self.rho_sx / (2 * E_s) * stresses['sigma_sx']**2 + \
               10**6 * self.rho_sy / (2 * E_s) * stresses['sigma_sy']**2
        W_e = W_ec + W_es
        return W_e  # [Nmm/mm] energy/thickness

    def __str__(self):
        return f'{self.__class__.__name__}(sx={self.sigma_x}, sy={self.sigma_y}, tau={self.tau}, rho_sx={self.rho_sx}, rho_sy={self.rho_sy})'


def cos_deg(deg):
    """
    Cosine function that takes the angle in degrees as input
    """
    return math.cos(math.radians(deg))


def sin_deg(deg):
    """
    Sine function that takes the angle in degrees as input
    """
    return math.sin(math.radians(deg))


def tan_deg(deg):
    """
    Tangent function that takes the angle in degrees as input
    """
    return math.tan(math.radians(deg))


if __name__ == '__main__':
    sigma_x = -25.50  # long.
    sigma_y = 0  # trans.
    tau = 2
    stresses = [sigma_x, sigma_y, tau]
    rho_sx = 0.01  # long.
    rho_sy = 0.01  # trans.
    from Material import MatProp
    Mat = MatProp()
    verification = Verify(stresses, Mat, rho_sx, rho_sy)  # run the main function
    print(verification)
    print('principal_stresses: ', verification.principal_stresses())
    # print('utilization and mechanism: ', verification.utilization(), verification.mechanism)
    theta = verification.cracked_strut_angle()
    # theta = 0
    print('optimized theta = ', theta)
    stresses = verification.cracked_equilibrium(theta)
    print('cracked_equilibrium: ', stresses)
    # print('complementary_energy: ', verification.complementary_energy(stresses))
    # rho_c_eq = rho_sx * cos_deg(theta)**2 + rho_sy * sin_deg(theta)**2
    # print('error1 = ', -sigma_x + (1 - rho_c_eq) * stresses['sigma_c'] * cos_deg(theta) ** 2 + rho_sx * stresses['sigma_sx'])
    # print('error2 = ', -sigma_y + (1 - rho_c_eq) * stresses['sigma_c'] * sin_deg(theta) ** 2 + rho_sy * stresses['sigma_sy'])
    # print('error3 = ', -abs(tau) - (1 - rho_c_eq) * stresses['sigma_c'] * sin_deg(theta) * cos_deg(theta))
    # print('Nx_check = ', (1-rho_sx)*stresses['sigma_c']*200 + stresses['sigma_sx']*200*rho_sx)

    # x = verification.min_comp_energy([stresses['sigma_c'], stresses['sigma_sx'], stresses['sigma_sy'], theta])
    # print('new optimization: ', x)
    # print('error1 = ', -sigma_x + (1 - rho_c_eq) * x[0] * math.cos(math.radians(x[-1])) ** 2 + rho_sx * x[1])
    # print('error2 = ', -sigma_y + (1 - rho_c_eq) * x[0] * math.sin(math.radians(x[-1])) ** 2 + rho_sy * x[2])
    # print('error3 = ', -abs(tau) - (1 - rho_c_eq) * x[0] * math.sin(math.radians(x[-1])) * math.cos(math.radians(x[-1])))
