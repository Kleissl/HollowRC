# -*- coding: utf-8 -*-
"""
Analysis class for  "Hollow section analysis"

Script defining the Analysis class

History log:
Version 0.1 - first working build

Author: Kenneth C. Kleissl (KEKL)
Last edited: May 2018
"""

# Standard library modules
import math

# Third-party library modules
import numpy as np
import nlopt

# Local source tree modules
import Verification
import SectionForces
import Material
import Results


# Perform a Minimum Complementary Energy Analysis (incl. optimizing shear flow based on capacity)
def minCompEnergy(section, SF, Mat):
    pass


# Perform a Plane Section Analysis (incl. optimizing shear flow based on capacity)
def planeSection(section, SF, Mat):
    print('---------- Plane section ULS analysis initiated ----------')

    # --------------- Initial guess of optimization variables based on uncracked analysis ---------------
    x0 = uncracked_strain_state(section, SF)

    # --------------- Determine the plane strain section for the primary section ---------------
    opt = nlopt.opt(nlopt.LN_NELDERMEAD, len(x0))
    opt.set_min_objective(lambda x, grad: errorFunBending(x, section, SF, Mat))
    opt.set_xtol_rel(1e-8)
    x = opt.optimize(x0)
    print("Optimized strain state =", x)
    print("Minimized error value = ", opt.last_optimum_value())
    # print("result code = ", opt.last_optimize_result())

    # If bending equilibrium fails capacity is insufficient -> intro. load factor and minimize it under error constraint
    if opt.last_optimum_value() > 1e-4:
        print("Error too big!, needs to consider a lambda_bending factor!")
        error_msg = ["Failed to find bending equilibrium", "The section cannot sustain the bending loads applied"]
        return None, error_msg

        # ------- need to implement gradients for optimization below ------
        # print("Error too big!, steps over to bigger problem including load factor")
        # # initial guess
        # x0 = np.append(x0, 0.9)
        # print('x0 = ', x0)
        # # initiate optimization instance
        # opt = nlopt.opt(nlopt.LN_COBYLA, len(x0))  # only LN_COBYLA support constraints
        # # set bounds
        # # opt.set_lower_bounds([-float('inf'), -float('inf'), -float('inf'), 1e-4])
        # # opt.set_upper_bounds([float('inf'), float('inf'), float('inf'), 1.0])
        # # set objective
        # # opt.set_max_objective(lambda x, grad: myObjective(x))
        # opt.set_max_objective(myObjective)
        # # set constraint
        # # opt.add_equality_constraint(lambda x, grad: errorFun(x, Geometry, SF, Mat), 1e-8)
        # opt.add_inequality_constraint(lambda x, grad: errorFunBending(x, section, SF, Mat), 1e-8)  # feasible if func < tol
        # # set tolerances
        # opt.set_xtol_rel(1e-8)
        # # solve
        # xopt = opt.optimize(x0)
        # x = xopt[:-1]
        # # print result
        # print("bending load factor =", xopt[-1])
        # print("bending optimum at x =", x)
        # print("bending error at opt =", errorFunBending(xopt, section, SF, Mat))
        # # print("result code = ", opt.last_optimize_result())
        #
        # if opt.last_optimum_value() > 1e-4:
        #     print("Error too big!, bigger problem including load factor failed, try with less load")
        #     error_msg = ["Failed to find bending equilibrium", "try with less load"]
        # else:
        #     print("Bigger problem including load factor succeeded, Maximum bending load factor is: " + str(xopt[-1]))
        #     error_msg = ["Failed to find bending equilibrium", "Maximum bending load factor is: " + str(xopt[-1])]
        # return None, error_msg

    _, dist = BendingEQ(section, Mat, x[0], x[1], x[2])  # get distributions

    # --------------- Dual-section analysis for initial guess ---------------
    # Prepare second section
    dx = 0.001  # [m] Offset
    SF2 = SectionForces.SectionForces(SF.N, SF.Mx + dx * SF.Vy, SF.My - dx * SF.Vx)
    # SF2 = prep_dual_section(SF, dx)  # nabouring SF

    # Optimize plane strain variables for the secondary section
    opt2 = nlopt.opt(nlopt.LN_NELDERMEAD, len(x))
    opt2.set_min_objective(lambda x, grad: errorFunBending(x, section, SF2, Mat))
    opt2.set_xtol_rel(1e-8)
    x2 = opt2.optimize(x)
    print("Optimized strain state2 =", x2)
    print("Minimized error2 value = ", opt.last_optimum_value())
    # print("result2 code = ", opt.last_optimize_result())

    # Shear flow - Counter-clockwise shear flow is positive
    _, dist = BendingEQ(section, Mat, x[0], x[1], x[2])         # get distributions from first section
    _, dist2 = BendingEQ(section, Mat, x2[0], x2[1], x2[2])     # get distributions from first section
    H = shear_flow(dist, dist2, SF, section, dx)

    # --------------- Optimize shear flow distribution ---------------
    # initial guess for shear flow distribution
    x0 = np.array(H)
    x0 = np.append(x0, 1.0)  # append the shear load factor variable

    # Determine variable bounds based on shear flow at yielding
    H_yield = []
    i = 0
    for wall in section.walls:  # looping over walls
        for j in range(wall.wallNodeN):  # looping over wall data points
            sigma_x = dist['normal_flow'][i] / wall.thick
            stress = [sigma_x, 0, 0]
            verification = Verification.Verify(stress, Mat, wall.rho_long, wall.rho_trans)
            H_yield.append(verification.tau_yielding() * wall.thick)
            i += 1  # index counter to be used with continuous dist vectors
    # print('H_yield: ', H_yield)
    lower_bound = [-x for x in H_yield]     # define lower bound list by neative yield shear flow
    lower_bound.append(1e-8)                # add shear load factor to lower bound list
    upper_bound = H_yield + [1.0]           # define upper bound list by pos. yield shear flow + added shear load factor

    # move initial guess inside bounds
    for i in range(len(x0)):
        x0[i] = np.sign(x0[i]) * upper_bound[i]  # optimization seems to work better for large initial shear flows
        # if abs(x0[i]) > upper_bound[i]:
        #     # print('bound ', i, ' outside bound')
        #     x0[i] = x0[i]/abs(x0[i])*abs(upper_bound[i])

    # initiate optimization instance
    opt = nlopt.opt(nlopt.LD_SLSQP, len(x0))   # only LD_SLSQP support equality constraints

    # set bounds
    opt.set_lower_bounds(lower_bound)
    opt.set_upper_bounds(upper_bound)
    # set objective
    # opt.set_max_objective(lambda x, grad: myObjective(x))
    opt.set_max_objective(myObjective)
    # set constraint
    # opt.add_equality_constraint(lambda x, grad: errorFunShear(x, Geometry, SF, Mat), 1e-8)
    # opt.add_inequality_constraint(lambda x, grad: errorFunShear(x, Geometry, SF, dist), 1e-6)  # feasible if func < tol
    opt.add_equality_mconstraint(lambda result, x, grad: myShearConstraints(result, x, grad, section, SF, dist), [1e-6, 1e-6, 1e-6])  # feasible if func < tol
    # opt.add_inequality_constraint(lambda x, grad: myYieldConstraint(x, dist), 1e-8)
    # tolerances
    opt.set_xtol_rel(1e-8)
    # solve
    xopt = opt.optimize(x0)
    H = xopt[:-1]
    # print result
    print("shear maximized load factor =", xopt[-1])
    # print("shear final objective = ", opt.last_optimum_value())
    # print("shear optimum at H =", H)
    shear_error = errorFunShear(xopt, section, SF, dist)
    print("shear error at opt =", shear_error)
    # print("shear result code = ", opt.last_optimize_result())
    if shear_error > 1e-4:
        print("Error too big!, shear optimization failed")
        error_msg = ["Failed to optimize shear flow"]
        return None, error_msg

    # --------------- Adjust the found optimum ---------------
    # The shear optimization problem should have been reduced to a smaller problem where the total shear force in each wall makes up the variables
    # for now the shear distribution in each wall is locally rearranged to instead reflect a scaled down H_yield distribution
    H_adjust = []
    for i, wall in enumerate(section.walls):  # looping over walls
        j_start = i * wall.wallNodeN
        j_end = (i + 1) * wall.wallNodeN
        # define weights/eff. length for each node
        ds = [0.5 * wall.length / (wall.wallNodeN - 1) if i in (0, wall.wallNodeN - 1) else wall.length / (
                    wall.wallNodeN - 1) for i in range(wall.wallNodeN)]
        # Integrate optimized shear flow
        V_wall = sum(ds * H[j_start:j_end])
        # Integrate yield shear flow
        V_yield = sum(ds * np.array(H_yield)[j_start:j_end])
        scale_factor = V_wall / V_yield
        print('shear flow in wall {} ({:.2f}kN) is at {:.2f}% utilization'.format(i + 1, V_wall, abs(scale_factor) * 100))
        # replace H with scaled down H_yield
        H_adjust.extend([scale_factor * H_yield[i] for i in range(j_start, j_end)])
    H = np.array(H_adjust)

    # --------------- ULS verification ---------------
    # Disk stress components
    ur_over = []
    i = 0
    for wall in section.walls:  # looping over walls
        for j in range(wall.wallNodeN):  # looping over wall data points
            sigma_x = dist['normal_flow'][i] / wall.thick
            tau = H[i] / wall.thick
            stress = [sigma_x, 0, tau]
            verification = Verification.Verify(stress, Mat, wall.rho_long, wall.rho_trans)
            ur_over.append(max(0, verification.utilization() - 1))
            # print("sigma_x, tau, UR =", sigma_x, tau, f[-1])
            i += 1  # index counter to be used with continuous dist vectors
    if max(ur_over) > 0:
        print("yield/overutilization reached!")
    else:
        print("no yielding occurs")
    H_yield = H_yield * H / (abs(H) + 1e-12)

    # Initiate Results class
    Res = Results.Results(dist['x'], dist['y'], dist['wallAngle'])
    Res.add_plot(dist['strain']*100, 'M+N strain', '%', 0.15)
    Res.add_plot(dist['concrete_stress'], 'M+N concrete stress', 'MPa', 0.1)
    Res.add_plot(dist['reinforcement_stress'], 'M+N reinforcement stress', 'MPa', 0.15)
    Res.add_plot(dist['normal_flow'], 'Normal flow', 'kN/m', 0.17)
    Res.add_plot(H, 'Shear flow', 'kN/m', 0.20)
    Res.add_plot(np.array(H_yield), 'Max shear flow', 'kN/m', 0.20 * max(H_yield) / (max(abs(H)) + 1e-12))
    # Res.add_plot(np.array(ur_over), 'Over-utilization', '', 0.25)

    print("Shear flow optimization succeeded, Maximum shear load factor is: " + str(xopt[-1]))
    if xopt[-1] == 1:
        error_msg = None
    else:
        error_msg = ["The section shear force utilization is at {:.1f}%".format(100/xopt[-1]), "The shown results applies maximized shear load factor of {:.4f}".format(xopt[-1])]
        # error_msg = ["The shown results applies maximized shear load factor:", "Maximum shear load factor = " +
        #          str(xopt[-1])]

    print('Integration test: ', integrateShearFlow(H, dist, section))

    return Res, error_msg


