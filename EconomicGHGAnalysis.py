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
import pandas as pd
from EconomicGHGAnalysis.Toronto import Toronto
from EconomicGHGAnalysis.Vancouver import Vancouver
from EconomicGHGAnalysis.Calgary import Calgary
from EconomicGHGAnalysis.Saskatoon import Saskatoon
from EconomicGHGAnalysis.Winnipeg import Winnipeg
from EconomicGHGAnalysis.StJohns import StJohns
from EconomicGHGAnalysis.Halifax import Halifax
from EconomicGHGAnalysis.Yellowknife import Yellowknife
from EconomicGHGAnalysis.Whitehorse import Whitehorse
from EconomicGHGAnalysis.Montreal import Montreal

# Define lists instead of sets to maintain order
City = ['Toronto', 'Vancouver', 'Calgary', 'StJohns', 'Winnipeg', 'Saskatoon', 'Halifax', 'Montreal', 'Whitehorse', 'Yellowknife']
CaseName = ['PV', 'Retrofit', 'HP&BITES', 'ST', 'WT', 'CR', 'Retrofit&Re']
Elec_PriceInc = [0.01, 0.05, 0.1]
Gas_PriceInc = [0.01, 0.05, 0.1]

BaseCaseName = 'Base'

for city in City:
#---------------------------------------------------------1:Toronto-----------------------------------
    if city == 'Toronto':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Toronto(city, BaseCaseName, case, Scenario,
                                                                NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                                BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                                HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                                ElecPriceInc, GasPriceInc)
                        print(city,case,Scenario)
            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Toronto(city, BaseCaseName, case, Scenario,
                                                                NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                                BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                                HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                                ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'CR':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 1
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Toronto(city, BaseCaseName, case, Scenario,
                                                                NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                                BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                                HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                                ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Toronto(city, BaseCaseName, case, Scenario,
                                                                NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                                BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                                HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                                ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 1
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Toronto(city, BaseCaseName, case, Scenario,
                                                                NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                                BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                                HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                                ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

#____________________________________________2:Vancouver_________________________________________________________________
    if city == 'Vancouver':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Vancouver(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Vancouver(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Vancouver(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Vancouver(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# ___________________________________________3:Calgary__________________________________________________________________
    if city == 'Calgary':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Calgary(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Calgary(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Calgary(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# ___________________________________________________4:Saskatoon__________________________________________________________
    if city == 'Saskatoon':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Saskatoon(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Saskatoon(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Saskatoon(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Saskatoon(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# ___________________________________________________5:Winnipeg__________________________________________________________
    if city == 'Winnipeg':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Winnipeg(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Winnipeg(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Winnipeg(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Winnipeg(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# _________________________________________________6:StJohns____________________________________________________________
    if city == 'StJohns':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                        Scenario = 'SCC{}E'.format(ElecPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = StJohns(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                        Scenario = 'SCC{}E'.format(ElecPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = StJohns(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                        Scenario = 'SCC{}E'.format(ElecPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = StJohns(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc)
                print(city, case, Scenario)

# _________________________________________________7:Montreal____________________________________________________________
    if city == 'Montreal':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Montreal(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Montreal(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Montreal(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Montreal(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# ______________________________________________________8:Halifax_______________________________________________________
    if city == 'Halifax':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Halifax(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Halifax(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Halifax(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'ST':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 1
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Halifax(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 1
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Halifax(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# ________________________________________________9:Whitehorse_____________________________________________________________
    if city == 'Whitehorse':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Whitehorse(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'WT':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 1
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Whitehorse(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)
            if case == 'HP&BITES':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 1
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Whitehorse(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Whitehorse(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 1
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 1
                HPSwitch = 1
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Whitehorse(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      GasPriceInc, GasPriceInc)
                        print(city, case, Scenario)

# _____________________________________________________10:Yellowknife________________________________________________________
    if city == 'Yellowknife':  # Corrected equality check
        for case in CaseName:
            if case == 'PV':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 0
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 0
                CRSwitch = 0
                AirTSwitch = 0

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Yellowknife(city, BaseCaseName, case, Scenario,
                                                   NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                   BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                   HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                   ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)

            if case == 'Retrofit':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 0
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 0
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Yellowknife(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)


            if case == 'Retrofit&Re':  # Corrected equality check
                # Switches
                NVSwitch = 0
                WindowDoorReplaceSwitch = 1
                STSwitch = 0
                BITESSwitch = 0
                PCMSwitch = 0
                PVSwitch = 1
                WTSwitch = 0
                HPSwitch = 0
                EnvSwitch = 1
                CRSwitch = 1
                AirTSwitch = 1

                # Iterate through price increments
                for ElecPriceInc in Elec_PriceInc:
                    for GasPriceInc in Gas_PriceInc:
                        Scenario = 'SCC{}E{}F'.format(ElecPriceInc, GasPriceInc)

                        # Replace 'Toronto' with the actual function name that processes city data
                        EconomicGHGAnalysis = Yellowknife(city, BaseCaseName, case, Scenario,
                                                      NVSwitch, WindowDoorReplaceSwitch, STSwitch,
                                                      BITESSwitch, PCMSwitch, PVSwitch, WTSwitch,
                                                      HPSwitch, EnvSwitch, CRSwitch, AirTSwitch,
                                                      ElecPriceInc, GasPriceInc)
                        print(city, case, Scenario)


