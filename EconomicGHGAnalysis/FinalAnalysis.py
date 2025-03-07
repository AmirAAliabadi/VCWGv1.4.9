# Calculate Annualized Marginal Cost and GHG Emissions
# Ali Madadizadeh, Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 2024-02-28

import random
import sys
import os
import numpy
import matplotlib.pyplot as plt
import os

import numpy as np
import pandas as pd

# Inputs
class FinalAnalysis():
    def __init__(self, PresLoanPayment, PresBaseFuelCost, PresRetrofitFuelCost, PresBaseElecCost,
             PresRetrofitElecCost, SalFactorBase, CIniBase, A_building, PWFFullPeriod, SalFactor, CIniRetrofit,
            CAnnOMBase, CAnnIniBase,CAnnIniRetrofit, CAnnOMRetrofit, Payback, outputFileNamePayback,
            outputFileName, Nyears, CRFFullPeriod, TotalCO2Sav,PresSCCSav):


        CAnnLoanPayment = PresLoanPayment * CRFFullPeriod

        CAnnSCCSav = PresSCCSav * CRFFullPeriod

        CAnnFuelBase = PresBaseFuelCost * CRFFullPeriod
        CAnnFuelRetrofit = PresRetrofitFuelCost * CRFFullPeriod

        CAnnElecBase = PresBaseElecCost * CRFFullPeriod
        CAnnElecRetrofit = PresRetrofitElecCost * CRFFullPeriod

        CSalBase = SalFactorBase * CIniBase * A_building * PWFFullPeriod
        CSalRetrofit = SalFactor * CIniRetrofit * PWFFullPeriod

        CAnnSalBase = CSalBase * CRFFullPeriod
        CAnnSalRetrofit = CSalRetrofit * CRFFullPeriod

        CAnnBase = CAnnIniBase + CAnnFuelBase + CAnnElecBase + CAnnOMBase * A_building - CAnnSalBase
        CAnnRetrofit = CAnnIniRetrofit + CAnnFuelRetrofit + CAnnElecRetrofit + CAnnOMRetrofit + CAnnLoanPayment -\
                       CAnnSalRetrofit - CAnnSCCSav

        #Cost saving
        TotalAnnCostSaving = CAnnBase - CAnnRetrofit
        PercAnnSaving = 100 * (CAnnBase - CAnnRetrofit) / CAnnBase

        print('Marginal Annualized Cost Base [Dollars]:', round(CAnnBase))
        print('Marginal Annualized Cost Retrofit [Dollars]: ', round(CAnnRetrofit))
        print('Savings in Marginal Annualized Cost [Dollars]', round(TotalAnnCostSaving))
        print('Percent Difference in Marginal Annualized Cost [Percent]: ', round(PercAnnSaving))
        print('CO2e Savings Total in Multiple Years [kg]: ', round(TotalCO2Sav))
        print('Annual Social Cost of Carbon [kg]: ', round(CAnnSCCSav))

    # Writing Payback Data
        with open(outputFileNamePayback, "w") as outputFile:
            outputFile.write("# 0: Year, 1: Cost Difference [Dollars]\n")
            for year, payback in zip(range(1, len(Payback) + 1), Payback):
                outputFile.write("%d \t %.0f\n" % (year, payback))

            # Writing Summary Data
        with open(outputFileName, "w") as outputFile:
            # Write header
            outputFile.write("#0: Marginal Annualized Cost Base [Dollars] \t 1: Marginal Annualized Cost Retrofit [Dollars] \t \
                               2: Savings in Marginal Annualized Cost [Dollars] \t 3: Percent Difference in Marginal Annualized Cost [Percent] \t \
                               4: CO2e Savings total [kg] \n")

            # Write data
            outputFile.write("%0.0f \t %0.0f \t %0.0f \t %0.0f \t %0.0f \n"
                             % (CAnnBase, CAnnRetrofit, TotalAnnCostSaving, PercAnnSaving, TotalCO2Sav))

