from cmath import inf, nan
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
        data = data.dropna()
        data['Year'] = data['Year'].astype(int)
        data = data.pivot(index=['Month', 'Day'], columns='Year', values='Discharge')
        all_years = np.arange(1950, data.columns[-1]+1)
        data = data.reindex(columns=all_years, method=None)
        self.PEAK_THRESHOLD = self.PEAK_THRESHOLD / max(list(data.max()))
        return data


    """
    Plot data in 3D surface plot

    """
    def plot3d(self):
        # Set up figure
        plt.figure(figsize=(12,8))
        ax = plt.axes(projection='3d')
        _date = np.arange(len(self.data))
        _year = np.arange(len(self.data.columns))
        ax.set_yticks(_year[::10])
        ax.set_yticklabels(list(self.data.columns)[::10], va='baseline', ha='left')
        ax.set_zlim(0,60) # 60 is the upper limit of discharge
        ax.set_ylim(0,70) # 70 years in this data set
        ax.set_xlim(0,366) # 366 days per year (leap year) (note: Feb. 29 will be a blank spot in non-leap year of the graph)
        ax.zaxis.get_major_ticks()[0].label1.set_visible(False)

        #plot labels
        ax.set_xlabel('Day', labelpad=10)
        ax.set_ylabel('Year', labelpad=20)
        ax.set_zlabel('Discharge (m\u00b3/s)')
        year, date = np.meshgrid(_year, _date)
        arr = self.data.to_numpy()

        # Custom, discrete colour bar showing magenta for extreme values
        cmap = (mplt.colors.ListedColormap(['yellow', 'greenyellow', 'lawngreen', 'limegreen', 
                                            'mediumseagreen',  'deepskyblue', 'royalblue', 'darkblue']).with_extremes(over='magenta'))
        bounds = [0, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]
        norm = mplt.colors.BoundaryNorm(bounds, ncolors=cmap.N+2, clip=False)
        ax.plot_surface(date, year, arr, cmap=cmap, linewidth=0.1, edgecolor='black', cstride=1, rstride=1, norm=norm)
        ax.view_init(38, -43) # initial view angle
        plt.colorbar(cm.ScalarMappable(cmap=cmap, norm=mplt.colors.BoundaryNorm([0, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20], ncolors=cmap.N, clip=False)), shrink=0.5, pad=0.1, extend='max', label='Discharge (m\u00b3/s)')
        plt.show()


def main():
    if (len(sys.argv) > 1):
        file = str(sys.argv[1])
        DischargeMap(20, file)
    else:
        DischargeMap(20, "LittleRougeCreek.csv")


if __name__ == "__main__":
    main()
