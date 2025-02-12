# Calculate Annualized Marginal Cost and GHG Emissions
# Ali Madadizadeh, Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 2024-02-28

import random
import sys
import os
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from EconomicGHGAnalysis.FinalAnalysis import FinalAnalysis


# Inputs
class Toronto():
    def __init__(self, City, BaseCaseName, CaseName, Senario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc):
        # 1:ON,Toronto (Zone = 5), 2:BC,Vancouver (Zone = 4), 3:AB_Calgary, 4:NL_StJohns, 5:MB Winnipeg (Zone = 7A), 6:SK_Saskatoon, 7:PE, 8:NS,Halifax (Zone = 6), 9:NB, 10:QC_Montreal, 11:YT_Withhorse, 12:NT Yellowknife (Zone = 8), 13:NU
        Region = 1

        #Input
        #Diurnal
        PerfMetricsDiurnalFileNameBase = r'Output/{}-2020/{}-2020-{}/Perf-Metrics-Diurnal{}-2020-{}-{}.txt'\
                                        .format(City,City,BaseCaseName,City,BaseCaseName,{})
        PerfMetricsDiurnalFileNameRetrofit = r'Output/{}-2020/{}-2020-{}-1/Perf-Metrics-Diurnal{}-2020-{}-1-{}.txt'\
                                            .format(City,City,CaseName,City,CaseName,{})

        # Electricity price rates
        ON_TOU_Electricity_Rates = pd.read_csv('resources/Economics/ON_TOU_Electricity_Rates.txt', delimiter=',')

        # Gas price rates
        ON_NG_Residential_Rates = pd.read_csv('resources/Economics/ON_NG_Residential_Rates.txt',  delimiter=',')

        # CO2 savings with the reduction of electricity consumption from the grid
        # ElecEmissionIntensity [gCO2e kW-h^-1]
        ElecEmissionIntensity = pd.read_csv('resources/Economics/ElecEmissionIntensity.txt', delimiter=',')
        CarbonIntensityProjection = pd.read_csv('resources/Economics/carbon_intensity_projection.txt', delimiter=',')
        outputFileNameCO2Saving = 'Output/EconomicGHGAnalysisResults/{}_{}_{}CO2Saving.txt'.format(City, CaseName, Senario)

        #Social Carbon Cost [$ Tonne CO2^-1]
        SCC = pd.read_csv('resources/Economics/SocialCarbonCost.txt', delimiter=',')
        
        MWCH4 = 12 + 4  # molecular weight of CH4 [gCH4 mol^-1]
        MWCO2 = 44  # molecular weight of CO2 [gCO2 mol^-1]
        rhoCH4 = 0.668  # density of methane [kgCH4 m^-3] at 293 K and 1 ATM

        #Output
        outputFileName = 'Output/EconomicGHGAnalysisResults/{}_{}_{}.txt'.format(City, CaseName, Senario)
        outputFileNamePayback = 'Output/EconomicGHGAnalysisResults/{}_{}_{}Payback.txt'.format(City, CaseName, Senario)
        outputFileNameCO2Saving = 'Output/EconomicGHGAnalysisResults/{}_{}_{}CO2Saving.txt'.format(City, CaseName, Senario)

        # Building envelope information
        A_building = 130  # Building footprint area [m^2]
        A_walls = 274  # Area of wall envelope [m^2]
        A_Roof = A_building / (np.cos(18.4 * np.pi/180))      # Area of full roof [m^2]

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

        #ElecPriceInc = 0.05       # Annual rate of electricity price increase, can be mean/median over many decades
        #GasPriceInc = 0.05        # Annual rate of gas price increase, can be mean/median over many decades

        # Initial investment Prices
        PVPrice = 377                # PV price per collector area now (i.e portion of roof area) [$ m^-2]
        WTPrice = 490 * 2            # WT price per swept area now [$ m^-2] assuming 1 additional replacement
        STPrice = 340                # ST price per collector area [$ m^-2]
        BITESPrice = 200             # BITES price per unit volume [$ m^-3]
        PCMPrice = 1930 * 2          # PCM price per unit volume [$ m^-3] assuming 1 additional replacement
        HPPrice = 25 * 2             # HP price per building footprint area [$ m^-2] assuming 1 additional replacement
        TreePrice = 200              # Tree price per tree now
        CRPrice = 8 * 2              # Cool Roof price per roof area now [$ m^-2] assuming 1 additional coat
        AirTPrice = 1500 * 2         # Air tightness price per building [$ test^-1] (Assume 2 tests)
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
        OMCR = 0.1 * CRPrice                 # Operation maintenance cost for keeping Cool Roof clean now [$]

        # Federal
        # Canada greener homes initiates
        # Canada Greener Homes Grant
        FedRebInsulation = 5000                          #[$]
        FedRebAirSealing = 1000                          #[$]
        FedRebWindowsDoors = 5000                        #[$]
        FedRebSpaceWaterHeating = 5000                   #[$]

        #Solar_photovoltaic_system_installation = 5000  #[$]
        FedRebPV = 5000
        
        # Canada Greener Homes Loan
        # From $5,000 to $40,000: Interest-free loans with a repayment term of 10 years to help you undertake major home retrofits
        FedLoanCanGreener = 10000                       #[$]
        FedLoanNyearsForgiveness = 10                   #[years]
        

        #Provincial
        #Eco-Roof Incentive Program
        #Cool Roof Incentives (up to $50,000)
        #cool_roof_with_new_membrane = 5                #[$/m2]
        #cool_roof_coating_existing_roof = 2            #[$/m2]
        ProvRebCR = 5                                   #[$/m2]

        #Home Energy Loan Program (HELP) up to 20 years, interest-free
        #Rooftop_Solar_PV = 1000 #[$]
        ProvHElPPV= 1000                                 #[$]

        #Mini_heatpump = 1250
        #Centrally_Ducted_heatPumps = 2000
        #cold_climat_HeatPumps= 2500
        ProvHElPHP = 2000                                #[$]

        ProvHelPNyearsForgiveness = 20                             # [years]


        if (Nyears < FedLoanNyearsForgiveness) or (Nyears < ProvHelPNyearsForgiveness):
            print('Loan period cannot be longer than the number of analysis years!')
            sys.exit()

        # Number of additional trees, each extra tree adds 0.5 LAI [m^2 m^-2]
        Additional_Trees = 0

        # Retrofit case parameters information
        A_pv = 0.5        # Per building footprint area [m2 m-2]
        A_wt = 0            # Per building footprint area [m2 m-2]
        V_bites = 0.1        # Per building footprint area [m3 m-2]
        A_st = 0          # Per building footprint area [m2 m-2]
        V_pcm = 0           # Per building footprint area [m3 m-2]
        A_CR = 1            # Per building footprint area [m2 m-2]
        RvalWallBaseCase = 3.6
        RvalRoofBaseCase = 5.46
        RvalWallCase = 2 * RvalWallBaseCase
        RvalRoofCase = 2 * RvalRoofBaseCase

        RvalueWall_quantity = abs(RvalWallCase-RvalWallBaseCase)     # [m2 K W-1]
        RvalueRoof_quantity = abs(RvalRoofCase-RvalRoofBaseCase)     # [m2 K W-1]

        # High performance envelop price [$]
        EnvPrice = EnvSwitch * A_walls * RvalueWall_quantity * RvalueWallPrice + EnvSwitch * A_Roof * RvalueRoof_quantity * RvalueRoofPrice

        # Compute annualized system cost
        EffIntRate = (IntRate - InfRate) / (1 + InfRate)
        PWFFullPeriod = 1 / ((1 + EffIntRate) ** Nyears)
        CRFFullPeriod = EffIntRate / (1 - (1 + EffIntRate) ** (-Nyears))


        CAnnOMRetrofit = (PVSwitch * A_pv * OMPV + WTSwitch * A_wt * OMWT + STSwitch * A_st * OMST + BITESSwitch * V_bites * OMBITES +\
                 PCMSwitch * V_pcm * OMPCM + HPSwitch * OMHP + CRSwitch * OMCR) * A_building + Additional_Trees * OMVeg

        # Capital investment for the retrofitted system for the entire footprint of the house [$]
        CIniRetrofit = ((PVSwitch * A_pv * PVPrice + WTSwitch * A_wt * WTPrice + STSwitch * A_st * STPrice + BITESSwitch * V_bites * BITESPrice +\
                         PCMSwitch *  V_pcm * PCMPrice + CRSwitch * A_CR * CRPrice + HPSwitch * HPPrice) * A_building + EnvSwitch * EnvPrice +\
                        AirTSwitch * AirTPrice + TreePrice * Additional_Trees -(FedLoanCanGreener + PVSwitch * FedRebPV + PVSwitch * ProvHElPPV +\
                        AirTSwitch * FedRebAirSealing + EnvSwitch * FedRebInsulation + CRSwitch * A_CR * ProvRebCR * A_building +\
                          HPSwitch * ProvHElPHP + WindowDoorReplaceSwitch * FedRebWindowsDoors))

        CAnnIniBase = CIniBase * A_building * CRFFullPeriod
        CAnnIniRetrofit = CIniRetrofit * CRFFullPeriod


        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Calculate present worth of cost of gas and electricity for base and retrofitted systems for the entire footprint of the house [$]

        Payback = []
        CO2Saving = []

        PresBaseGasCost, PresRetrofitGasCost, PresBaseElecCost, PresRetrofitElecCost, TotalGasConsumpHeatBase,\
        TotalGasConsumpWaterHeatBase, TotalGasConsumpHeatRetrofit, TotalGasConsumpWaterHeatRetrofit, TotalElecCoolDemandBase, \
        TotalElecDomesticDemandBase, TotalElecCoolDemandRetrofit, TotalElecHeatDemandRetrofit, TotalElecDomesticDemandRetrofit, \
        TotalElecProducedPVRetrofit, TotalElecProducedWTRetrofit, PresBaseOMCost, PresRetrofitOMCost, SumAnnualCostDiff, \
        PresFedLoanPayment, PresProvHELPHP, PresProvHELPPV , FuelCO2Saving, ElecCO2Saving,TotalCO2Sav,PresSCCSav = [0] * 25
 
 # Embodied carbon factors
        ECF_PV = 50  # kg CO2e m-2 (embodied carbon factor for photovoltaic panels)
        ECF_WT = 100  # kg CO2e m-2 (embodied carbon factor for wind turbines)
        ECF_BITES = 30  # kg CO2e m-3 (embodied carbon factor for BITES system)
        ECF_ST = 40  # kg CO2e m-3 (embodied carbon factor for solar thermal)
        ECF_PCM = 25  # kg CO2e m-3 (embodied carbon factor for PCM)
        ECF_Insulation = 10  # kg CO2e m-2 (embodied carbon factor for insulation materials)
        ECF_CoolRoof = 5  # kg CO2e m-2 (embodied carbon factor for cool roofing)

        # Total embodied carbon
        TotalEmbodiedCO2 = (PVSwitch * A_pv * ECF_PV + WTSwitch * A_wt * ECF_WT + BITESSwitch * V_bites * ECF_BITES + \
                            + STSwitch * A_st * ECF_ST + PCMSwitch * V_pcm * ECF_PCM + CRSwitch* A_CR * ECF_CoolRoof)*A_building \
                              + EnvSwitch * RvalueWall_quantity * A_walls * ECF_Insulation + EnvSwitch * RvalueRoof_quantity * A_Roof * ECF_Insulation\


        AnnVegCO2Saving = Additional_Trees * (CO2UptakeTree10Years / 10)
        # Calculate present worth for multiple variables
        #PresSCCSav = (-TotalEmbodiedCO2 / 1000) * SCC.iloc[0, 1]  # [$]
        #TotalCO2Sav = -TotalEmbodiedCO2

        print(TotalEmbodiedCO2,PresSCCSav)

        # Calculate present worth base and system cumulative gas and electricity cost
        for year in range(1, Nyears + 1):
            for month_idx, month in enumerate(months, start=0):
                # Construct the file names based on the template
                FilePathRetrofitDiurnal = PerfMetricsDiurnalFileNameRetrofit.format(month)
                FilePathBaseDiurnal = PerfMetricsDiurnalFileNameBase.format(month)

                # Check if the file exists before attempting to load
                if os.path.exists(FilePathRetrofitDiurnal) and os.path.exists(FilePathBaseDiurnal) :
                    # Load data from the file
                    #Diurnal
                    PerfMetricsDiurnalBase = pd.read_csv(FilePathBaseDiurnal, delimiter=',')
                    PerfMetricsDiurnalRetrofit = pd.read_csv(FilePathRetrofitDiurnal, delimiter=',')

                    #Total Energy Consumption
                    TotalGasConsumpHeatBase = TotalGasConsumpHeatBase + PerfMetricsDiurnalBase.iloc[:, 2].sum()
                    TotalGasConsumpWaterHeatBase = TotalGasConsumpWaterHeatBase + PerfMetricsDiurnalBase.iloc[:, 7].sum()

                    TotalGasConsumpHeatRetrofit = TotalGasConsumpHeatRetrofit + PerfMetricsDiurnalRetrofit.iloc[:, 2].sum()
                    TotalGasConsumpWaterHeatRetrofit = TotalGasConsumpWaterHeatRetrofit + PerfMetricsDiurnalRetrofit.iloc[:,7].sum()

                    TotalElecCoolDemandBase = TotalElecCoolDemandBase + PerfMetricsDiurnalBase.iloc[:,5].sum()
                    TotalElecDomesticDemandBase = TotalElecDomesticDemandBase + PerfMetricsDiurnalBase.iloc[:,10].sum()

                    TotalElecCoolDemandRetrofit = TotalElecCoolDemandRetrofit + PerfMetricsDiurnalRetrofit.iloc[:,5].sum()
                    TotalElecHeatDemandRetrofit = TotalElecHeatDemandRetrofit + PerfMetricsDiurnalRetrofit.iloc[:,3].sum()
                    TotalElecDomesticDemandRetrofit = TotalElecDomesticDemandRetrofit + PerfMetricsDiurnalRetrofit.iloc[:,10].sum()
                    TotalElecProducedPVRetrofit = TotalElecProducedPVRetrofit + PerfMetricsDiurnalRetrofit.iloc[:,8].sum()
                    TotalElecProducedWTRetrofit = TotalElecProducedWTRetrofit + PerfMetricsDiurnalRetrofit.iloc[:,9].sum()

                    # Total Energy Consumtion
                    MonthlyDiffFuelConsump =  PerfMetricsDiurnalBase.iloc[:, 2].sum() +PerfMetricsDiurnalBase.iloc[:, 7].sum() - \
                                      PerfMetricsDiurnalRetrofit.iloc[:, 2].sum() - PerfMetricsDiurnalRetrofit.iloc[:,7].sum()

                    MonthlyDiffElecConsump = PerfMetricsDiurnalBase.iloc[:,5].sum() + PerfMetricsDiurnalBase.iloc[:,10].sum() - \
                        (PerfMetricsDiurnalRetrofit.iloc[:,5].sum() + PerfMetricsDiurnalRetrofit.iloc[:,3].sum() + PerfMetricsDiurnalRetrofit.iloc[:,10].sum() - \
                          PerfMetricsDiurnalRetrofit.iloc[:,8].sum() -  PerfMetricsDiurnalRetrofit.iloc[:,9].sum())

                    # Saved CO2 [kg]
                    FuelCO2Saving = (MonthlyDiffFuelConsump) *  A_building * rhoCH4 * MWCO2 / MWCH4
                    ElecCO2Saving = (MonthlyDiffElecConsump) * A_building * (CarbonIntensityProjection.iloc[year-1,1] /100) *\
                                    ElecEmissionIntensity.iloc[8, Region] / 1000

                    TotalCO2Sav = TotalCO2Sav + (FuelCO2Saving + ElecCO2Saving + AnnVegCO2Saving/12)

                    #Social Cost of Carbon
                    PresSCCSav = PresSCCSav + ((FuelCO2Saving + ElecCO2Saving + AnnVegCO2Saving/12) / 1000) * SCC.iloc[year-1,1] * \
                                  1 / ((1 + EffIntRate) ** year)
                    #print(FuelCO2Saving,ElecCO2Saving, PresSCCSav)

                    # Gas Consumption Cost
                    PresBaseGasCost = PresBaseGasCost + (((PerfMetricsDiurnalBase.iloc[:,2] + PerfMetricsDiurnalBase.iloc[:,7]) * \
                       ON_NG_Residential_Rates.iloc[0,2]/100).sum() * A_building) *(1 + GasPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                    PresRetrofitGasCost = PresRetrofitGasCost + (((PerfMetricsDiurnalRetrofit.iloc[:,2] + PerfMetricsDiurnalRetrofit.iloc[:,7]) * \
                                           ON_NG_Residential_Rates.iloc[0,2]/100).sum() * A_building) *(1 + GasPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                    # Electricity Consumption Cost
                    if month is 'May 'or 'Jun' or 'Jul'or 'Aug' or'Sep' or'Oct':
                        PresBaseElecCost = PresBaseElecCost + (((PerfMetricsDiurnalBase.iloc[:,5] + PerfMetricsDiurnalBase.iloc[:,10]) *
                             ON_TOU_Electricity_Rates.iloc[:,1]/100).sum() * A_building) *  (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                        PresRetrofitElecCost = PresRetrofitElecCost + (((PerfMetricsDiurnalRetrofit.iloc[:,3] + PerfMetricsDiurnalRetrofit.iloc[:,5] + PerfMetricsDiurnalRetrofit.iloc[:,10]-\
                                        PerfMetricsDiurnalRetrofit.iloc[:,8] - PerfMetricsDiurnalRetrofit.iloc[:,9]) * ON_TOU_Electricity_Rates.iloc[:,1]/100).sum() * A_building) * \
                                          (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                    if month is 'Jan' or 'Feb' or 'Mar' or 'Apr' or 'Nov' or 'Dec':
                        PresBaseElecCost = PresBaseElecCost + (((PerfMetricsDiurnalBase.iloc[:,5] + PerfMetricsDiurnalBase.iloc[:,10]) * ON_TOU_Electricity_Rates.iloc[:,2]/100).sum() * A_building) * \
                                          (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

                        PresRetrofitElecCost = PresRetrofitElecCost + (((PerfMetricsDiurnalRetrofit.iloc[:,3] + PerfMetricsDiurnalRetrofit.iloc[:,5] + PerfMetricsDiurnalRetrofit.iloc[:,10]-\
                                        PerfMetricsDiurnalRetrofit.iloc[:,8] - PerfMetricsDiurnalRetrofit.iloc[:,9]) * ON_TOU_Electricity_Rates.iloc[:,2]/100).sum() * A_building) * \
                                          (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)
                else:
                    print('There are no building energy performance metrics files!')

            # Calculate the payment of Canada_Greener_Homes_Loan as Interest-free loans over 10 years
            if year <= FedLoanNyearsForgiveness:
                PresFedLoanPayment = PresFedLoanPayment + ((FedLoanCanGreener/FedLoanNyearsForgiveness) * (1 / ((1 + EffIntRate) ** year)))

            #Home Energy Loan Program (HELP) up to 20 years, interest-free
            #PV
            if year <= ProvHelPNyearsForgiveness:
                PresProvHELPPV = PresProvHELPPV + ((ProvHElPPV/ProvHelPNyearsForgiveness) * (1 / ((1 + EffIntRate) ** year)))
            #HP
            if year <= ProvHelPNyearsForgiveness:
                PresProvHELPHP = PresProvHELPHP + ((ProvHElPHP/ProvHelPNyearsForgiveness) * (1 / ((1 + EffIntRate) ** year)))

            # Calculate the payback period
            PresBaseOMCost = PresBaseOMCost + CAnnOMBase * A_building * 1 / ((1 + EffIntRate) ** year)
            PresRetrofitOMCost = PresRetrofitOMCost + CAnnOMRetrofit * 1 / ((1 + EffIntRate) ** year)

            SumAnnualCostDiff = PresFedLoanPayment + PVSwitch * PresProvHELPPV + HPSwitch * PresProvHELPHP + PresRetrofitGasCost +\
                PresRetrofitElecCost + PresRetrofitOMCost - PresBaseGasCost - PresBaseElecCost - PresBaseOMCost  - PresSCCSav


            PaybackDiff = SumAnnualCostDiff + CIniRetrofit - CIniBase * A_building
            print('Year, PaybackDiff = ', year, round(PaybackDiff))

            Payback.append(round(PaybackDiff))

            AnnualCO2Saving = FuelCO2Saving + ElecCO2Saving
            #print('Year, AnnualCO2Saving = ', year, round(AnnualCO2Saving))

            CO2Saving.append (round(AnnualCO2Saving))

        #Total Loan Payment
        PresLoanPayment = PresFedLoanPayment + PVSwitch * PresProvHELPPV + HPSwitch * PresProvHELPHP

        # Total Energy Consumtion
        DiffFuelConsump = TotalGasConsumpHeatBase + TotalGasConsumpWaterHeatBase - \
                          TotalGasConsumpHeatRetrofit - TotalGasConsumpWaterHeatRetrofit
        DiffElecConsump = TotalElecCoolDemandBase + TotalElecDomesticDemandBase - \
              (TotalElecCoolDemandRetrofit + TotalElecHeatDemandRetrofit + TotalElecDomesticDemandRetrofit - \
                                       TotalElecProducedPVRetrofit - TotalElecProducedWTRetrofit)

        Final_Analysis = FinalAnalysis(PresLoanPayment, PresBaseGasCost, PresRetrofitGasCost, PresBaseElecCost,
            PresRetrofitElecCost, SalFactorBase, CIniBase, A_building, PWFFullPeriod,SalFactor, CIniRetrofit,
             CAnnOMBase, CAnnIniBase, CAnnIniRetrofit, CAnnOMRetrofit, Additional_Trees, CO2UptakeTree10Years,
              DiffFuelConsump, DiffElecConsump, ElecEmissionIntensity, Region, Payback,outputFileNamePayback,
                 outputFileName, Nyears, CRFFullPeriod, FuelCO2Saving,ElecCO2Saving,
                                       CO2Saving,outputFileNameCO2Saving ,TotalCO2Sav,PresSCCSav)
