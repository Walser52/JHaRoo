from imp import modify_input_file, initialize_datafile, runbash, extract_total_energy, writexy, calculate_relative_errors, checkconv, convOver, update_input_file, plotter # type: ignore
import numpy as np
import matplotlib.pyplot as plt
def main():
    # __________________ Parameters of input file on which convergence has to run _________________________________
    calc = {
        'ecutwfc': [20, 24],
        'smearing': ['mv', 'mp']
    }

    # ______________________Initial Parameters for code__________________________
    params = {
        'template': 'pwscf.in',
        'command': 'mpirun -n 8 --mca btl vader,self,tcp pw.x < {} > {}',
        'over': 'etot'
    }

    # ____________________________Convergence _________________________________________
    for param in calc:
        datafile = convOver(calc={param: calc[param]},**params)

    # ________________________Plotting___________________________________________________
        data = np.genfromtxt(datafile, dtype=None, encoding=None, names=True)

        plotter(data, 
                xlabel=param, 
                ylabel='Total Energy (Ry)', 
                filename= f'convergence_{param}.pdf')



        # __________________________Create a file to Store Converged Values____________________________________
        converged_value = checkconv(datafile=params['datafile_template'].format(param, 'dat'), thresh=0.002)
        print(f"Converged {param}: {converged_value}")

        # Write the converged value to a separate file
        results_file = f'converged_{param}.dat'
        with open(results_file, 'a') as f:
            f.write(f"Converged {param}: {converged_value}\n")

    
    # _______________________Determine Converged values using checkconv function____________________________
    for param in calc:
        converged_value = checkconv(datafile=params['datafile_template'].format(param, 'dat'), thresh=0.002)
        with open(results_file, 'a') as f:
            f.write(f"Converged {param}: {converged_value}\n")

        # ____________________Update Input file with converged value of previous convergence_________________________
        update_input_file(params['input_file'], {param: converged_value})

        # _______________Converegnce for ecutrho__________________________________________
        if param == 'ecutwfc':
            ecutrho_values = [factor * converged_value for factor in [4, 6, 8, 10, 12]]
            calc['ecutrho'] = ecutrho_values

    # ____________________ Append Converged values___________________________________________
    for param in calc:
        with open(f'converged_{param}.dat', 'a') as f:
            f.write(f"Converged {param}: {converged_value}\n")

if __name__ == "__main__":
    main()
