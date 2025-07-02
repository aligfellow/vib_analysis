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

## Examples 
Sample python use in examples/ folder:
![sn2 imaginary mode](images/sn2.gif)
    - the gif is generated using [v.2.0](https://github.com/briling/v) ```v sn2.v006.xyz``` press `f` and then `q` ; then ```convert -delay 5 -loop 0 sn2*xpm sn2.gif```
From the command line:
  ``` vib_analysis sn2.v006.xyz ```

Gives:
```
#Analysed vibrational trajectory from bond_sn2.v006.xyz:

===== Significant Bond Changes =====
Bond (0, np.int64(4)): Δ = 1.584 Å, Initial Length = 1.717 Å
Bond (0, np.int64(5)): Δ = 1.356 Å, Initial Length = 1.952 Å
```

## Work in progress
For now can be installed locally by:
- ```git clone https://github.com/aligfellow/vib_analysis.git```
- ```cd vib_analysis```
- ```pip install .```
