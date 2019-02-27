# HollowRC
A Python executable for general design of hollow reinforced concrete sections under combined actions

## Getting Started - Installation
1. Download the latest release from https://github.com/Kleissl/HollowRC/releases/latest
2. Unzip the distribution package
3. Execute HollowRC.exe

## About
This is an easy to use design tool for analysis of hollow reinforced concrete sections under combined loading, fully embracing the interactions between bending and shear behaviour.
To propor describe the interaction between the flow of normal stesses and shear stress and to fully utilize the capacity of the cross-section one must leave the simplfied approach of the diagonal truss model.
For a linear-elastic material one could apply the Grashof's formula, similar to analysis of thin-walled steel-sections, to determining shear flow etc. 
However, with the basic assumption of linear-elastic material behaviour being unsuitable for reinforced concrete, a more numerical extensive approach involving a series of optimization routines needs to be adopted.
To make this analysis method more approachable, this easy to use application has been developed.

### Service Limit State
This design tool will provide designers with a superior insight into the actual stress state during Service Limit State (SLS), including the shear or torsion induced stresses in the transverse reinforcement (in the circumferential direction), and will completely avoid any superposition of plastic lower bound methods from the diagonal truss model, additional shear-induced demand for longitudinal reinforcement and the corresponding strain incompatibilities introduced by separating shear and bending analysis.
For SLS the actual shear flow is determined based on a plane dual-section analysis, which just means that two nabouring plane-sections are analysed and from their differences in normal flow, simple equilibrium yields the corresponding shear flow distribution.
So only by applying the fundamental flexural member assumption of plane sections must remain plane combined with basic equilibrium equations can the actual normal and shear flow distributions be determined.
From this an in-plane membrane analysis is used to determined the reinforcement stresses etc. by choosing the resulting compressive stress direction / strut angle such that it minimizes the complementary strain energy (similar to fulfilling compatibility).

### Ultimate Limit State
For Ultimate Limit State (ULS) this design tool will allow designers to push the capacity of the cross-section even further, as it by use of mathematical optimization algorithms are able to identify the true optimal plastic lower-bound solution that fully utilize the strength of the materials.
For ULS a classic plane section analysis is performed and from its normal flow distribution, an in-plane membrane analysis considering the yield conditions determines the leftover shear flow capacity at any given point along the cross-section, which then is integrated into a shear force capacity for each of the cross-sectional wall elements. Finally this is followed up by solving the optimization problem of maximizing the load-factor while maintaining equalibrium between the wall shear forces and the user specified global sectional forces.

### Assumptions and limitations
The implementation is based on the following assumptions:
- The span to depth ratio of the section is sufficient for beam theory to be applicable where plane section analysis approach is considered.
- The walls are sufficient thin, compared to the cross-section dimensions, for a thin-walled approach to be applicable.
- Normal stresses in the circumferential direction are neglected even though equilibrium in principle requires the presence of these. This is a common approach when analysing thin-walled sections.

## Documentation
Further documention with figures etc. will follow...

### Sign convention
Axes:
* Positive x towards right
* Positive y upward
* The sign convention generally follows a left hand system (LHS)

Geometry:
* All dimension are in millimeters
* The section must be defined in the clock-wise direction
* Angles are taken positive in the counter-clockwise direction starting from the x-axis

Flows & Stresses:
* Normal flow and normal stress are positive for tension
* Shear flow is positive in the counter-clockwise direction

Section forces:
* Positive Mx moment yields compression in the top
* Positive My moment yields compression on the left side
* Negative N (normal force) yields compression
* Positive Vx yields shear in the x-direction (right)
* Positive Vy yields shear in the y-direction (upward)
* Positive T (torsion) yields counter-clockwise shear flow

## Issues
If you experience a problem with the application package please raise an issue on this GitHub repository. 

## Versioning
For the versions available, see the [tags on this repository](https://github.com/Kleissl/HollowRC/tags). 

## Author
**Kenneth C. Kleissl** - [Kleissl](https://github.com/Kleissl)

## License
The HollowRC project is licensed under the GNU GPL license, so any code using it must also be under the same license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
* Thanks to the COWI Foundation for funding the development of the concept and drafting of the first working version.
* Thanks to João Luís Domingues Costa for valuable discussions and feedback to the project
