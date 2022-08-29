"""
Exercise 3, Sherpa
"""

load_pha(1, "fpma_60ks.pha")
ignore_id(1, "0.:3.,78.:")
set_analysis(1, "ener", "counts")
b = get_bkg_plot(1)
d = get_data_plot(1)
grpN = 1
while bkg_binned == False:
    group_counts(1, grpN)
    b = get_bkg_plot(1)
    d = get_data_plot(1)
    if np.count_nonzero(b.y) == len(b.y):
        bkg_binned = True
    elif grpN == 20:
        group_counts(1, 1)
        bkg_binned = True
    else:
        grpN += 1
