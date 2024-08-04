import subprocess
import matplotlib.pyplot as plt
import numpy as np

def modify_input_file(input_file, output_file, ecutwfc, ecutrho):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            if 'ecutwfc' in line:
                line = f"  ecutwfc = {ecutwfc},\n"
            elif 'ecutrho' in line:
                line = f"  ecutrho = {ecutrho},\n"
            file.write(line)

def initialize_energy_file(energy_file):
    open(energy_file, 'w').close()

def runbash(output_file, command):
    try:
        with open(output_file, 'w') as out:
            result = subprocess.run(command, shell=True, check=True, stdout=out, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"Error in command: {command}")
                print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        return

def convOver(calc, input_file, output_file_template, energy_file, command):
    values = list(calc.items())[0][1]
    calc = list(calc.items())[0][0]

    initialize_energy_file(energy_file)

    for val in values:
        ecutwfc = val if calc == 'ecutwfc' else values[0] / 4
        ecutrho = 4 * ecutwfc if calc == 'ecutwfc' else val

        # Modify the input file with the current ecut value
        modified_input_file = f'pwscf_{calc}-{val}.in'
        modify_input_file(input_file, modified_input_file, ecutwfc, ecutrho)

        # Construct and run the command
        output_file = output_file_template.format(val)
        full_command = command.format(modified_input_file, output_file)
        print(f"Running command: {full_command}")
        runbash(output_file, full_command)
        writexy(output_file, energy_file, val)
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

def writexy(readfrom, writeto, x):
    y = extract_total_energy(readfrom)
    if y is not None:
        with open(writeto, 'a') as energy_fid:
            energy_fid.write(f"{x} {y}\n")
    else:
        print(f"Value not found in the output file for {x}.")
    return

def calculate_relative_errors(fromfile = None, data = None):

    if fromfile is not None: data = np.loadtxt(fromfile)[:, 1]
    
    relative_errors = []
    for i in range(1, len(data)):
        rel_error = abs((data[i] - data[i - 1]) / data[i])
        relative_errors.append(rel_error)
    return np.array(relative_errors)

def plotter(data, xlabel, ylabel, filename):
    ecut_values = data[:, 0]
    total_energies = data[:, 1]

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
