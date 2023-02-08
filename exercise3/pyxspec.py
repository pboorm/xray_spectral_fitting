"""
Exercise 3, PyXspec
"""
import subprocess

ftgrouppha_str = "ftgrouppha"
ftgrouppha_str += " infile=fpma_60ks.pha"
ftgrouppha_str += " backfile=fpma_60ks_bkg.pha"
ftgrouppha_str += " outfile=fpma_60ks_bmin1.pha"
ftgrouppha_str += " grouptype=bmin"
ftgrouppha_str += " groupscale=1"
ftgrouppha_str += " clobber=yes"

print(ftgrouppha_str.replace(" ", "\n"))

## remember to initialise HEASOFT before running ftgrouppha
subprocess.call(ftgrouppha_str, shell=True)
