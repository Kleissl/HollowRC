# HollowRC
A Python executable for general design of hollow reinforced concrete sections under combined actions

## Getting Started - Installation
1. Download the latest release from https://github.com/Kleissl/HollowRC/releases/latest
2. Unzip the distribution package
3. Execute HollowRC.exe

## About
This is a design tool for analysis of hollow reinforced concrete sections under combined loading, fully embracing the interactions between bending and shear behaviour.
The complete interaction between bending and shear meant replacing the simple diagonal truss model with a more numerical extensive approach evolving a series of numerical optimization routines all based on achieving better fulfilment of equilibrium and for Service Limit State also elastic complementary energy for strain compatibility. The designer will therefore not need to deal with additional longitudinal reinforcement to cope with a separate shear demand.
The approach is similar to applying the Grashof's formula for thin-walled steel-sections for determining shear flow etc. however here without the basic assumption of linear elastic material behaviour unsuitable for reinforced concrete.
This method will provide designers with a superior insight into the actual stress state during Service Limit State including the transverse reinforcement in the circumferential direction and will avoid any superposition of lower bound methods and the corresponding strain compatibility violations typically applied with separate shear and bending analysis.
For Ultimate Limit State this tool will allow for an enhanced capacity of the cross-section as it determines an optimal shear flow distribution within the yield conditions of reinforced disks.

### Assumptions and limitations
The implementation is based on the following assumptions:
- The span to depth ratio of the section is sufficient for beam theory to be applicable where plane section analysis approach is considered.
- The walls are sufficient thin, compared to the cross-section dimensions, for a thin-walled approach to be applicable.
- Normal stresses in the circumferential direction are neglected even though equilibrium in principle requires the presence of these. This is a common approach when analysing thin-walled sections.

## Documentation
...

Sign convention:
Axis
- Positive x towards right
- Positive y upward
Geometry
- The section must be defined in the clock-wise direction
- Angles are taken positive in the counter-clockwise direction starting from the x-axis
Section forces
- Positive Mx moment yields compression in the top
- Positive My moment yields compression on the left side
- Negative N (normal force) yields compression
- Positive Vx yields shear in the x-direction (right)
- Positive Vy yields shear in the y-direction (upward)
- Positive T (torsion) yields counter-clockwise shear flow
Note that the above sign definitions follows a left hand system (LHS)

## Issues
If you experience a problem with the application package please raise an issue on this GitHub repository. 

## Versioning
For the versions available, see the [tags on this repository](https://github.com/Kleissl/HollowRC/tags). 

## Author
**Kenneth C. Kleissl** - [Kleissl](https://github.com/Kleissl)

## License
The HollowRC project is licensed under the GNU GPL license, so any code using it must also be under the same license - see the [LICENSE](LICENSE) file for details

## Acknowledgments
* Thanks to the COWI Foundation for funding the development of the concept and drafting of the first working version.
* Thanks to João Luís Domingues Costa for valuable discussions and feedback to the project