# def myYieldConstraint(x, dist):  # Something like this will be needed if also to optimize normal flow
#     # unload variables
#     H = x[:-1]
#
#     # Disk stress components
#     thick = 200  # wall thickness hardcoded for now
#     ur_over = []
#     for i in range(len(dist['normal_flow'])):
#         sigma_x = dist['normal_flow'][i] / thick
#         tau = H[i] / thick
#         stress = [sigma_x, 0, tau]
#         verification = Verification.Verify(stress)
#         ur_over.append(max(0, verification.utilization() - 1))
#
#         # print("sigma_x, tau, UR =", sigma_x, tau, f[-1])
#     return max(ur_over)


def finite_difference(x, section, SF, dist):  # finite-difference function to check analytical gradient matrix
    grad = np.empty(shape=(3, len(x)))
    delta = 0.1
    for i in range(len(x)):
        x_delta = np.zeros_like(x)
        x_delta[i] = x_delta[i] + delta
        result1 = constrain_function(x + x_delta, section, SF, dist)
        result2 = constrain_function(x - x_delta, section, SF, dist)
        grad[0, i] = (result1[0] - result2[0]) / (2 * delta)
        grad[1, i] = (result1[1] - result2[1]) / (2 * delta)
        grad[2, i] = (result1[2] - result2[2]) / (2 * delta)
    return grad


def constrain_function(x, section, SF, dist):  # constrain function to be used with finite-difference
    # unload variables
    H = x[:-1]
    load_fac = x[-1]

    # integrate shear flow into sectional forces
    Vx, Vy, T = integrateShearFlow(H, dist, section)

    # Section force difference (sum squared diff.)
    result = [SF.Vx * load_fac - Vx,
              SF.Vy * load_fac - Vy,
              SF.T * load_fac - T]
    return result


def myShearConstraints(result, x, grad, section, SF, dist):  # constrain function for shear optimization
    # unload variables
    H = x[:-1]
    load_fac = x[-1]

    # integrate shear flow into sectional forces
    Vx, Vy, T = integrateShearFlow(H, dist, section)

    # Section force difference (sum squared diff.)
    result[0] = SF.Vx * load_fac - Vx
    result[1] = SF.Vy * load_fac - Vy
    result[2] = SF.T * load_fac - T

    if grad.size > 0:
        # get geometry stuff
        wallAngle = dist['wallAngle'][:-1]
        e = section.get_e(local_data=True)[:-1] / 1000
        ds = dist['ds'] / 1000

        # first node
        grad[0, 0] = 0.5 * ds[0] * np.cos(wallAngle[0])
        grad[1, 0] = 0.5 * ds[0] * np.sin(wallAngle[0])
        grad[2, 0] = - 0.5 * ds[0] * e[0]

        for j in range(1, len(H) - 1):  # loop over central nodes
            # print('j = ', j)
            grad[0, j] = 0.5 * ds[j - 1] * np.cos(wallAngle[j - 1]) + 0.5 * ds[j] * np.cos(wallAngle[j])
            grad[1, j] = 0.5 * ds[j - 1] * np.sin(wallAngle[j - 1]) + 0.5 * ds[j] * np.sin(wallAngle[j])
            grad[2, j] = - 0.5 * ds[j - 1] * e[j - 1]               - 0.5 * ds[j] * e[j]

        # last node
        grad[0, -2] = 0.5 * ds[-1] * np.cos(wallAngle[-1])
        grad[1, -2] = 0.5 * ds[-1] * np.sin(wallAngle[-1])
        grad[2, -2] = - 0.5 * ds[-1] * e[-1]

        # load factor gradient
        grad[0, -1] = SF.Vx
        grad[1, -1] = SF.Vy
        grad[2, -1] = SF.T

    # check gradient matrix by finite-difference
    # grad2 = finite_difference(x, Geometry, SF, dist)
    # print('grad shape: ', grad.shape)
    # print('grad2 shape: ', grad2.shape)
    # print('max abs grad diff: ', np.max(np.abs(grad - grad2)))


