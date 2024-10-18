from jhr.cleaners.bandsQE import bandHandlerQE

#Define High Symmetry Points
high_symmetry_points = {
    'gG1'   : 0,
    'X1'    : 30,
    'M1'    : 60,
    'gG2'   : 90,
    'R1'    : 120,
    'X2|M2' : 150,
    'R2'    : 180
}
data_file = '/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/Abinitio-Codes/data/band_files/CsPbBr2I.bands.gnu'


_, _, _, _, homolumo, bandgap = bandHandlerQE(data_file,high_symmetry_points, efermi = 1.9, index = [14, 23])

