#!/usr/bin/env python3
# convert.py
import os
import sys
import argparse
import numpy as np
from ase import Atoms
from ase.io import read
import cclib

def get_orca_pltvib_path():
    """Find orca_pltvib executable in the same directory as orca"""
    orca_path = os.popen('which orca').read().strip()
    if not orca_path:
        raise RuntimeError("ORCA not found in PATH. Please ensure ORCA is installed.")
    
    orca_dir = os.path.dirname(orca_path)
    pltvib_path = os.path.join(orca_dir, 'orca_pltvib')
    
    if not os.path.exists(pltvib_path):
        raise RuntimeError(f"orca_pltvib not found at {pltvib_path}")
    
    return pltvib_path

def get_orca_frequencies(orca_file):
    """Extract vibrational frequencies from ORCA output"""
    with open(orca_file, 'r') as f:
        lines = f.readlines()
    
    section_indices = [i for i, line in enumerate(lines) if "VIBRATIONAL FREQUENCIES" in line]
    if not section_indices:
        raise ValueError("No vibrational frequencies section found in ORCA output.")
    
    idx = section_indices[-1] # last occurence if multiple are present
    freqs = []
    
    for line in lines[idx:]:
        if "NORMAL MODES" in line:
            break
        parts = line.split(':')
        if len(parts) > 1:
            try:
                freq = float(parts[1].split()[0])
                freqs.append(freq)
            except (ValueError, IndexError):
                continue
    return freqs

def convert_orca(orca_file, mode):
    """Convert ORCA output to vibration trajectory files"""
    pltvib = get_orca_pltvib_path()
    basename = os.path.splitext(orca_file)[0]
    
    # Generate vibration files using orca_pltvib
    os.system(f'{pltvib} {orca_file} {mode} > /dev/null 2>&1')

    # Process each mode file
    orca_vib = f'{basename}.out.v{mode:03d}.xyz'
    xyz_vib = f'{basename}.v{mode:03d}.xyz'

    if not os.path.exists(orca_vib):
        raise FileNotFoundError(f"File {orca_vib} not found. Ensure ORCA output is correct.")

    with open(orca_vib, 'r') as f:
        lines = f.readlines()
    
    # Process frames
    xyz_len = int(lines[0].split()[0]) + 2
    xyzs = [lines[i:i+xyz_len] for i in range(0, len(lines), xyz_len)]
    
    # Clean and write new file
    with open(xyz_vib, 'w') as f:
        for idx in xyzs:
            # Keep header lines (atom count and comment)
            f.write(idx[0])
            f.write(f"Mode {mode} Frame: {idx[1]}")

            # Process atom lines (keep only symbol and coordinates)
            for line in idx[2:]:
                parts = line.split()
                f.write(f"{parts[0]} {parts[1]} {parts[2]} {parts[3]}\n")
    
    # Remove temporary file
    os.remove(orca_vib)
    return xyz_vib

def parse_cclib_output(output_file, mode, amplitudes=None):
    """Convert Gaussian/ORCA/other output to vibration trajectory files for a single mode with cclib"""
    mode = int(mode)
    if amplitudes is None:
        amplitudes = [0.0, -0.2, -0.4, -0.6, -0.8, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2]
        # amplitudes = [0.0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1]

    # Parse file with cclib
    parser = cclib.io.ccopen(output_file)
    data = parser.parse()

    freqs = data.vibfreqs
    if len(freqs) == 0:
        raise ValueError("No vibrational frequencies found in file.")

    # Validate mode index
    num_modes = len(data.vibfreqs)
    if mode < 0 or mode >= num_modes:
        raise ValueError(f"Mode index {mode} out of range. File has {num_modes} modes.")
    # === Prepare geometry and displacement ===
    atom_numbers = data.atomnos
    atom_symbols = [Atoms(numbers=[z]).get_chemical_symbols()[0] for z in atom_numbers]
    eq_coords = data.atomcoords[-1]
    displacement = np.array(data.vibdisps[mode])
    freq = freqs[mode]

    # Output file
    base = os.path.splitext(output_file)[0]
    out_xyz = f"{base}.v{mode:03d}.xyz"

    with open(out_xyz, 'w') as f:
        for amp in amplitudes:
            displaced = eq_coords + amp * displacement
            f.write(f"{len(atom_numbers)}\n")
            f.write(f"Mode: {mode}, Frequency: {freq:.2f} cm**-1, Amplitude: {amp:.2f}\n")
            for sym, coord in zip(atom_symbols, displaced):
                f.write(f"{sym} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

    print(f"Written trajectory to: {out_xyz}")
    return freqs, out_xyz
    