def integrateShearFlow(H, dist, section):
    # # calculate average shear flow between data points
    # H_avg = (H[1:] + H[:-1]) / 2
    #
    # # get geometry stuff
    # wallNodeN = Geometry['wallNodeN']
    # wallAngle = dist['wallAngle'][:-1]
    # e = np.repeat(Geometry['e'], wallNodeN)[:-1] / 1000
    # ds = dist['ds'] / 1000
    #
    # Integrate for shear sectional forces
    # Vx = sum(H_avg * ds * np.cos(wallAngle))
    # Vy = sum(-H_avg * ds * np.sin(wallAngle))
    # T = sum(H_avg * ds * e)

    # --------------------- Matrix approach ---------------------------
    # Averaging matrix
    A = np.zeros(shape=(len(H) - 1, len(H)))
    for i, row in enumerate(A):
        row[i] = 0.5
        row[i + 1] = 0.5
    H_avg = np.dot(A, H)

    # get geometry stuff
    wallAngle = dist['wallAngle'][:-1]
    e = section.get_e(local_data=True)[:-1] / 1000
    ds = dist['ds'] / 1000

    # Integration matrix
    T = np.zeros(shape=(3, len(H) - 1))
    T[0, :] = - ds * np.cos(wallAngle)      # Vx (negative as geometry is define opposite positive flow)
    T[1, :] = - ds * np.sin(wallAngle)      # Vy (negative as geometry is define opposite positive flow)
    T[2, :] = ds * e                        # T
    Vx, Vy, T = np.dot(T, H_avg)
    return Vx, Vy, T


