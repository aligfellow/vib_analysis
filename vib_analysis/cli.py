import argparse
from .core import analyze_internal_displacements, read_xyz_trajectory, calculate_bond_length, calculate_angle, calculate_dihedral

def main():
    parser = argparse.ArgumentParser(description="Internal Coordinate Displacement Analyzer")
    parser.add_argument("xyz_file", help="Path to XYZ trajectory file.")
    parser.add_argument("--bond_tolerance", type=float, default=1.5, help="Bond detection tolerance multiplier.")
    parser.add_argument("--angle_tolerance", type=float, default=1.1, help="Angle detection tolerance multiplier.")
    parser.add_argument("--dihedral_tolerance", type=float, default=1.0, help="Dihedral detection tolerance multiplier.")
    parser.add_argument("--bond_threshold", type=float, default=0.5, help="Minimum internal coordinate change to report.")
    parser.add_argument("--angle_threshold", type=float, default=10.0, help="Minimum angle change in degrees to report.")
    parser.add_argument("--all", action='store_true', default=False, help="Report all changes in angles and dihedrals.")

    args = parser.parse_args()

    results = analyze_internal_displacements(
        args.xyz_file,
        bond_tolerance=args.bond_tolerance,
        angle_tolerance=args.angle_tolerance,
        dihedral_tolerance=args.dihedral_tolerance,
        bond_threshold=args.bond_threshold,
        angle_threshold=args.angle_threshold,
    )
    print(f"Analysed vibrational trajectory from {args.xyz_file}:")

    initial_geom = read_xyz_trajectory(args.xyz_file)[0]

    if results['bond_changes']:
        print("\n===== Significant Bond Changes =====")
        for bond, (change, initial_value) in sorted(results['bond_changes'].items(), key=lambda x: -x[1][0]):
            print(f"Bond {bond}: Δ = {change:.3f} Å, Initial Length = {initial_value:.3f} Å")


    if results['angle_changes']:
        print("\n===== Significant Angle Changes =====")
        for angle, (change, initial_value) in sorted(results['angle_changes'].items(), key=lambda x: -x[1][0]):
            print(f"Angle {angle}: Δ = {change:.3f} degrees, Initial Value = {initial_value:.3f} degrees")

    if results['dihedral_changes']:
        print("\n===== Significant Dihedral Changes =====")
        for dihedral, (change, initial_value) in sorted(results['dihedral_changes'].items(), key=lambda x: -x[1][0]):
            print(f"Dihedral {dihedral}: Δ = {change:.3f} degrees, Initial Value = {initial_value:.3f} degrees")
        if results['bond_changes'] or results['angle_changes']:
            print("\nNote: These dihedrals are not directly dependent on other changes however they may be artefacts of other motion in the TS.")

    if args.all:
        if results['minor_angle_changes']:
            print("\n===== Minor Angle Changes =====")
            for angle, (change, initial_value) in sorted(results['minor_angle_changes'].items(), key=lambda x: -x[1][0]):
                print(f"Angle {angle}: Δ = {change:.3f} degrees, Initial Value = {initial_value:.3f} degrees")
            print("\nNote: These angles are dependent on other changes and may not be significant on their own.")

        if results['minor_dihedral_changes']:
            print("\n===== Less Significant Dihedral Changes =====")
            for dihedral, (change, initial_value) in sorted(results['minor_dihedral_changes'].items(), key=lambda x: -x[1][0]):
                print(f"Dihedral {dihedral}: Δ = {change:.3f} degrees, Initial Value = {initial_value:.3f} degrees")
            print("\nNote: These dihedrals are dependent on other changes and may not be significant on their own.")

if __name__ == "__main__":
    main()