import subprocess
import matplotlib.pyplot as plt
import numpy as np

def modify_input_file(input_file, output_file, **kwargs):
    """Update the input file with various parameter values."""
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            updated_line = line
            for param, value in kwargs.items():
                if param in line:
                    if isinstance(value, str):
                        # Add quotes around string values
                        updated_line = f"  {param} = '{value}',\n"
                    else:
                        # For non-string values
                        updated_line = f"  {param} = {value},\n"
                    break  # Break after updating the line for the specific parameter
            file.write(updated_line)

def initialize_datafile(datafile):
    open(datafile, 'w').close()
    return

def runbash(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Error in command: {command}")
            print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return


def convOver(calc, input_file, outfile_template, datafile_template, command):
    for param, values in calc.items():
        datafile = datafile_template.format(param, 'dat')
        initialize_datafile(datafile)

        for val in values:
            # Modify the input file with the current parameter value
            modified_input_file = f'pwscf_{param}-{val}.in'
            modify_input_file(input_file, modified_input_file, **{param: val})

            # Construct and run the command
            output_file = outfile_template.format(param, val)
            full_command = command.format(modified_input_file, output_file)
            print(f"Running command: {full_command}")
            runbash(full_command)
            writexy(output_file, datafile, val)

    return


def writexy(readfrom, writeto, x):
    y = extract_total_energy(readfrom)
    if y is not None:
        with open(writeto, 'a') as energy_fid:
            energy_fid.write(f"{x} {y}\n")
    else:
        print(f"Value not found in the output file for {x}.")
    return


def extract_total_energy(output_file):
    with open(output_file, 'r') as file:
        for line in file:
            if '!' in line and 'total energy' in line:
                # Split the line based on '=' to isolate the total energy value
                parts = line.split('=')
                if len(parts) > 1:
                    # Extract and clean the energy value part
                    energy_str = parts[1].strip()
                    try:
                        # The energy value is expected to be the first item in the cleaned part
                        return float(energy_str.split()[0])
                    except ValueError:
                        print(f"Error converting value to float in line: {line.strip()}")
                        return None
    return None



def calculate_relative_errors(datafile = None, data = None):

    if datafile is not None: data = np.loadtxt(datafile)[:, 1]
    
    relative_errors = []
    for i in range(1, len(data)):
        rel_error = abs((data[i] - data[i - 1]) / data[i])
        relative_errors.append(rel_error)
    return np.array(relative_errors)


def checkconv(datafile = None, thresh=0.001):
    """Returns value over which convergence is achieved"""
    data = np.loadtxt(datafile)
    x = data[:, 0]
    y = data[:, 1]
    relative_errors = calculate_relative_errors(data = y)

    convergedVal = None
    for i, rel_error in enumerate(relative_errors):
        if rel_error < thresh:
            convergedVal = x[i]
            break

    if convergedVal is None:
      convergedVal = x[-1]

    return convergedVal

def update_input_file(input_file, params):
    """Update the input file with the converged values for multiple parameters."""
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(input_file, 'w') as file:
        for line in lines:
            # Check for each parameter in the line and update if necessary
            updated = False
            for param, value in params.items():
                if param in line:
                    file.write(f'{param} = {value}\n')
                    updated = True
                    break
            if not updated:
                file.write(line)




def plotter(data, xlabel, ylabel, filename):
    ecut_values = data['parameter']
    total_energies = data['total_energy']

    plt.figure(figsize=(10, 6))
    plt.plot(ecut_values, total_energies, marker='o', linestyle='-', color='b', label='Total Energy')

    plt.title(f'Convergence Test: {xlabel} vs {ylabel}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    return 
 # type: ignore