def errorFunShear(x, section, SF, dist):
    # unload variables
    H = x[:-1]
    load_fac = x[-1]

    # calculate average shear flow between data points
    H_avg = (H[1:] + H[:-1]) / 2

    # get perp. distance
    e = section.get_e(local_data=True)

    # Integrate for shear sectional forces
    Vy = sum(-H_avg * dist['ds'] / 1000 * np.sin(dist['wallAngle'][:-1]))
    Vx = sum(-H_avg * dist['ds'] / 1000 * np.cos(dist['wallAngle'][:-1]))
    T = sum(H_avg * dist['ds'] / 1000 * e[:-1] / 1000)
    print('Integrated Vx, Vy, T: ', Vx, Vy, T)

    # Section force difference (sum squared diff.)
    return (SF.Vy*load_fac - Vy)**2 + (SF.Vx*load_fac - Vx)**2 + (SF.T*load_fac - T)**2


def myObjective(x, grad):  # objective function defining last variable as the objevtive
    if grad.size > 0:
        grad[:] = [0]*len(grad)
        grad[-1] = 1
    return x[-1]


# Perform a Dual Section Analysis (incl. shear flow determined by equilibrium)
def dualSection(section, SF, Mat):
    print('---------- Dual section SLS analysis initiated ----------')

    # --------------- Initial guess of optimization variables based on uncracked analysis ---------------
    x0 = uncracked_strain_state(section, SF)

    # --------------- Optimize plane strain variables for the primary section ---------------
    opt = nlopt.opt(nlopt.LN_NELDERMEAD, len(x0))
    opt.set_min_objective(lambda x, grad: errorFunBending(x, section, SF, Mat))
    opt.set_xtol_rel(1e-8)
    x = opt.optimize(x0)
    print("Optimized strain state =", x)
    print("Minimized error value = ", opt.last_optimum_value())

    # check result for high error margin
    if opt.last_optimum_value() > 1e-4:
        print("Failed to find bending equilibrium, try with less load")
        # error_msg = ["Failed to find bending equilibrium", "try with less load"]
        error_msg = ["Failed to find bending equilibrium", "The section cannot sustain the bending loads applied"]
        return None, error_msg

    # --------------- Prepare second section ---------------
    dx = 0.001  # [m] Offset
    SF2 = SectionForces.SectionForces(SF.N, SF.Mx + dx * SF.Vy, SF.My - dx * SF.Vx)
    # SF2 = prep_dual_section(SF, dx)  # nabouring SF

    # --------------- Optimize plane strain variables for the secondary section ---------------
    opt2 = nlopt.opt(nlopt.LN_NELDERMEAD, len(x))
    opt2.set_min_objective(lambda x, grad: errorFunBending(x, section, SF2, Mat))
    opt2.set_xtol_rel(1e-8)
    x2 = opt2.optimize(x)
    print("Optimized strain state2 =", x2)
    print("Minimized error2 value = ", opt.last_optimum_value())

    # --------------- Shear flow - Counter-clockwise shear flow is positive ---------------
    _, dist = BendingEQ(section, Mat, x[0], x[1], x[2])         # get distributions from first section
    _, dist2 = BendingEQ(section, Mat, x2[0], x2[1], x2[2])     # get distributions from first section
    H = shear_flow(dist, dist2, SF, section, dx)

    # --------------- SLS verification ---------------
    # Disk stress components
    theta, sigma_c, sigma_sx, sigma_sy = [], [], [], []
    i = 0
    for wall in section.walls:  # looping over walls
        for j in range(wall.wallNodeN):  # looping over wall data points
            sigma_x = dist['normal_flow'][i] / wall.thick
            tau = H[i] / wall.thick
            stress = [sigma_x, 0, tau]
            verification = Verification.Verify(stress, Mat, wall.rho_long, wall.rho_trans)
            theta.append(verification.cracked_strut_angle())
            stresses = verification.cracked_equilibrium(theta[i])
            sigma_c.append(stresses['sigma_c'])
            sigma_sx.append(stresses['sigma_sx'])
            sigma_sy.append(stresses['sigma_sy'])
            # if wall==section.walls[0] and j==12:
            #     print('H={:.4f}, N={:.4f}, tau={:.4f}, sigma_x={:.4f}, thk={}'.format(H[i], dist['normal_flow'][i], tau, sigma_x, wall.thick))
            #     print('stress:', stress)
            #     print('theta:', theta[i])
            #     print('stresses:', stresses)
            #     print('H[i], wall.thick, tau, H[i]/wall.thick', H[i], wall.thick, tau, H[i]/wall.thick)
            i += 1  # index counter to be used with continuous dist vectors
    if max(max(sigma_sx), max(sigma_sy)) > 200:
        print("reinforcement stress > 200 MPa!")
    sigma_c, sigma_sx, sigma_sy = np.array(sigma_c), np.array(sigma_sx), np.array(sigma_sy)

    # Initiate Results class
    Res = Results.Results(dist['x'], dist['y'], dist['wallAngle'])
    Res.add_plot(dist['strain']*100, 'M+N strain', '%', 0.15)
    Res.add_plot(dist['concrete_stress'], 'M+N concrete stress', 'MPa', 0.1)
    Res.add_plot(dist['reinforcement_stress'], 'M+N reinforcement stress', 'MPa', 0.15)
    Res.add_plot(dist['normal_flow'], 'Normal flow', 'kN/m', 0.17)
    Res.add_plot(H, 'Shear flow', 'kN/m', 0.20)
    Res.add_plot(np.array(theta), 'Cracked strut angle', 'deg', 0.25)
    Res.add_plot(sigma_c, 'In-plane concrete stress', 'MPa', 0.1 * max(abs(sigma_c)) / (max(abs(dist['concrete_stress'])) + 1e-12))
    Res.add_plot(sigma_sx, 'Long. reinf. stress', 'MPa', 0.15 * max(abs(sigma_sx)) / (max(abs(dist['reinforcement_stress'])) + 1e-12))
    Res.add_plot(sigma_sy, 'Trans. reinf. stress', 'MPa', 0.15 * max(abs(sigma_sy)) / (max(abs(dist['reinforcement_stress'])) + 1e-12))

    print('Integration test: ', integrateShearFlow(H, dist, section))
    return Res, None


