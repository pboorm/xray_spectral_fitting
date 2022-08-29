"""
Exercise 2, Sherpa
"""

load_pha(1, "fpma_60ks.pha")
ignore_id(1, "0.:3.,78.:")
set_analysis(1, "chan", "counts")
plot_data(xlog=True, ylog=True)

plot_bkg(xlog=True, ylog=True)
