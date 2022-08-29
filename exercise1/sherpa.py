"""
Exercise 1, Sherpa

Assuming you started an interactive Sherpa iPython session by typing "sherpa"
"""

load_pha(1, "fpma_60ks.pha")
ignore_id(1, "0.:3.,78.:")
set_analysis(1, "chan", "counts")
plot_data(xlog=True, ylog=True)