# def prep_dual_section(SF, dx):
#     # --------------- Prepare second section ---------------
#     # make sure shear is perpendicular to resulting moment
#     Vres = math.sqrt(SF.Vx ** 2 + SF.Vy ** 2)
#     # print("original Vy, Vx =",SF['Vy'], SF['Vx'])
#
#     # bending moment angle (loading angle, not NA angle!)
#     load_angle = math.atan2(SF.My, SF.Mx)
#     # print("load angle = ", math.degrees(load_angle))
#
#     # Shear force components ensuring perp. to res. moment
#     Vy = -Vres * math.cos(load_angle)
#     Vx = -Vres * math.sin(load_angle)
#     print("perp. Vx, Vy =", Vx, Vy)
#
#     # SF2 = SectionForces.SectionForces(SF.N, SF.Mx + dx * Vy, SF.My + dx * Vx)
#     SF2 = SectionForces.SectionForces(SF.N, SF.Mx + dx * Vy, SF.My - dx * Vx)
#     # SF2 = dict()
#     # SF2['N'] = SF["N"]
#     # SF2['Mx'] = SF["Mx"] + dx * Vy
#     # SF2['My'] = SF["My"] + dx * Vx
#     return SF2


def shear_flow(dist, dist2, SF, section, dx):
    dN = (dist2['normal_flow'] - dist['normal_flow'])  # calculate normal flow difference
    dN_avg = (dN[1:] + dN[:-1]) / 2  # calculate average normal flow diff. between data points
    dH_avg = dN_avg * dist['ds'] / dx / 1000  # convert normal flow diff. to shear flow diff.
    H = [0.0]  # temporarily assume shear flow to start at zero
    for row in dH_avg:
        H.append(H[-1] - row)  # articulate shear flow distribution (neg. sign as the articulation is against pos. flow)
    H = np.array(H)  # convert list to np array
    H_avg = (H[1:] + H[:-1]) / 2  # calculate average shear flow between data points

    # Introduce offset to match Torsional moment
    e = section.get_e(local_data=True)
    T = sum(H_avg * dist['ds'] / 1000 * e[:-1] / 1000)
    H_offset = -(T - SF.T) / (2 * abs(
        section.get_enclosed_area()))  # the sign might have to be used for counter-clock wall arrangement
    H = H + H_offset
    return H


