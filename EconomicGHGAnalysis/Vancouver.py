# Calculate Annualized Marginal Cost and GHG Emissions
# Ali Madadizadeh, Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 04 December 2023

import random
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from EconomicGHGAnalysis.FinalAnalysis import FinalAnalysis

# Inputs
class Vancouver():
    def __init__(self, City, BaseCaseName, CaseName, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc):
        # 1:ON,Toronto (Zone = 5), 2:BC,Vancouver (Zone = 4), 3:AB_Calgary, 4:NL_StJohns, 5:MB Winnipeg (Zone = 7A), 6:SK_Saskatoon, 7:PE, 8:NS,Halifax (Zone = 6), 9:NB, 10:QC_Montreal, 11:YT_Withhorse, 12:NT Yellowknife (Zone = 8), 13:NU
        Region = 2

        #Input
        #Monthly
        PerfMetricsMonthlyFileNameBase = r'Output/{}-2020/{}-2020-{}/Perf-Metrics-{}-2020-{}-{}.txt'\
                                         .format(City,City,BaseCaseName,City,BaseCaseName,{})
        PerfMetricsMonthlyFileNameRetrofit = r'Output/{}-2020/{}-2020-{}/Perf-Metrics-{}-2020-{}-{}.txt'\
                                            .format(City,City,CaseName,City,CaseName,{})

        # Electricity price rates
        BC_Residential_Electricity_Rates = pd.read_csv('resources/Economics/BC_Residential_Electricity_Rates.txt', delimiter=',')

        # Gas price rates
        BC_NG_Residential_Rates = pd.read_csv('resources/Economics/BC_NG_Residential_Rates.txt',  delimiter=',')

        # CO2 savings with the reduction of electricity consumption from the grid
        # ElecEmissionIntensity [gCO2e kW-h^-1]
        ElecEmissionIntensity = pd.read_csv('resources/Economics/ElecEmissionIntensity.txt', delimiter=',')
        CarbonIntensityProjection = pd.read_csv('resources/Economics/carbon_intensity_projection.txt', delimiter=',')
        outputFileNameCO2Saving = 'Output/EconomicGHGAnalysisResults/{}_{}_{}CO2Saving.txt'.format(City, CaseName, Scenario)

        #Social Carbon Cost [$ Tonne CO2^-1]
        SCC = pd.read_csv('resources/Economics/SocialCarbonCost.txt', delimiter=',')

        MWCH4 = 12 + 4  # molecular weight of CH4 [gCH4 mol^-1]
        MWCO2 = 44  # molecular weight of CO2 [gCO2 mol^-1]
        rhoCH4 = 0.668  # density of methane [kgCH4 m^-3] at 293 K and 1 ATM

        # Output
        outputFileName = 'Output/EconomicGHGAnalysisResults/{}_{}_{}.txt'.format(City, CaseName, Scenario)
        outputFileNamePayback = 'Output/EconomicGHGAnalysisResults/{}_{}_{}Payback.txt'.format(City, CaseName, Scenario)
        outputFileNameCO2Saving = 'Output/EconomicGHGAnalysisResults/{}_{}_{}CO2Saving.txt'.format(City, CaseName, Scenario)

        #A gigajoule of natural gas is about 25.5 cubic metres at standard conditions.
        GJtoM3 = 25.5


        # Electricity consumption brackets or steps [kW-hr]
        BC_Step = 22.1918 * 30              # [kW-hr] = kW-hr day-1 * 30

        # Building envelope information
        A_building = 130  # Building footprint area [m^2]
        A_walls = 274  # Area of wall envelope [m^2]
        A_Roof = A_building / (np.cos(18.4 * np.pi / 180))  # Area of full roof [m^2]

        # Economic input
        # Annual inflation rate:  https://www.macrotrends.net/countries/CAN/canada/inflation-rate-cpi
        InfRate = 0.0183
        # Annual interest rate: https: // www150.statcan.gc.ca
        IntRate = 0.0378

        CIniBase = 5        # Marginal initial installation cost now per building foot print area [$ m^-2]
        CAnnOMBase = 1      # Marginal annual operation and maintenance cost now per building foot print area [$ m^-2] 0.9
        Nyears = 20         # Number of years for economic analysis
        # Marginal costs of base system without renewable energy
        # These costs are additional to the base cost of a system without renewable energy


        #ElecPriceInc = 0.05         # Annual rate of electricity price increase, can be mean/median over many decades
        #GasPriceInc = 0.05         # Annual rate of gas price increase, can be mean/median over many decades

        # Initial investment Prices
        PVPrice = 377                # PV price per collector area now (i.e portion of roof area) [$ m^-2]
        WTPrice = 490 * 2            # WT price per swept area now [$ m^-2] assuming 1 additional replacement
        STPrice = 340                # ST price per collector area [$ m^-2]
        BITESPrice = 200             # BITES price per unit volume [$ m^-3]
        PCMPrice = 1930 * 2          # PCM price per unit volume [$ m^-3] assuming 1 additional replacement
        HPPrice = 25 * 2              # HP price per building footprint area [$ m^-2] assuming 1 additional replacement
        TreePrice = 200              # Tree price per tree now
        CRPrice = 8 * 2              # Cool Roof price per roof area now [$ m^-2] assuming 1 additional coate
        AirTPrice = 1500 * 2            # Air tightness price per building [$ test^-1] (Assume 2 tests)
        RvalueWallPrice = 8          # Price of insulation of unit R value change for wall [$ m^-4 K^-1 W]
        RvalueRoofPrice = 8          # Price of insulation of unit R value change for roof [$ m^-4 K^-1 W]

        SalFactorBase = 0.03         # Fraction of initial investment of equipment that can be salvaged
        SalFactor = 0.05             # Fraction of initial investment of equipment that can be salvaged


        # CO2 uptake
        # 1: 10.52 [kg coniferous tree^-1 year^-10]
        # 2: 17.24 [kg deciduous tree^-10]
        # 3: 13.88 [kg Tree^-1] on average

        CO2UptakeTree10Years = 13.88  # [kgCO2 10-years-1]

        # Operation maintenance cost
        OMPV = 0.01 * PVPrice                # Operation maintenance cost for PV per collector area now [$ m^-2]
        OMWT = 0.02 * WTPrice                # Operation maintenance cost for WT per swept area now [$ m^-2]
        OMST = 0.01 * STPrice                # Operation maintenance cost for ST per collector area [$ m^-2]
        OMBITES = 0.01 * BITESPrice          # Operation maintenance cost for BITES per unit volume [$ m^-3]
        OMPCM = 0.01 * PCMPrice              # Operation maintenance cost for PCM per unit volume [$ m^-3]
        OMHP = 0.05 * HPPrice                # Operation maintenance cost for HP per building footprint area [$ m^-2]
        OMVeg = 130                          # Operation maintenance cost for tree care per 0.5 LAI [m^2 m^-2] added (~ 1 tree)
        OMCR = 0                             # Operation maintenance cost for keeping Cool Roof clean now [$]

        # Federal
        # Canada greener homes initiates
        # Canada Greener Homes Grant
        FedRebInsulation = 5000             # [$]
        FedRebAirSealing = 1000             # [$]
        FedRebWindowsDoors = 5000           # [$]
        FedRebSpaceWaterHeating = 5000      # [$]

        # Solar_photovoltaic_system_installation = 5000  #[$]
        FedRebPV = 5000                     #[$]

        # Canada Greener Homes Loan
        # From $5,000 to $40,000: Interest-free loans with a repayment term of 10 years to help you undertake major home retrofits
        FedLoanCanGreener = 10000       # [$]
        FedLoanNyearsForgiveness = 10   # [years]

        #Provincial
        #Heat Pump Rebates
        #Central_Ducted_HeatPump = 6000 #$1,200 - $6,000
        #Ductless_HeatPump = 6000 #$1,000 - $6,000 Ductless Mini-Split or Multi-Split Heat Pump
        #Dual_Fuel_Ducted_HeatPump = 3000 #[$]
        #Air_to_Water_HeatPump = 3000 #[$]
        #Combined_Space_HotWater_Air_to_Water_HeatPump = 4000 #[$] 1,000 - $4,000
        ProvRebHP = 3000        #[$]

        #Heat Pump Water Heaters
        # Electric_Heat_Pump_Water_Heater_Rebate = 1000
        # FortisBC_NaturalGas_Water_Heater_Rebates = 2500 #Up to $2,500

        # Windows, Doors, and Draftproofing
        ProvRebWindowsDoors = 2000      #[$] Up to $2,000

        #Ventilation_Rebate
        ProvRebVentHeatRecovery = 1600  #CleanBC Income Qualified Program Rebates & Up to $1,600

        #Insulation_Rebate
        ProvRebInsulation = 5500 #CleanBC Income Qualified Program Rebates & Up to $5,500

        if (Nyears < FedLoanNyearsForgiveness):
            print('Loan period cannot be longer than the number of analysis years!')
            sys.exit()

        # Number of additional trees, each extra tree adds 0.5 LAI [m^2 m^-2]
        Additional_Trees = 0

        # Retrofit case parameters information
        A_pv = 0.5
        A_wt = 0
        V_bites = 0.1
        A_st = 0
        V_pcm = 0
        A_CR = 0
        RvalWallBaseCase = 3.18
        RvalRoofBaseCase = 4.41
        RvalWallCase = 2 * RvalWallBaseCase
        RvalRoofCase = 2 * RvalRoofBaseCase

        RvalueWall_quantity = abs(RvalWallCase-RvalWallBaseCase)     # [m2 K W-1]
        RvalueRoof_quantity = abs(RvalRoofCase-RvalRoofBaseCase)     # [m2 K W-1]

        # High performance envelop price [$]
        EnvPrice = A_walls * RvalueWall_quantity * RvalueWallPrice + A_Roof * RvalueRoof_quantity * RvalueRoofPrice

        # Compute annualized system cost
        EffIntRate = (IntRate - InfRate) / (1 + InfRate)
        PWFFullPeriod = 1 / ((1 + EffIntRate) ** Nyears)
        CRFFullPeriod = EffIntRate / (1 - (1 + EffIntRate) ** (-Nyears))

        CAnnOMRetrofit = (PVSwitch * A_pv * OMPV + WTSwitch * A_wt * OMWT + STSwitch * A_st * OMST + BITESSwitch * V_bites * OMBITES + \
                          PCMSwitch * V_pcm * OMPCM + HPSwitch * OMHP + CRSwitch * OMCR) * A_building + Additional_Trees * OMVeg

        # Capital investment for the retrofitted system for the entire footprint of the house [$]
        CIniRetrofit = (PVSwitch * A_pv * PVPrice + WTSwitch * A_wt * WTPrice + STSwitch * A_st * STPrice +\
                        BITESSwitch * V_bites * BITESPrice + PCMSwitch *  V_pcm * PCMPrice + \
                         CRSwitch * A_CR * CRPrice + HPSwitch * HPPrice) * A_building + EnvSwitch * EnvPrice +\
                       AirTSwitch * AirTPrice + TreePrice * Additional_Trees - \
                        (FedLoanCanGreener + PVSwitch * FedRebPV + AirTSwitch * FedRebAirSealing + \
                         EnvSwitch * FedRebInsulation + EnvSwitch * ProvRebInsulation + HPSwitch * ProvRebHP +\
                         BITESSwitch * ProvRebVentHeatRecovery + WindowDoorReplaceSwitch * FedRebWindowsDoors +\
                         WindowDoorReplaceSwitch * ProvRebWindowsDoors)

        CAnnIniBase = CIniBase * A_building * CRFFullPeriod
        CAnnIniRetrofit = CIniRetrofit * CRFFullPeriod


        # Calculate present worth of cost of gas and electricity for base and retrofitted systems for the entire footprint of the house [$]
        PresBaseGasCost, PresRetrofitGasCost, PresBaseElecCost, PresRetrofitElecCost, TotalGasConsumpHeatBase, \
        TotalGasConsumpWaterHeatBase, TotalGasConsumpHeatRetrofit, TotalGasConsumpWaterHeatRetrofit, TotalElecCoolDemandBase, \
        TotalElecDomesticDemandBase, TotalElecCoolDemandRetrofit, TotalElecHeatDemandRetrofit, TotalElecDomesticDemandRetrofit, \
        TotalElecProducedPVRetrofit, TotalElecProducedWTRetrofit, PresBaseOMCost, PresRetrofitOMCost, SumAnnualCostDiff, \
        PresFedLoanPayment , FuelCO2Saving, ElecCO2Saving,TotalCO2Sav,PresSCCSav= [0] * 23

        Payback = []
        CO2Saving = []

        AnnVegCO2Saving = Additional_Trees * (CO2UptakeTree10Years / 10)

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
 
        # Calculate present worth base and system cumulative gas and electricity cost
        for year in range(1, Nyears + 1):
            for month_idx, month in enumerate(months, start=0):
                # Construct the file names based on the template
                FilePathRetrofitMonthly = PerfMetricsMonthlyFileNameRetrofit.format(month)
                FilePathBaseMonthly = PerfMetricsMonthlyFileNameBase.format(month)

                # Check if the file exists before attempting to load
                if os.path.exists(FilePathRetrofitMonthly) and os.path.exists(FilePathBaseMonthly):

                    # Load data from the file
                    # Monthly
                    PerfMetricsMonthlyBase = np.loadtxt(FilePathBaseMonthly)
                    PerfMetricsMonthlyRetrofit = np.loadtxt(FilePathRetrofitMonthly)

                    # Total Energy Consumption
                    TotalGasConsumpHeatBase = TotalGasConsumpHeatBase + PerfMetricsMonthlyBase[1]
                    TotalGasConsumpWaterHeatBase = TotalGasConsumpWaterHeatBase + PerfMetricsMonthlyBase[6]

                    TotalGasConsumpHeatRetrofit = TotalGasConsumpHeatRetrofit + PerfMetricsMonthlyRetrofit[1]
                    TotalGasConsumpWaterHeatRetrofit = TotalGasConsumpWaterHeatRetrofit + PerfMetricsMonthlyRetrofit[6]

                    TotalElecCoolDemandBase = TotalElecCoolDemandBase + PerfMetricsMonthlyBase[4]
                    TotalElecDomesticDemandBase = TotalElecDomesticDemandBase + PerfMetricsMonthlyBase[7]

                    TotalElecCoolDemandRetrofit = TotalElecCoolDemandRetrofit + PerfMetricsMonthlyRetrofit[4]
                    TotalElecHeatDemandRetrofit = TotalElecHeatDemandRetrofit + PerfMetricsMonthlyRetrofit[2]
                    TotalElecDomesticDemandRetrofit = TotalElecDomesticDemandRetrofit + PerfMetricsMonthlyRetrofit[7]
                    TotalElecProducedPVRetrofit = TotalElecProducedPVRetrofit + PerfMetricsMonthlyRetrofit[8]
                    TotalElecProducedWTRetrofit = TotalElecProducedWTRetrofit + PerfMetricsMonthlyRetrofit[9]

                    # Total Energy Consumtion
                    MonthlyDiffFuelConsump = PerfMetricsMonthlyBase[1] + PerfMetricsMonthlyBase[6] - \
                                             PerfMetricsMonthlyRetrofit[1] - PerfMetricsMonthlyRetrofit[6]
                    MonthlyDiffElecConsump = PerfMetricsMonthlyBase[4] + PerfMetricsMonthlyBase[7] - \
                                             (PerfMetricsMonthlyRetrofit[4] + PerfMetricsMonthlyRetrofit[2] +
                                              PerfMetricsMonthlyRetrofit[7] - \
                                              PerfMetricsMonthlyRetrofit[8] - PerfMetricsMonthlyRetrofit[9])

                    # Saved CO2 [kg]
                    FuelCO2Saving = (MonthlyDiffFuelConsump) *  A_building * rhoCH4 * MWCO2 / MWCH4
                    ElecCO2Saving = (MonthlyDiffElecConsump) * A_building * (CarbonIntensityProjection.iloc[year-1,1] /100) *\
                                    ElecEmissionIntensity.iloc[8, Region] / 1000

                    TotalCO2Sav = TotalCO2Sav + (FuelCO2Saving + ElecCO2Saving + AnnVegCO2Saving/12)

                    #Social Cost of Carbon
                    PresSCCSav = PresSCCSav + ((FuelCO2Saving + ElecCO2Saving + AnnVegCO2Saving/12) / 1000) * SCC.iloc[year-1,1] * \
                                  1 / ((1 + EffIntRate) ** year)
                    #print(FuelCO2Saving,ElecCO2Saving, PresSCCSav)
                    #Gas Consumption Cost
                    PresBaseGasCost = PresBaseGasCost + (BC_NG_Residential_Rates.iloc[0,0] + ((PerfMetricsMonthlyBase[1] + \
                        PerfMetricsMonthlyBase[6]) * (BC_NG_Residential_Rates.iloc[0,1] + BC_NG_Residential_Rates.iloc[0,2]+\
                         BC_NG_Residential_Rates.iloc[0,3])) * A_building) * (1 + GasPriceInc) ** \
                           year * 1 / ((1 + EffIntRate) ** year)

                    PresRetrofitGasCost = PresRetrofitGasCost + (BC_NG_Residential_Rates.iloc[0,0] + ((PerfMetricsMonthlyRetrofit[1] + \
                      PerfMetricsMonthlyRetrofit[6]) * (BC_NG_Residential_Rates.iloc[0, 1] + BC_NG_Residential_Rates.iloc[0, 2] + \
                          BC_NG_Residential_Rates.iloc[0, 3])) * A_building) * (1 + GasPriceInc) ** \
                            year * 1 / ((1 + EffIntRate) ** year)

                    #Electricity Consumption Cost
                    MonthlyElecDemandBase = PerfMetricsMonthlyBase[4] + PerfMetricsMonthlyBase[7]
                    MonthlyElecDemandRetrofit = PerfMetricsMonthlyRetrofit[4] + PerfMetricsMonthlyRetrofit[7] +\
                                                PerfMetricsMonthlyRetrofit[2] - PerfMetricsMonthlyRetrofit[8] - \
                                                PerfMetricsMonthlyRetrofit[9]


                    if MonthlyElecDemandBase <= BC_Step:

                        PresBaseElecCost = PresBaseElecCost + (BC_Residential_Electricity_Rates.iloc[0, 0] * 30 / 100 + \
                                    ((MonthlyElecDemandBase) * BC_Residential_Electricity_Rates.iloc[0,1] / 100) *\
                                    A_building) * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                    if MonthlyElecDemandBase >= BC_Step:
                        PresBaseElecCost = PresBaseElecCost + (BC_Residential_Electricity_Rates.iloc[0,0] * 30 / 100 + \
                            ((BC_Step / A_building) * BC_Residential_Electricity_Rates.iloc[0,1] / 100 +\
                            (MonthlyElecDemandBase - BC_Step / A_building) * BC_Residential_Electricity_Rates.iloc[:,2] / 100 ) *\
                                           A_building) * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                    if MonthlyElecDemandRetrofit <= BC_Step:

                        PresRetrofitElecCost = PresRetrofitElecCost + (BC_Residential_Electricity_Rates.iloc[0, 0] * 30 / 100 + \
                                ((MonthlyElecDemandRetrofit) * BC_Residential_Electricity_Rates.iloc[0,1] / 100) *\
                                    A_building) * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                    if MonthlyElecDemandRetrofit >= BC_Step:
                        PresRetrofitElecCost = PresRetrofitElecCost + (BC_Residential_Electricity_Rates.iloc[0,0] * 30 / 100 + \
                            ((BC_Step / A_building) * BC_Residential_Electricity_Rates.iloc[0,1] / 100 +\
                            (MonthlyElecDemandRetrofit - BC_Step / A_building) * BC_Residential_Electricity_Rates.iloc[:,2] / 100 ) *\
                                           A_building) * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                else:
                     print('There are no building energy performance metrics files!')

            # Calculate the payment of Canada_Greener_Homes_Loan as Interest-free loans over 10 years
            if year <= FedLoanNyearsForgiveness:
                PresFedLoanPayment = PresFedLoanPayment + ((FedLoanCanGreener / FedLoanNyearsForgiveness) * (1 / ((1 + EffIntRate) ** year)))

            # Calculate the payback period
            PresBaseOMCost = PresBaseOMCost + CAnnOMBase * A_building * 1 / ((1 + EffIntRate) ** year)
            PresRetrofitOMCost = PresRetrofitOMCost + CAnnOMRetrofit * 1 / ((1 + EffIntRate) ** year)

            SumAnnualCostDiff = PresFedLoanPayment + PresRetrofitGasCost + PresRetrofitElecCost + PresRetrofitOMCost - PresBaseGasCost - PresBaseElecCost - PresBaseOMCost - PresSCCSav

            PaybackDiff = SumAnnualCostDiff + CIniRetrofit - CIniBase * A_building
            print('Year, PaybackDiff = ', year, round(PaybackDiff))

            Payback.append(round(PaybackDiff))
            AnnualCO2Saving = FuelCO2Saving + ElecCO2Saving
            print('Year, AnnualCO2Saving = ', year, round(AnnualCO2Saving))

            CO2Saving.append (round(AnnualCO2Saving))
        #Total Loan Payment
        PresLoanPayment = PresFedLoanPayment

        #Total Energy Consumtion
        DiffFuelConsump = TotalGasConsumpHeatBase + TotalGasConsumpWaterHeatBase - \
                          TotalGasConsumpHeatRetrofit - TotalGasConsumpWaterHeatRetrofit
        DiffElecConsump = TotalElecCoolDemandBase + TotalElecDomesticDemandBase - \
                      (TotalElecCoolDemandRetrofit + TotalElecHeatDemandRetrofit + TotalElecDomesticDemandRetrofit - \
                       TotalElecProducedPVRetrofit - TotalElecProducedWTRetrofit)

        Final_Analysis = FinalAnalysis(PresLoanPayment, PresBaseGasCost, PresRetrofitGasCost, PresBaseElecCost,
          PresRetrofitElecCost, SalFactorBase, CIniBase, A_building, PWFFullPeriod,SalFactor, CIniRetrofit, CAnnOMBase,
             CAnnIniBase, CAnnIniRetrofit,CAnnOMRetrofit,Additional_Trees, CO2UptakeTree10Years, DiffFuelConsump,
                DiffElecConsump, ElecEmissionIntensity, Region, Payback, outputFileNamePayback, outputFileName, Nyears,
                                       CRFFullPeriod , FuelCO2Saving, ElecCO2Saving,CO2Saving,outputFileNameCO2Saving,
                                       TotalCO2Sav,PresSCCSav)

