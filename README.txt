A working command line and python package to read in vibrational trajectories and return the internal coordinates associated with the vibration.

Requires a *trj.xyz file
Currently, this has been written for orca.out
orca_pltvib <orca>.out 6 # first vibrational mode

In the future this may be able to read orca.out and gaussian.log files directly, rather than requiring a trj.xyz file.

##Examples 

Sample python use in examples/ folder:

