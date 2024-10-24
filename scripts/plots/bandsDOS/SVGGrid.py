import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Paths to your SVG images
s = '../plots/Grids/'

png_files = [[s+ 'CsPbBr2I.png', s+ 'CsPbBr3.png'],
              [s+ 'CsPbBrI2.png', s+ 'CsPbI3.png']]


fig, axes = plt.subplots(2, 2)

for row in [0, 1]:
    for column in [0, 1]:
        ax = axes[row, column]
        ax.axis('off')
        image = plt.imread(png_files[row][column])
        ax.imshow(image)

plt.tight_layout()
plt.savefig('grid.png', bbox_inches='tight', dpi = 400)  # Save as PNG
plt.show()


