"""
Exercise 4, PyXspec
"""

from xspec import *

Plot.xAxis = "keV"
Plot.device = "/xw"
## since we use TBabs, we must set the abundances accordingly
Xset.abund = "Wilm"
Fit.statMethod = "cstat"
Fit.query = "yes"

## load the recently re-binned data
AllData("1:1 fpma_60ks_bmin1.pha")
AllData.ignore("1: 0.-3. 78.-**")

## create model1
model1 = Model("TBabs*zpowerlw")
## set the fixed Galactic column through the Milky Way
## note forcing delta to be -1., means the parameter will be frozen
model1.TBabs.nH.values = (0.04, -1.)

## then set the parameters of the redshifted powerlaw
model1.zpowerlw.PhoIndex.values = (1.8, 0.1, -3., -2., 9., 10.)
model1.zpowerlw.Redshift.values = (0.05, -1.)
model1.zpowerlw.norm.values = (1.e-5, 0.01, 1.e-10, 1.e-10, 1.e-1, 1.e-1)

## Plot the data before fitting to make sure the model is reasonable
## for more complex models, the final fit can depend drastically on the initial parameters
Plot("ldata")

## perform a Levenberg-Marquardt fit to the data
Fit.perform()

## show the information from the model that was fit
AllModels.show()
