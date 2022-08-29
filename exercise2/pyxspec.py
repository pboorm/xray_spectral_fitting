"""
Exercise 2, PyXspec
"""
from xspec import *
import numpy as np
import matplotlib.pyplot as plt

## set the x-axis to channels
Plot.xAxis = "chan"
Plot.device = "/xw"

## load the data
AllData("1:1 fpma_60ks.pha")
## ignore relevant channels in a certain energy range
## note: Xspec will treat the ranges as channels if integers are provided!
AllData.ignore("1: 0.-3. 78.-**")

## Remove the background to be able to plot total "on" region counts
AllData(1).background = None

## Xspec defaults to plotting lcounts with a linear x-axis, so we undo that here
Plot.addCommand("log x on")
Plot("lcounts")

## In exercise 1, we removed the background so add that back here
AllData(1).background = "fpma_60ks_bkg.pha"

## including the background contribution in each bin of the plot
Plot.background = True

Plot("lcounts")

## save the data plotted to create a plot in matplotlib
y = np.array(Plot.backgroundVals())
x = Plot.x()
xErr = Plot.xErr()
yErr = np.sqrt(y)
fig, ax = plt.subplots()
ax.errorbar(x, y, xerr=xErr, yerr=yErr, fmt="o", markersize=3.)
ax.set_ylabel("Counts/channel")
ax.set_xlabel("Channel")
ax.set_xscale("log")
ax.set_yscale("log")
plt.show()
