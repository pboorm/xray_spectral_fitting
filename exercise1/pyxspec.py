"""
Exercise 1, PyXspec
"""
from xspec import *

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
