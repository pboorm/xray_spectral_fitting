"""
Exercise 4, Sherpa
"""

## load the recently re-binned data
load_pha(1, "fpma_60ks_bmin1.pha")
ignore_id(1, "0.:3.,78.:")

## set the x-axis to energy units and the y-axis to count rate
set_analysis(1, "ener", "rate")

## make sure we are using W-statistics (aka modified C-statistics)
set_stat("wstat")

## we use TBabs, so set the abundances accordingly
set_xsabund("wilm")

## define model1
model1 = xstbabs.nhgal*xszpowerlw.mypow

## set the column density along the line-of-sight purely from the Milky Way
set_par(nhgal.nh, val=0.04, frozen=True)

## set the parameters in the redshifted powerlaw
set_par(mypow.phoindex, val=1.8, min=-3., max=10., frozen=False)
set_par(mypow.redshift, val=0.05, frozen=True)
set_par(mypow.norm, val=1.e-5, min=1.e-10, max=1.e-1, frozen=False)

## set model1 to the dataset that was loaded
set_source(1, model1)

## plot the data before running fit to check everything looks ok
plot_fit(xlog=True, ylog=True)

## perform a Levenberg-Marquardt fit
fit()

