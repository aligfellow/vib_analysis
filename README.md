# A command line and python package to read in vibrational trajectories and return the internal coordinates associated with the vibration.

- Requires a ```*trj.xyz``` file
  - of the structure:
```
[n_atoms]
comment line
<atomic symbol/number> <x> <y> <z>
... ... ... ... 
```
- Currently, this has been written for orca.out
  - _e.g._ ```orca_pltvib <orca>.out 6 ```# first vibrational mode
  - this could also come from using [pyQRC](https://github.com/patonlab/pyQRC) from R. Paton
  
     - could run a loop of amplitudes to generate individual xyz trj files
     
In the future this may be able to read orca.out and gaussian.log files directly, rather than requiring a trj.xyz file.

## Installation
For now can be installed locally by:
- ```git clone https://github.com/aligfellow/vib_analysis.git```
- ```cd vib_analysis```
- ```pip install .```

## Command line interface
```
vib_analysis -h
usage: vib_analysis [-h] [--bond_tolerance BOND_TOLERANCE] [--angle_tolerance ANGLE_TOLERANCE]
                    [--dihedral_tolerance DIHEDRAL_TOLERANCE] [--bond_threshold BOND_THRESHOLD]
                    [--angle_threshold ANGLE_THRESHOLD] [--all]
                    xyz_file

Internal Coordinate Displacement Analyzer

positional arguments:
  xyz_file              Path to XYZ trajectory file.

options:
  -h, --help            show this help message and exit
  --bond_tolerance BOND_TOLERANCE
                        Bond detection tolerance multiplier.
  --angle_tolerance ANGLE_TOLERANCE
                        Angle detection tolerance multiplier.
  --dihedral_tolerance DIHEDRAL_TOLERANCE
                        Dihedral detection tolerance multiplier.
  --bond_threshold BOND_THRESHOLD
                        Minimum internal coordinate change to report.
  --angle_threshold ANGLE_THRESHOLD
                        Minimum angle change in degrees to report.
  --all                 Report all changes in angles and dihedrals.
```                 
Python interface similarly:

## Minimal Examples 
Sample python use in examples/ folder:
![sn2 imaginary mode](images/sn2.gif)
    - the gif is generated using [v.2.0](https://github.com/briling/v) ```v sn2.v006.xyz``` press `f` and then `q` ; then ```convert -delay 5 -loop 0 sn2*xpm sn2.gif```
From the command line:
  ``` vib_analysis sn2.v006.xyz ```

Gives:
```
Analysed vibrational trajectory from bond_sn2.v006.xyz:

===== Significant Bond Changes =====
Bond (0, np.int64(4)): Δ = 1.584 Å, Initial Length = 1.717 Å
Bond (0, np.int64(5)): Δ = 1.356 Å, Initial Length = 1.952 Å
```
The magnitude and change (Δ) of the modes is somewhat meaningless, though this should report the initial value of the 1st frame (or reference frame).

Another example:
![dihedral imaginary mode](images/dihedral.gif)
```vib_analysis dihedral.v006.xyz```

Results in:
```
Analysed vibrational trajectory from dihedral.v006.xyz:

===== Significant Dihedral Changes =====
Dihedral (np.int64(6), 0, np.int64(3), np.int64(7)): Δ = 39.556 degrees, Initial Value = 359.998 degrees
```

The bond changes are hierarchical, so an angle with a large change as a consequence of a bonding change is not reported as a *significant* change.
Another:
![larger molecule sn2](images/large.gif)
```vib_analysis large.v006.xyz```

```
Analysed vibrational trajectory from orca_ts.v006.xyz:

===== Significant Bond Changes =====
Bond (0, np.int64(1)): Δ = 1.195 Å, Initial Length = 2.807 Å
Bond (1, np.int64(47)): Δ = 0.706 Å, Initial Length = 2.168 Å
```

## Further Examples
Complex transformation with BIMP catalysed rearrangement
![bimp rearrangement](images/bimp.gif)
```vib_analysis bimp.v006.xyz```

```
Analysed vibrational trajectory from SR_0070_TS.v006.xyz:

===== Significant Bond Changes =====
Bond (11, np.int64(12)): Δ = 1.432 Å, Initial Length = 2.064 Å

===== Significant Dihedral Changes =====
Dihedral (np.int64(32), 14, np.int64(15), np.int64(20)): Δ = 30.937 degrees, Initial Value = 350.826 degrees
Dihedral (np.int64(31), 13, np.int64(14), np.int64(32)): Δ = 29.557 degrees, Initial Value = 185.910 degrees
Dihedral (np.int64(88), 85, np.int64(87), np.int64(92)): Δ = 13.860 degrees, Initial Value = 186.215 degrees
Dihedral (np.int64(92), 87, np.int64(91), np.int64(97)): Δ = 13.702 degrees, Initial Value = 45.805 degrees
Dihedral (np.int64(14), 13, np.int64(31), np.int64(33)): Δ = 11.470 degrees, Initial Value = 170.957 degrees

Note: These dihedrals are not directly dependent on other changes however they may be artefacts of other motion in the TS.
```
- correctly identifies the bond change between atoms 11 and 12, though perhaps misses a weakly correlated bonding change of 10 and 14
- identifies extra dihedrals for now - atoms 13, 14, 15 featured as neighbours of the bonding change
- also picking up motion of the thiourea protons that have strong NCIs with the substrate
- this may have suffered from a poor internal coordinate construction

more detailed:
```vib_analysis bimp.v006.xyz --all```

```
Analysed vibrational trajectory from SR_0070_TS.v006.xyz:

===== Significant Bond Changes =====
Bond (11, np.int64(12)): Δ = 1.432 Å, Initial Length = 2.064 Å

===== Significant Dihedral Changes =====
Dihedral (np.int64(32), 14, np.int64(15), np.int64(20)): Δ = 30.937 degrees, Initial Value = 350.826 degrees
Dihedral (np.int64(31), 13, np.int64(14), np.int64(32)): Δ = 29.557 degrees, Initial Value = 185.910 degrees
Dihedral (np.int64(88), 85, np.int64(87), np.int64(92)): Δ = 13.860 degrees, Initial Value = 186.215 degrees
Dihedral (np.int64(92), 87, np.int64(91), np.int64(97)): Δ = 13.702 degrees, Initial Value = 45.805 degrees
Dihedral (np.int64(14), 13, np.int64(31), np.int64(33)): Δ = 11.470 degrees, Initial Value = 170.957 degrees

Note: These dihedrals are not directly dependent on other changes however they may be artefacts of other motion in the TS.

===== Minor Angle Changes =====
Angle (np.int64(13), 12, np.int64(29)): Δ = 11.020 degrees, Initial Value = 122.116 degrees

Note: These angles are dependent on other changes and may not be significant on their own.

===== Less Significant Dihedral Changes =====
Dihedral (np.int64(29), 12, np.int64(13), np.int64(31)): Δ = 48.971 degrees, Initial Value = 17.521 degrees
Dihedral (np.int64(2), 1, np.int64(10), np.int64(11)): Δ = 35.026 degrees, Initial Value = 194.336 degrees

Note: These dihedrals are dependent on other changes and may not be significant on their own.
```

## Work in progress
This is a work in progress and will hopefully improve at some point in the future...
Feel free to contribute and ask any questions
