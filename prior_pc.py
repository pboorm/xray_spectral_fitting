"""
This function saves simulated prior model counts to plot
as a shaded region on a QQdiff plot
"""

from xspec import *
import bxa.xspec as bxa
from bxa.xspec.solver import set_parameters
import numpy as np
import pandas as pd

s = AllData("1:1 fpma_60ks_bmin1.pha")
AllData.ignore("1:0.-3. 78.-**")

model1 = Model("TBabs*zpowerlw")
model1.TBabs.nH.values = (0.04, -1.)
model1.zpowerlw.PhoIndex.values = (1.8, 0.1, -3., -2., 9., 10.)
model1.zpowerlw.Redshift.values = (0.05, -1.)
model1.zpowerlw.norm.values = (1.e-5, 0.01, 1.e-10, 1.e-10, 1.e-1, 1.e-1)

prior1 = bxa.create_uniform_prior_for(model1, model1.zpowerlw.PhoIndex)
prior2 = bxa.create_loguniform_prior_for(model1, model1.zpowerlw.norm)

solver = bxa.BXASolver(transformations=[prior1, prior2], outputfiles_basename="powerlaw_pyxspec")

Nreals = 1000
Plot.xAxis = "keV"
Plot.background = True
Plot.addCommand("log x on")
Plot.setRebin(5., 1000)
Plot("lcounts")
## REMEMBER Plot.y() is background-subtracted in PyXspec
df = pd.DataFrame(data = {"x": Plot.x(), "x_err": Plot.xErr(), "b": Plot.backgroundVals(), "s": Plot.y(), "s_err": Plot.yErr()})
df.loc[:, "b_err"] = np.sqrt(df["b"])
df.loc[:, "sb"] = df["s"] + df["b"]

df.loc[:, "sb_err"] = 0.
mask = (df["s"] >= 1.) & (df["b"] >= 1.)
df.loc[mask, "sb_err"] = np.sqrt((df.loc[mask, "s_err"] / df.loc[mask, "s"]) ** 2 + (df.loc[mask, "b_err"] / df.loc[mask, "b"]) ** 2)
df.loc[:, "Qsb"] = df["sb"].cumsum() / df["sb"].sum()
prior_realisations = {}
for i in range(Nreals):
    values = solver.prior_function(np.random.uniform(
                                   size=len(solver.paramnames)))
    set_parameters(transformations=solver.transformations, values=values)
    Plot("lcounts")
    prior_realisations["m_%d" %(i)] = Plot.model()
    prior_realisations["mb_%d" %(i)] = prior_realisations["m_%d" %(i)] + df["b"].values
    prior_realisations["Qmb_%d" %(i)] = np.cumsum(prior_realisations["mb_%d" %(i)]) / np.sum(prior_realisations["mb_%d" %(i)])
    # if np.sum(prior_realisations["mb_%d" %(i)]) < 10.:
    #     print(prior_realisations["m_%d" %(i)], prior_realisations["mb_%d" %(i)])
    #     pause = input()

for key, item in prior_realisations.items():
    df.loc[:, key] = item

df.to_csv("./prior_pc_model1.csv", index = False)