def errorFunBending(x0, section, SF, Mat):
    # unload variables
    if len(x0) > 3:
        NA_angle, eps_comp, eps_tens, load_fac = x0
        # SF.fac_bending = load_fac
    else:
        NA_angle, eps_comp, eps_tens = x0
        load_fac = 1.0

    # call bending equilibrium function
    curSF, _ = BendingEQ(section, Mat, NA_angle, eps_comp, eps_tens)  # get SF for given strain state

    # Section force difference (sum squared diff.)
    return (SF.N*load_fac - curSF.N)**2 + (SF.Mx*load_fac - curSF.Mx)**2 + (SF.My*load_fac - curSF.My)**2


def uncracked_strain_state(section, SF):
    # NA_angle = -11.56       # angle of NA relative to horizontal (positive counter-clockwise)
    # eps_comp = - 1.397e-03  # strain in extreme compression fiber
    # eps_tens = 2.923e-03    # strain in extreme tension fiber

    # bending moment angle (loading angle, not NA angle!)
    load_angle = math.degrees(math.atan2(SF.My, SF.Mx))

    NA_angle = load_angle       # angle of NA relative to horizontal (positive counter-clockwise)
    eps_comp = - 1.5e-03  # strain in extreme compression fiber
    eps_tens = 3.0e-03    # strain in extreme tension fiber
    x0 = np.array([NA_angle, eps_comp, eps_tens])  # initial guess
    return x0
    # SHOULD INSTEAD ESTIMATE THIS BY UNCRACKED SECTIONAL ANALYSIS


