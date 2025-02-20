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
            CAnnOMBase, CAnnIniBase,CAnnIniRetrofit, CAnnOMRetrofit, Additional_Trees, CO2UptakeTree10Years,
           DiffFuelConsump, DiffElecConsump, ElecEmissionIntensity,Region, Payback, outputFileNamePayback,
            outputFileName, Nyears, CRFFullPeriod,FuelCO2Saving,ElecCO2Saving,\
                 CO2Saving,outputFileNameCO2Saving,TotalCO2Sav,PresSCCSav):


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


        # CO2 savings over the investment period [kg]

        # CO2 savings with the addition of vegetation [kg]
        # EPA 2021 - Greenhouse Gases Equivalencies Calculator - Calculations and References
        VegCO2Saving = Additional_Trees * (CO2UptakeTree10Years / 10) * Nyears

        # CO2 savings with the reduction of Fuel [kg]
        # Saved Fuel [m^3 for Gas and L for Diesel]

        FuelSaving = (DiffFuelConsump) * A_building * Nyears

        # Total CO2 savings [kg]
        #TotalCO2Sav = VegCO2Saving + FuelCO2Saving + ElecCO2Saving

        print('Marginal Annualized Cost Base [Dollars]:', round(CAnnBase))
        print('Marginal Annualized Cost Retrofit [Dollars]: ', round(CAnnRetrofit))
        print('Savings in Marginal Annualized Cost [Dollars]', round(TotalAnnCostSaving))
        print('Percent Difference in Marginal Annualized Cost [Percent]: ', round(PercAnnSaving))
        print('CO2e Savings from Extra Vegetation [kg]: ', round(VegCO2Saving))
        print('CO2e Savings from Fuel Savings [kg]: ', round(FuelCO2Saving))
        print('CO2e Savings from Electricity Savings [kg]: ', round(ElecCO2Saving))
        print('CO2e Savings total [kg]: ', round(TotalCO2Sav))
        print('Social Cost of Carbon [kg]: ', round(CAnnSCCSav))

    # Writing Payback Data
        with open(outputFileNamePayback, "w") as outputFile:
            outputFile.write("# 0: Year, 1: Cost Difference [Dollars]\n")
            for year, payback in zip(range(1, len(Payback) + 1), Payback):
                outputFile.write("%d \t %.0f\n" % (year, payback))

            # Writing CO2Saving Data
        with open(outputFileNameCO2Saving, "w") as outputFile:
            outputFile.write("# 0: Year, 1: CO2Saving [kg]\n")
            for year, CO2Saving in zip(range(1, len(CO2Saving) + 1), CO2Saving):
                outputFile.write("%d \t %.0f\n" % (year, CO2Saving))

            # Writing Summary Data
        with open(outputFileName, "w") as outputFile:
            # Write header
            outputFile.write("#0: Marginal Annualized Cost Base [Dollars] \t 1: Marginal Annualized Cost Retrofit [Dollars] \t \
                               2: Savings in Marginal Annualized Cost [Dollars] \t 3: Percent Difference in Marginal Annualized Cost [Percent] \t \
                               4: CO2e Savings from Extra Vegetation [kg] \t 5: CO2e Savings from Fuel Savings [kg] \t \
                               6: CO2e Savings from Electricity Savings [kg] \t 7: CO2e Savings total [kg] \n")

            # Write data
            outputFile.write("%0.0f \t %0.0f \t %0.0f \t %0.0f \t %0.0f \t %0.0f \t %0.0f \t %0.0f \n"
                             % (CAnnBase, CAnnRetrofit, TotalAnnCostSaving, PercAnnSaving, VegCO2Saving, FuelCO2Saving,
                                ElecCO2Saving, TotalCO2Sav))

