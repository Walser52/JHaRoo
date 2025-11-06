#Module for making geometries. 

from ase.build import bulk, cut
from ase.io import read, write
import numpy as np

def make_qd(
    material,
    size_nm,
    crystal_structure=None,
    lattice_constant=None,
    from_cif=False,
    cif_path=None,
    output="qd.xyz"
):
    """
    Create a roughly spherical quantum dot (QD) of desired size using ASE.
    
    Parameters
    ----------
    material : str
        Element symbol (e.g. 'Cu') or material name if from_cif=True.
    size_nm : float
        Desired QD diameter in nanometers.
    crystal_structure : str, optional
        ASE bulk crystal structure for elemental solids ('fcc', 'bcc', 'hcp', etc.)
        Required if from_cif=False.
    lattice_constant : float, optional
        Lattice constant (Å). Required if from_cif=False.
    from_cif : bool, default=False
        If True, builds the QD from a provided CIF file.
    cif_path : str, optional
        Path to the CIF file (used if from_cif=True).
    output : str, default='qd.xyz'
        Output file name.

    Returns
    -------
    qd : ase.Atoms
        ASE Atoms object of the quantum dot.
    """

    # Convert nm to Å
    radius = (size_nm * 10) / 2.0  # diameter → radius

    # === Load base structure ===
    if from_cif:
        if cif_path is None:
            raise ValueError("Please provide a cif_path when from_cif=True.")
        base = read(cif_path)
    else:
        if crystal_structure is None or lattice_constant is None:
            raise ValueError("Need crystal_structure and lattice_constant for elemental QD.")
        base = bulk(material, crystalstructure=crystal_structure, a=lattice_constant)

    # === Determine replication size ===
    # Replicate until the supercell comfortably exceeds the target radius
    cell_lengths = np.array(base.get_cell().lengths())
    reps = np.ceil((2 * radius) / cell_lengths).astype(int)
    supercell = base.repeat(reps)

    # === Cut spherical region ===
    qd = cut(supercell, a=(1,0,0), b=(0,1,0), c=(0,0,1),
             origo=(0,0,0), nlayers=None,
             radius=radius, center=(0,0,0), kind="sphere")

    # Center the QD in a big cell
    qd.center(vacuum=10.0)

    # Save
    write(output, qd)
    print(f"✅ Quantum dot created: {len(qd)} atoms, radius ~{radius:.2f} Å, saved as {output}")

    return qd

