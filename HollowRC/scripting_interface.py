'''
Scripting interface for HollowRC

Author: Kenneth C. Kleissl
'''
# imports
from Geometry import CrossSection, Wall
from Material import MatProp
from SectionForces import SectionForces
import Analysis

# ----- Geometry -----
thick = 600
rho_long = 0.022
rho_trans = 0.008

wall_1 = Wall([0, 5000], [7000, 7000], thick, rho_long, rho_trans)
wall_2 = Wall([5000, 5000], [7000, 0], thick, rho_long, rho_trans)
wall_3 = Wall([5000, 0], [0, 0], thick, rho_long, rho_trans)
wall_4 = Wall([0, 0], [0, 7000], thick, rho_long, rho_trans)

section = CrossSection()
section.add_wall(wall_1)
section.add_wall(wall_2)
section.add_wall(wall_3)
section.add_wall(wall_4)
print(section)

# check if geometry is valid
valid, msg = section.valid()
if not valid:
    print('The defined geometry is not valid', msg)

# ----- Material -----
Mat = MatProp()
Mat.f_ck = 55.16
Mat.f_yk = 414.0
Mat.E_s = 200.0
Mat.alpha_cc = 0.85
Mat.gamma_c = 1.0
Mat.gamma_s = 1.0
Mat.update_strengths()  # in case default f_ck was changed
Mat.set_methods('EN Parabolic-rectangular', 'Elastic-plastic')
Mat.update_conc_stiffness()  # stiffnesses must be updated after strength update
print(Mat)

# ----- SectionForces -----
N = -200000
My = 230000
Mz = 0
Vy = 51100  # only ok with inequality
# Vy = 51210  # only ok with equality constraint
Vz = 0
T = 0
SF = SectionForces(N, My, Mz, Vy, Vz, T)
print(SF)

# ----- Analysis -----
print()
try:
    # result = Analysis.SLS_analysis(section, SF, Mat)
    result, error_msg = Analysis.ULS_analysis(section, SF, Mat, printing=True)
    print('error_msg:', error_msg)

except Analysis.MyOptimizerError as e:
    # caught a MyOptimizerError exception
    print('exception msg:', [str(e), e.discription])
