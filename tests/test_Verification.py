"""
Unit testing of the Verification class
"""
# imports
import pytest
from HollowRC.Verification import Verify
from HollowRC.Material import MatProp

# tolerance level
tol = 10**-4


@pytest.mark.parametrize("comp_stress", [-0.1, -2, -10.2])
def test_strut_angle1(comp_stress):
    stress = [comp_stress, 0, 0]
    Mat = MatProp()
    rho_sx = 0.01
    rho_sy = 0.01
    disk = Verify(stress, Mat, rho_sx, rho_sy)
    theta = disk.cracked_strut_angle()
    assert abs(theta - 0) < tol


@pytest.mark.parametrize("comp_stress", [-0.1, -2, -10.2])
def test_strut_angle2(comp_stress):
    stress = [0, comp_stress, 0]
    Mat = MatProp()
    rho_sx = 0.01
    rho_sy = 0.01
    disk = Verify(stress, Mat, rho_sx, rho_sy)
    theta = disk.cracked_strut_angle()
    assert abs(theta - 90) < tol


@pytest.mark.parametrize("shear_stress", [-7.5, -2, 0, 2.5, 100])
def test_strut_angle3(shear_stress):
    stress = [0, 0, shear_stress]
    Mat = MatProp()
    rho_sx = 0.01
    rho_sy = 0.01
    disk = Verify(stress, Mat, rho_sx, rho_sy)
    theta = disk.cracked_strut_angle()
    assert abs(theta - 45) < tol


@pytest.mark.parametrize("comp_stress", [-0.1, -2, -10.2])
def test_equilibrium1(comp_stress):
    stress = [comp_stress, 0, 0]
    Mat = MatProp()
    rho_sx = 0.0000001  # the check only applied to 
    rho_sy = 0.0000001
    disk = Verify(stress, Mat, rho_sx, rho_sy)
    theta = 0
    stresses = disk.cracked_equilibrium(theta)
    assert abs(stresses['sigma_c'] - comp_stress) < tol
    # assert abs(stresses['sigma_sx'] - 0) < tol
    assert abs(stresses['sigma_sy'] - 0) < tol
