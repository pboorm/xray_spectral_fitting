"""
Script for performing the Null Hypothesis Significance Testing exercises
"""
import subprocess
from xspec import *
import pandas as pd
from tqdm import tqdm

def model1():
	"""
	Function to setup model1
	"""
	model = Model("TBabs(zpowerlw)")
	AllModels(1)(1).values = (0.04, -1)
	AllModels(1)(2).values = (1.8, 0.1, -3., -2., 9., 10.)
	AllModels(1)(3).values = (0.05, -1)
	AllModels(1)(4).values = (1.e-05, 0.01, 1.e-10, 1.e-10, 1.e-1, 1.e-1)

def model2():
	"""
	Function to setup model2
	"""
	model = Model("TBabs(zphabs*cabs*zpowerlw)")
	AllModels(1)(1).values = (0.04, -1)
	AllModels(1)(2).values = (10., 0.1, 0.01, 0.01, 1000., 1000.)
	AllModels(1)(3).values = (0.05, -1)
	AllModels(1)(4).link = "p3" ## cabs.nH
	AllModels(1)(5).values = (1.8, 0.1, -3., -2., 9., 10.)
	AllModels(1)(6).values = (0.05, -1)
	AllModels(1)(7).values = (1.e-05, 0.01, 1.e-10, 1.e-10, 1.e-1, 1.e-1)

Fit.statMethod = "cstat"
Plot.device = "/null"
Xset.abund = "wilm"
Fit.query = "yes"
N_reals = 1000

for type_error in ["I", "II"]:
	nhst_dict = {}
	with tqdm(total = N_reals, position = 0, desc = "Type %s error" %(type_error)) as pbar:
		for i, rn in enumerate(range(N_reals)):
			s = AllData("1:1 fpma_60ks_bmin1.pha")
			AllData.ignore("1:0.-3. 78.-**")
			if type_error == "I":
				model1()
			else:
				model2()
			Fit.perform()

			fakeit_kwargs = {}
			fakeit_kwargs["response"] = AllData(1).response.rmf
			fakeit_kwargs["arf"] = AllData(1).response.arf
			fakeit_kwargs["exposure"] = AllData(1).exposure
			fakeit_kwargs["correction"] = "1."
			fakeit_kwargs["backExposure"] = fakeit_kwargs["exposure"]
			fakeit_kwargs["fileName"] = "NHST.pha"
			fakeit_kwargs["background"] = AllData(1).background.fileName
			fakeit_settings = FakeitSettings(**fakeit_kwargs)
			AllData.fakeit(1, fakeit_settings, applyStats=True)

			## make sure to bin suitably for WStat
			bin_fname = "NHST_bmin1.pha"
			ftgrouppha_str = "ftgrouppha"
			ftgrouppha_str += " infile=%s" %(AllData(1).fileName)
			ftgrouppha_str += " backfile=%s" %(AllData(1).background.fileName)
			ftgrouppha_str += " outfile=%s" %(bin_fname)
			ftgrouppha_str += " grouptype=bmin"
			ftgrouppha_str += " groupscale=1"
			ftgrouppha_str += " clobber=yes"
			subprocess.call(ftgrouppha_str, shell = True)

			AllData("1:1 %s" %(bin_fname))
			AllData.ignore("1:0.-3. 78.-**")

			model1()
			Fit.perform()
			if i == 0:
				nhst_dict["Wstat1"] = []
				nhst_dict["dof1"] = []
				nhst_dict["Wstat2"] = []
				nhst_dict["dof2"] = []
			nhst_dict["Wstat1"].append(Fit.statistic)
			nhst_dict["dof1"].append(Fit.dof)

			model2()
			Fit.perform()
			nhst_dict["Wstat2"].append(Fit.statistic)
			nhst_dict["dof2"].append(Fit.dof)
			pbar.update(1)
					
		df = pd.DataFrame(data = nhst_dict)
		df.to_csv("./nhst_type%s.csv" %(type_error), index = False)
	
		