def BendingEQ(section, Mat, NA_angle, eps_comp, eps_tens):

    # Along-walls data points
    s, x, y, wallAngle = [], [], [], []  # lower case coordinates is for the local nodes
    length_prev = 0  # accumulated length of previous walls
    for wall in section.walls:      # looping over walls
        for j in range(wall.wallNodeN):  # looping over wall data points
            s.append(length_prev + j / (wall.wallNodeN - 1) * wall.length)  # Along-wall S-coordinates
            x.append(wall.X[0] + j / (wall.wallNodeN - 1) * wall.dX)
            y.append(wall.Y[0] + j / (wall.wallNodeN - 1) * wall.dY)
            # eta.append( math.cos(math.radians(NA_angle)) * (y[-1] - centreY) - math.sin(math.radians(NA_angle)) * (x[-1] - centreX))
            wallAngle.append(wall.angle)
        length_prev += wall.length

    # the eta-axis is defined perp. to NA from GC towards compression
    centreX, centreY = section.get_centre()
    eta = math.cos(math.radians(NA_angle)) * (np.array(y) - centreY) - math.sin(math.radians(NA_angle)) * (np.array(x) - centreX)

    ds = np.array(s[1:]) - np.array(s[:-1])
    #print("ds=", ds)

    # Strain (negative: compression, positive: tension)
    eta_max = max(eta)  # extreme compression fiber
    eta_min = min(eta)  # extreme tension fiber
    eps = eps_comp + (eps_comp - eps_tens) / (eta_max - eta_min) * (eta - eta_max)  # - eta_plastic
    #print("eps =", eps)

    # Concrete stress
    sigmaConc = ConcreteStressAry(eps, Mat)
    #print("sigmaConc =", sigmaConc)

    # Reinforcement stress
    sigmaReinf = ReinforcementStressAry(eps, Mat)
    #print("sigmaReinf =", sigmaReinf)

    # Number of data points per wall
    wallNodeN = section.walls[0].wallNodeN
    wallNo = np.repeat(range(len(section.walls)), wallNodeN)  # repeat each index in the array N times in the new array

    # Normal flows
    rho_long = np.array(section.get_rho_long())
    thick = np.array(section.get_thick())
    N_c = sigmaConc * thick[wallNo] * (1 - rho_long[wallNo])
    N_s = sigmaReinf * thick[wallNo] * rho_long[wallNo]
    N_tot = N_c + N_s
    #print("N_c =",N_c)
    #print("N_s =", N_s)
    #print("N_tot =", N_tot)

    N_avg = (N_tot[1:] + N_tot[:-1]) / 2
    #print("N_avg =", N_avg)

    # Normal stress integration about concrete centre
    # Normal force
    F_tot = N_avg * ds / 1000  # [kN]
    #print("F_tot =", F_tot)
    N = sum(F_tot)

    # Moment about x-axis
    y_avg = (np.array(y[1:]) + np.array(y[:-1])) / 2
    wallMx = -F_tot * (y_avg - centreY) / 1000  # [kNm]
    Mx = sum(wallMx)

    # Moment about y-axis
    x_avg = (np.array(x[1:]) + np.array(x[:-1])) / 2
    wallMy = F_tot * (x_avg - centreX) / 1000  # [kNm]
    My = sum(wallMy)

    # Dump into SectionForces class
    SF = SectionForces.SectionForces(N, Mx, My)

    # Arrange stress/flow distributions into a dictionary
    dist = dict()
    dist['strain'] = eps
    dist['concrete_stress'] = sigmaConc
    dist['reinforcement_stress'] = sigmaReinf
    dist['normal_flow'] = N_tot     # N_avg*ds/1000  # convert normal flow into discreticed forces  [kN/m] -> [kN]
    # dist['distance'] = e[wallNo]
    dist['ds'] = ds
    dist['x'] = x
    dist['y'] = y
    dist['wallNo'] = wallNo
    dist['wallAngle'] = wallAngle

    return SF, dist


def ConcreteStressAry(eps, Mat):
    # This is just a facade for the ConcreteStress function able to handle arrays
    if isinstance(eps, (int, float)):  # check if a single value (int or float) is given
        return Mat.concreteStress(eps)
    else:
        stress = []  # Initiate array
        for strain in np.asarray(eps):  # loop over array
            stress.append(Mat.concreteStress(strain))
        return np.array(stress)


def ReinforcementStressAry(eps, Mat):
    # This is just a facade for the ReinforcementStress function able to handle arrays
    if isinstance(eps, (int, float)):  # check if a single value (int or float) is given
        return Mat.reinforcementStress(eps)
    else:
        stress = []  # Initiate array
        for strain in np.asarray(eps):  # loop over array
            stress.append(Mat.reinforcementStress(strain))
        return np.array(stress)


# For when this script is excetuted on its own
if __name__ == '__main__':  # if we're running file directly and not importing it
    # Define Geometry
    X = [-1500, 1500, 1500, -1500]  # X-coordinates
    Y = [1500, 1500, -2000, -2000]  # Y-coordinates
    T = [200, 200, 200, 200]  # Wall thickness
    rho_long = [0.02, 0.02, 0.02, 0.02]  # Reinforcement ratio
    Geometry = {'X': X, 'Y': Y, 'T': T, 'rho_long': rho_long}
    Geometry['wallNodeN'] = 10

    # Define sectional forces
    N = -17000
    Mx = 50000
    My = 00000
    Vx = 0
    Vy = 2000
    T = 0
    SF = SectionForces.SectionForces(N, Mx, My, Vx, Vy, T)

    # Initiate Material class
    Mat = Material.MatProp()

    # Call SLS analysis
    Res = dualSection(Geometry, SF, Mat)

    # Call ULS analysis
    Res = planeSection(Geometry, SF, Mat)
    # print(Res.plot_names)
