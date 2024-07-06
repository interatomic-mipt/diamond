#Takes energies and forces from QE output
#and generates MTP's cfg file

from ase.io import read
import numpy as np
import sys

# Specify the path to your Quantum Espresso output file
qe_output_file = sys.argv[1]
out_name = sys.argv[2]

# Read the output file
atoms = read(qe_output_file)

# Extract useful information
positions = atoms.get_positions()
cell = atoms.get_cell()
energy = atoms.get_potential_energy()
forces = atoms.get_forces()
types = atoms.get_chemical_symbols()

# Function to write the required custom file format
def write_custom_format(filename, atoms, forces, energy,types):
    num_atoms = len(atoms)
    cell = atoms.get_cell()
    positions = atoms.get_positions()
    
    with open(filename, 'w') as f:
        f.write("BEGIN_CFG\n")
        f.write(" Size\n")
        f.write(f"    {num_atoms}\n")
        f.write(" Supercell\n")
        for vector in cell:
            f.write(f"    {vector[0]:.6f}    {vector[1]:.6f}    {vector[2]:.6f}\n")
        
        f.write(" AtomData:  id type       cartes_x      cartes_y      cartes_z           fx          fy          fz\n")
        for i, (pos, force, types) in enumerate(zip(positions, forces,types), start=1):
            if types == 'N':
                atom_type = 1
            else:
                atom_type = 0
            f.write(f"    {i:<5}{atom_type:<4}{pos[0]:>12.6f}{pos[1]:>12.6f}{pos[2]:>12.6f}"
                    f"{force[0]:>12.6f}{force[1]:>12.6f}{force[2]:>12.6f}\n")
        
        f.write(" Energy\n")
        f.write(f"    {energy:.12f}\n")
        
        # Stress tensor (NONE)
        stress = np.array([0, 0, 0, 0, 0, 0])
        f.write(" PlusStress:  xx          yy          zz          yz          xz          xy\n")
        f.write(f"    {stress[0]:.5f}    {stress[1]:.5f}    {stress[2]:.5f}    "
                f"{stress[3]:.5f}    {stress[4]:.5f}    {stress[5]:.5f}\n")
        
        f.write(" Feature   EFS_by       QE\n")
        f.write("END_CFG\n")

# Output file path
output_file = out_name+'.cfg'

# Write the custom file format
write_custom_format(output_file, atoms, forces, energy,types)

print(f"QE output written to {output_file}")

