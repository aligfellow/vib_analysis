import argparse
from .core import analyze_internal_displacements, read_xyz_trajectory, calculate_bond_length, calculate_angle, calculate_dihedral
from .convert import parse_cclib_output, get_orca_frequencies, convert_orca

def print_analysis_results(results, args):
    if results['bond_changes']:
        print("\n===== Significant Bond Changes =====")
        for bond, (change, initial_value) in sorted(results['bond_changes'].items(), key=lambda x: -x[1][0]):
            print(f"Bond {bond}: Δ = {change:.3f} Å, Initial = {initial_value:.3f} Å")

    if results['angle_changes']:
        print("\n===== Significant Angle Changes =====")
        for angle, (change, initial_value) in sorted(results['angle_changes'].items(), key=lambda x: -x[1][0]):
            print(f"Angle {angle}: Δ = {change:.3f}°, Initial = {initial_value:.3f}°")

    if results['dihedral_changes']:
        print("\n===== Significant Dihedral Changes =====")
        for dihedral, (change, initial_value) in sorted(results['dihedral_changes'].items(), key=lambda x: -x[1][0]):
            print(f"Dihedral {dihedral}: Δ = {change:.3f}°, Initial = {initial_value:.3f}°")
        if results['bond_changes'] or results['angle_changes']:
            print("\nNote: These dihedrals are not directly dependent on other changes however they may be artefacts of other motion in the TS.")

    if args.all:
        if results['minor_angle_changes']:
            print("\n===== Minor Angle Changes =====")
            for angle, (change, initial_value) in sorted(results['minor_angle_changes'].items(), key=lambda x: -x[1][0]):
                print(f"Angle {angle}: Δ = {change:.3f}°, Initial = {initial_value:.3f}°")
            print("\nNote: These angles are dependent on other changes and may not be significant on their own.")

        if results['minor_dihedral_changes']:
            print("\n===== Less Significant Dihedral Changes =====")
            for dihedral, (change, initial_value) in sorted(results['minor_dihedral_changes'].items(), key=lambda x: -x[1][0]):
                print(f"Dihedral {dihedral}: Δ = {change:.3f}°, Initial = {initial_value:.3f}°")
            print("\nNote: These dihedrals are dependent on other changes and may not be significant on their own.")

def print_first_5_nonzero_modes(freqs, args):
    """Print the first 5 non-zero vibrational modes with proper handling"""
    # Filter out zero frequencies and get first 5
    non_zero = [f for f in freqs if abs(f) > 1e-5][:5]
    
    print("\nFirst 5 non-zero vibrational frequencies:")
    for i, freq in enumerate(non_zero):
        # Add note for imaginary frequencies
        note = " (imaginary)" if freq < 0 else ""
        print(f"  Mode {i}: {freq:.2f} cm**-1 {note}")

def run_vib_analysis(
    input_file,
    mode=None,
    parse_cclib=False,
    parse_orca=False,
    bond_tolerance=1.5,
    angle_tolerance=1.1,
    dihedral_tolerance=1.0,
    bond_threshold=0.5,
    angle_threshold=10.0,
    dihedral_threshold=20.0,
    ts_frame=False,
    report_all=False,
    print_output=False,
    ):
    
    if parse_cclib or parse_orca:
        if mode is None:
            raise ValueError("Mode index is required for Gaussian/ORCA conversion")

        if parse_cclib:
            freqs, trj_file = parse_cclib_output(input_file, mode)
        elif parse_orca:
            freqs = get_orca_frequencies(input_file)
            trj_file = convert_orca(input_file, mode)

        if print_output:
            print_first_5_nonzero_modes(freqs, argparse.Namespace(parse_orca=parse_orca))

        results = analyze_internal_displacements(
            trj_file,
            bond_tolerance=bond_tolerance,
            angle_tolerance=angle_tolerance,
            dihedral_tolerance=dihedral_tolerance,
            bond_threshold=bond_threshold,
            angle_threshold=angle_threshold,
            dihedral_threshold=dihedral_threshold,
            ts_frame=ts_frame,
        )

        if print_output:
            print(f"\nAnalysed vibrational trajectory (Mode {mode} with frequency {freqs[mode]} cm**-1):")
            print_analysis_results(results, argparse.Namespace(all=report_all))

    else:
        # XYZ direct analysis
        results = analyze_internal_displacements(
            input_file,
            bond_tolerance=bond_tolerance,
            angle_tolerance=angle_tolerance,
            dihedral_tolerance=dihedral_tolerance,
            bond_threshold=bond_threshold,
            angle_threshold=angle_threshold,
            dihedral_threshold=dihedral_threshold,
            ts_frame=ts_frame,
        )

        if print_output:
            print(f"\nAnalysed vibrational trajectory from {input_file}:")
            print_analysis_results(results, argparse.Namespace(all=report_all))

    return results

def main():
    parser = argparse.ArgumentParser(description="Vibrational Mode Analysis Tool")
    parser.add_argument("input", help="Input file (XYZ trajectory, ORCA output, or Gaussian log)")
    parser.add_argument("--parse_cclib", action="store_true", help="Process Gaussian/ORCA/other output file instead of XYZ trajectory: requires --mode !0 indexed!")
    parser.add_argument("--parse_orca", action="store_true", help="Parse ORCA output file instead of XYZ trajectory: requires --mode !orca indexed! - ie 6 for first mode (3N-6)")
    parser.add_argument("--mode", type=int, help="Mode index to analyze (for Gaussian/ORCA conversion)")
    
    # Analysis parameters
    parser.add_argument("--bond_tolerance", type=float, default=1.5, help="Bond detection tolerance multiplier. Default: 1.5")
    parser.add_argument("--angle_tolerance", type=float, default=1.1, help="Angle detection tolerance multiplier. Default: 1.1")
    parser.add_argument("--dihedral_tolerance", type=float, default=1.0, help="Dihedral detection tolerance multiplier. Default: 1.0")
    parser.add_argument("--bond_threshold", type=float, default=0.5, help="Minimum internal coordinate change to report. Default: 0.5")
    parser.add_argument("--angle_threshold", type=float, default=10.0, help="Minimum angle change in degrees to report. Default: 10")
    parser.add_argument("--dihedral_threshold", type=float, default=20.0, help="Minimum dihedral change in degrees to report. Default: 20")
    parser.add_argument("--ts_frame", action='store_true', default=0, help="TS frame for distances and angles in the TS. Default: 0 (first frame)")
    parser.add_argument("--all", action='store_true', default=False, help="Report all changes in angles and dihedrals.")

    args = parser.parse_args()

    run_vib_analysis(
            input_file=args.input,
            mode=args.mode,
            parse_cclib=args.parse_cclib,
            parse_orca=args.parse_orca,
            bond_tolerance=args.bond_tolerance,
            angle_tolerance=args.angle_tolerance,
            dihedral_tolerance=args.dihedral_tolerance,
            bond_threshold=args.bond_threshold,
            angle_threshold=args.angle_threshold,
            dihedral_threshold=args.dihedral_threshold,
            ts_frame=args.ts_frame,
            report_all=args.all,
            print_output=True,
        )

if __name__ == "__main__":
    main()