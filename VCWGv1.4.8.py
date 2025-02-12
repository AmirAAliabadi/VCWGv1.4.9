from UWG import UWG
from BEMMonthly import BEMMonthly
from BEMDiurnal import BEMDiurnal
import os

# Define the .epw, .uwg filenames to create an UWG object.
# UWG will look for the .epw file in the UWG/resources/epw folder,
# and the .uwg file in the UWG/resources/parameters folder.

City= 'StJohns'
epw_filename = 'ERA5-{}-2010.epw'.format(City)
param_filename = 'initialize_{}_10.uwg'.format(City)        # .uwg file name
case_name = '{}-2020-Retrofit&RE-1'.format(City)
Adv_ene_heat_mode = 3
Month = 'Nov.txt'
OutputData = ['BEM', 'q_profiles', 'Tepw', 'TKE_profiles', 'Tr_profiles', 'Tu_profiles', 'U_profiles', 'V_profiles']

# Initialize the UWG object and run the simulation
uwg = UWG(epw_filename, param_filename,'','','','')
uwg.run()

BEMMonthly(Adv_ene_heat_mode, 'Output/Perf-Metrics-' + case_name + '-' + Month)
#BEMDiurnal(Adv_ene_heat_mode, 'Output/Perf-Metrics-Diurnal' + case_name + '-' + Month)

# Rename all hourly files
for output_type in OutputData:
    input_file = "Output/{}_hourly.txt".format(output_type)
    output_file = "Output/{}_hourly-{}-{}".format(output_type, case_name, Month)
    os.rename(input_file, output_file)
