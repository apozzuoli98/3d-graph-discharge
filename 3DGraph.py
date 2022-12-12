from cmath import nan
import matplotlib as mplt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm

"""
3d Surface plot to show daily discharge per year for river dataset

Accepts a csv file with column titles: 'Year', 'Month', 'Day', and 'Discharge' in any order with any other data columns

Author: Andrew Pozzuoli
Date: December 2022
"""
class DischargeMap: 

    """
    pk  peak threshold for colour values (every thing over peak threshold is coloured red)
    f   name of csv file
    """
    def __init__(self, pk, f):
        self.PEAK_THRESHOLD = pk
        self.filename = f
        self.data = self.readFile(f)
        self.plot3d()
        

    """
    Read data from csv file and create an array from it

    """
    def readFile(self, f):
        data = pd.read_csv(f)
        data = data.pivot(index=['Month', 'Day'], columns='Year', values='Discharge')
        all_years = np.arange(data.columns[0], data.columns[-1])
        data = data.reindex(columns=all_years)
        self.PEAK_THRESHOLD = self.PEAK_THRESHOLD / max(list(data.max()))
        return data


    """
    Plot data in 3D surface plot

    """
    def plot3d(self):
        plt.figure(figsize=(12,8))
        ax = plt.axes(projection='3d')
        _date = np.arange(len(self.data))
        _year = np.arange(len(self.data.columns))
        ax.set_yticks(_year[::10])
        ax.set_yticklabels(list(self.data.columns)[::10])
        # ax.set_yticks(_date[::31])
        # ax.set_yticklabels(np.arange(12)+1)
        ax.set_xlabel('Day', labelpad=10)
        ax.set_ylabel('Year', labelpad=10)
        ax.set_zlabel('Discharge (m\u00b3/s)')
        year, date = np.meshgrid(_year, _date)
        arr = self.data.to_numpy()
        cmap = (mplt.colors.ListedColormap(["yellow", "greenyellow", "lawngreen", "limegreen", "mediumseagreen",  "deepskyblue", "royalblue", "magenta"]))
        bounds = [0, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]
        norm = mplt.colors.BoundaryNorm(bounds, cmap.N, clip = True)
        ax.plot_surface(date, year, arr, cmap=cmap, linewidth=0.1, edgecolor='black', cstride=1, rstride=1, norm=norm, vmax=20)

        plt.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm), shrink=0.5, pad=0.1)
        plt.show()



def main():
    if (len(sys.argv) > 1):
        file = str(sys.argv[1])
        DischargeMap(20, file)
    else:
        DischargeMap(20, "LittleRougeCreek.csv")


if __name__ == "__main__":
    main()
