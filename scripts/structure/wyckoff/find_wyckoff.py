#Finds the Wyckoff symmetry coordinates for a site.

from pymatgen.core.structure import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Load the structure from a CIF file
structure = Structure.from_file("/home/fes33/Downloads/Li10Ge(PS6)2(2).cif")

# Create a SpacegroupAnalyzer object
sga = SpacegroupAnalyzer(structure, symprec=1e-3)

# Get the symmetrized structure
symm_structure = sga.get_symmetrized_structure()

# Print basic space group info
print(f"Space group: {sga.get_space_group_symbol()} ({sga.get_space_group_number()})")
print()

# Loop over all symmetry-equivalent site groups and their Wyckoff symbols
print("Wyckoff positions and equivalent sites:")
for i, (site_group, wyckoff) in enumerate(zip(symm_structure.equivalent_sites, symm_structure.wyckoff_symbols)):
    print(f"Group {i+1}: Wyckoff position {wyckoff}")
    for site in site_group:
        species = site.species_string
        coords = site.frac_coords
        print(f"  - {species} at fractional coordinates: {coords}")
    print()

# Example: Find the Wyckoff position for site index 0 in the original structure
target_index = 0
target_site = structure[target_index]
for group, wyckoff in zip(symm_structure.equivalent_sites, symm_structure.wyckoff_symbols):
    if any(site.is_periodic_image(target_site) for site in group):
        print(f"Site index {target_index} ({target_site.species_string}) is in Wyckoff position: {wyckoff}")
        break

