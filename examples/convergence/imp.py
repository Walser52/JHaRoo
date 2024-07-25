# imp.py
import matplotlib.pyplot as plt

# Function to modify the ecutwfc value in the input file
def modify_input_file(input_file, output_file, ecut):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            if 'ecutwfc' in line:
                line = f"  ecutwfc = {ecut},\n"
            file.write(line)

# Function to extract the total energy from the output file
def extract_total_energy(output_file):
    with open(output_file, 'r') as file:
        for line in file:
            if '!' in line:
                words = line.split()
                return float(words[4])
    return None

# Function to plot

def plotter(data):
# Separate the data into two columns
    ecut_values = data[:, 0]
    second_column = data[:, 1]

  # Step 3: Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(ecut_values, second_column, marker='o', linestyle='-', color='b', label='Data')

  # Add title and labels
    plt.title('Plot of output.dat')
    plt.xlabel('Ecut Values')
    plt.ylabel('Second Column Values')
    plt.legend()

  # Show grid
    plt.grid(True)

  # Save the plot as a PDF
    plt.savefig('output_plot.pdf')

    print("Plot saved as output_plot.pdf")

    return
