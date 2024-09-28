## Convenience routines for reading and plotting bands:


## Example
## file_path = 'CsPbBr3.bands.gnu'
## df = reshapeBands(file_path, 36)
## plotly3Darray(df)
##
##



import numpy as np
import plotly.graph_objects as go
import plotly.subplots as subplots

import numpy as np

# Define the path to your data file
file_path = '/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/Abinitio-Codes/data/band_files/CsPbBr3.bands.gnu'

# Read the data while skipping blank lines



def reshapeBands(file_path, num_bands):
    """
    Reshape QE bands file so that you have a 3D array of shape (num_bands, num_kpoints, 2)
    
    num_kpoints = rows of data block in QE bands data file.
    """
    data = np.loadtxt(file_path)
    num_rows = data.shape[0]

    num_kpoints = num_rows // num_bands
    
    df = np.reshape(data, (num_bands, num_kpoints, 2))
    return df



def plotly3Darray(df):
    """
    Convenience plot for a 3D array such that the first column is 'index' and the 2nd two are the rows and columsn. 
    
    Args:
            df = [index, rows, columns]
        
    """
    # Create a figure
    fig = go.Figure()

    # Loop through each index in the first dimension
    for i in range(df.shape[0]):
        x_data = df[i, :, 0]  # First column (X values)
        y_data = df[i, :, 1]  # Second column (Y values)

        # Add a scatter trace for each index
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', name=f'Plot {i+1}'))

    # Update layout
    fig.update_layout(
        xaxis_title='X-axis',
        yaxis_title='Y-axis',
        yaxis=dict(range=[-10, 10]),  # Set y-axis limits
        height=800,  # Height in pixels
        width=400    # Width in pixels
    )

    fig.show()
    return 


file_path = '/home/fes33/Documents/GIK - R&D/Personal - Papers and Reports/--Libraries/abinit/Abinitio-Codes/data/band_files/CsPbBr3.bands.gnu'
df = reshapeBands(file_path, 36)
plotly3Darray(df)


