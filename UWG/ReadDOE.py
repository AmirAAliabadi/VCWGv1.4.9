import sys
import os
import cPickle

from BuildingEnergy import Building
from Material import Material
from Element import Element
from BEMDef import BEMDef
from schdef import SchDef
from Utilities import read_csv, str2fl
import Utilities

"""
Developed by Bruno Bueno, Mojtaba Safdari, Amir A. Aliabadi
Building Technology, Massachusetts Institute of Technology (MIT), Cambridge, U.S.A.
Last update: 2024-02-20
"""

DIR_CURR = os.path.abspath(os.path.dirname(__file__))
DIR_DOE_PATH = os.path.join(DIR_CURR,"..","resources","DOERefBuildings")

# Define standards: NBuildingTypes building types, 3 built eras, NClimateZones climate zones

# DOE Building Types
BLDTYPE = [
    'FullServiceRestaurant',    # 1
    'Hospital',                 # 2
    'LargeHotel',               # 3
    'LargeOffice',              # 4
    'MedOffice',                # 5
    'MidRiseApartment',         # 6
    'OutPatient',               # 7
    'PrimarySchool',            # 8
    'QuickServiceRestaurant',   # 9
    'SecondarySchool',          # 10
    'SmallHotel',               # 11
    'SmallOffice',              # 12
    'StandAloneRetail',         # 13
    'StripMall',                # 14
    'SuperMarket',              # 15
    'WareHouse']                # 16

BUILTERA = [
    'Pre80',                    # 1
    'Pst80',                    # 2
    'New'                       # 3
    ]

ZONETYPE = [
    '1A (Miami)',               # 1
    '2A (Houston)',             # 2
    '2B (Phoenix)',             # 3
    '3A (Atlanta)',             # 4
    '3B-CA (Los Angeles)',      # 5
    '3B (Las Vegas)',           # 6
    '3C (San Francisco)',       # 7
    '4A (Baltimore)',           # 8
    '4B (Albuquerque)',         # 9
    '4C (Seattle)',             # 10
    '5A (Chicago)',             # 11
    '5B (Boulder)',             # 12
    '6A (Minneapolis)',         # 13
    '6B (Helena)',              # 14
    '7 (Duluth)',               # 15
    '8 (Fairbanks)',            # 16
    '5A (Guelph)'               # 17
    ]

def readDOE(serialize_output=True):

    """
    Read csv files of DOE buildings
    Sheet 1 = BuildingSummary
    Sheet 2 = ZoneSummary
    Sheet 3 = LocationSummary
    Sheet 4 = Schedules
    Note BLD8 & 10 = school


    Then make matrix of ref data as nested nested lists [NBuildingTypes, 3, NClimateZones]:
    matrix refDOE = Building objs
    matrix Schedule = SchDef objs
    matrix refBEM (NBuildingTypes,3,NClimateZones) = BEMDef
    where:
        [NBuildingTypes,3,17] is Type = 1-NBuildingTypes, Era = 1-3, climate zone = 1-NClimateZones
        i.e.
        Type: FullServiceRestaurant, Era: Pre80, Zone: 6A Minneapolis
    Nested tree:
    [TYPE_1:
        ERA_1:
            CLIMATE_ZONE_1
            ...
            CLIMATE_ZONE_NClimateZones
        ERA_2:
            CLIMATE_ZONE_1
            ...
            CLIMATE_ZONE_NClimateZones
        ...
        ERA_3:
            CLIMATE_ZONE_1
            ...
            CLIMATE_ZONE_NClimateZones]

    """

    NClimateZones = 17
    NBuildingTypes = 16

    #Nested, nested lists of Building, SchDef, BEMDef objects
    refDOE = map(lambda j_: map (lambda k_: [None]*NClimateZones,[None]*3), [None]*NBuildingTypes)     #refDOE(NClimateZones,3,NBuildingTypes) = Building;
    Schedule = map(lambda j_: map (lambda k_: [None]*NClimateZones,[None]*3), [None]*NBuildingTypes)   #Schedule (NClimateZones,3,NBuildingTypes) = SchDef;
    refBEM = map(lambda j_: map (lambda k_: [None]*NClimateZones,[None]*3), [None]*NBuildingTypes)     #refBEM (NClimateZones,3,NBuildingTypes) = BEMDef;

    #Purpose: Loop through every DOE reference csv and extract building data
    #Nested loop = NBuildingTypes types, 3 era, NClimateZones zones

    for i in xrange(NBuildingTypes):

        # Read building summary (Sheet 1)
        file_doe_name_bld = os.path.join("{}".format(DIR_DOE_PATH), "BLD{}".format(i+1),"BLD{}_BuildingSummary.csv".format(i+1))
        list_doe1 = read_csv(file_doe_name_bld)
        #listof(listof 3 era values)
        nFloor      = str2fl(list_doe1[3][3:6])      # Number of Floors, this will be list of floats and str if "basement"
        glazing     = str2fl(list_doe1[4][3:6])      # Ratio Total
        hCeiling    = str2fl(list_doe1[5][3:6])      # [m] Ceiling height
        ver2hor     = str2fl(list_doe1[7][3:6])      # Wall to Skin Ratio
        AreaRoof    = str2fl(list_doe1[8][3:6])      # [m2] Gross Dimensions - Total area

        # Read zone summary (Sheet 2)
        file_doe_name_zone = os.path.join("{}".format(DIR_DOE_PATH), "BLD{}".format(i+1),"BLD{}_ZoneSummary.csv".format(i+1))
        list_doe2 = read_csv(file_doe_name_zone)
        #listof(listof 3 eras)
        AreaFloor   = str2fl([list_doe2[2][5],list_doe2[3][5],list_doe2[4][5]])       # [m^2]
        Volume      = str2fl([list_doe2[2][6],list_doe2[3][6],list_doe2[4][6]])       # [m^3]
        AreaWall    = str2fl([list_doe2[2][8],list_doe2[3][8],list_doe2[4][8]])       # [m^2]
        AreaWindow  = str2fl([list_doe2[2][9],list_doe2[3][9],list_doe2[4][9]])       # [m^2]
        Occupant    = str2fl([list_doe2[2][11],list_doe2[3][11],list_doe2[4][11]])    # Number of People
        Light       = str2fl([list_doe2[2][12],list_doe2[3][12],list_doe2[4][12]])    # [W m^-2]
        Elec        = str2fl([list_doe2[2][13],list_doe2[3][13],list_doe2[4][13]])    # [W m^-2] Electric Plug and Process
        Gas         = str2fl([list_doe2[2][14],list_doe2[3][14],list_doe2[4][14]])    # Gas Plug and Process per unit floor area [W m^-2]
        SHW         = str2fl([list_doe2[2][15],list_doe2[3][15],list_doe2[4][15]])    # Peak Service Hot Water per unit floor [kg hr^-1 m^-2]
        Vent        = str2fl([list_doe2[2][17],list_doe2[3][17],list_doe2[4][17]])    # [L s^-1 m^-2] Ventilation rate per unit floor area
        Infil       = str2fl([list_doe2[2][20],list_doe2[3][20],list_doe2[4][20]])    # Infiltration Air Change per Hour (ACH) [hr^-1]

        # Read location summary (Sheet 3)
        file_doe_name_location = os.path.join("{}".format(DIR_DOE_PATH), "BLD{}".format(i+1),"BLD{}_LocationSummary.csv".format(i+1))
        list_doe3 = read_csv(file_doe_name_location)
        #(listof (listof 3 eras (listof NClimateZones climate types)))
        TypeWall    = [list_doe3[3][4:NClimateZones+4],list_doe3[14][4:NClimateZones+4],list_doe3[25][4:NClimateZones+4]]             # Construction type
        RvalWall    = str2fl([list_doe3[4][4:NClimateZones+4],list_doe3[15][4:NClimateZones+4],list_doe3[26][4:NClimateZones+4]])     # [m^2 K W^-1] R-value
        TypeRoof    = [list_doe3[5][4:NClimateZones+4],list_doe3[16][4:NClimateZones+4],list_doe3[27][4:NClimateZones+4]]             # Construction type
        RvalRoof    = str2fl([list_doe3[6][4:NClimateZones+4],list_doe3[17][4:NClimateZones+4],list_doe3[28][4:NClimateZones+4]])     # [m^2 K W^-1] R-value
        Uwindow     = str2fl([list_doe3[7][4:NClimateZones+4],list_doe3[18][4:NClimateZones+4],list_doe3[29][4:NClimateZones+4]])     # [W m^-2 K^-1] U-factor
        SHGC        = str2fl([list_doe3[8][4:NClimateZones+4],list_doe3[19][4:NClimateZones+4],list_doe3[30][4:NClimateZones+4]])     # [-] coefficient
        HVAC        = str2fl([list_doe3[9][4:NClimateZones+4],list_doe3[20][4:NClimateZones+4],list_doe3[31][4:NClimateZones+4]])     # [kW] Air Conditioning
        HEAT        = str2fl([list_doe3[10][4:NClimateZones+4],list_doe3[21][4:NClimateZones+4],list_doe3[32][4:NClimateZones+4]])    # [kW] Heating
        COP         = str2fl([list_doe3[11][4:NClimateZones+4],list_doe3[22][4:NClimateZones+4],list_doe3[33][4:NClimateZones+4]])    # [-] Air Conditioning COP
        EffHeat     = str2fl([list_doe3[12][4:NClimateZones+4],list_doe3[23][4:NClimateZones+4],list_doe3[34][4:NClimateZones+4]])    # [%] Heating Efficiency
        FanFlow     = str2fl([list_doe3[13][4:NClimateZones+4],list_doe3[24][4:NClimateZones+4],list_doe3[35][4:NClimateZones+4]])    # [m^3 s^-1] Fan Max Flow Rate

        # Read Schedules (Sheet 4)
        file_doe_name_schedules = os.path.join("{}".format(DIR_DOE_PATH), "BLD{}".format(i+1),"BLD{}_Schedules.csv".format(i+1))
        list_doe4 = read_csv(file_doe_name_schedules)

        #listof(listof weekday, sat, sun (list of 24 fractions)))
        SchEquip    = str2fl([list_doe4[1][6:30],list_doe4[2][6:30],list_doe4[3][6:30]])      # Equipment Schedule 24 hrs
        SchLight    = str2fl([list_doe4[4][6:30],list_doe4[5][6:30],list_doe4[6][6:30]])      # Light Schedule 24 hrs; Wkday=Sat=Sun=Hol
        SchOcc      = str2fl([list_doe4[7][6:30],list_doe4[8][6:30],list_doe4[9][6:30]])      # Occupancy Schedule 24 hrs
        SetCool     = str2fl([list_doe4[10][6:30],list_doe4[11][6:30],list_doe4[12][6:30]])   # Cooling Setpoint Schedule 24 hrs [K]
        SetHeat     = str2fl([list_doe4[13][6:30],list_doe4[14][6:30],list_doe4[15][6:30]])   # Heating Setpoint Schedule 24 hrs; summer design [K]
        SchGas      = str2fl([list_doe4[16][6:30],list_doe4[17][6:30],list_doe4[18][6:30]])   # Gas Equipment Schedule 24 hrs; wkday=sat
        SchSWH      = str2fl([list_doe4[19][6:30],list_doe4[20][6:30],list_doe4[21][6:30]])   # Solar Water Heating Schedule 24 hrs; wkday=summerdesign, sat=winterdesgin
        RHSetCool   = str2fl([list_doe4[22][6:30], list_doe4[23][6:30], list_doe4[24][6:30]]) # Cooling RH Setpoint Schedule 24 hrs [%]
        RHSetHeat   = str2fl([list_doe4[25][6:30], list_doe4[26][6:30], list_doe4[27][6:30]]) # Heating RH Setpoint Schedule 24 hrs; summer design [%]

        for j in xrange(3):

            for k in xrange(NClimateZones):

                B = Building(
                    hCeiling[j],                        # floorHeight by area
                    1,                                  # intHeatNight
                    1,                                  # intHeatDay
                    0.1,                                # intHeatFRad
                    0.1,                                # intHeatFLat
                    Infil[j],                           # infiltration rate Air Change per Hour (ACH) [hr^-1]
                    Vent[j]/1000.,                      # ventilation rate per unit floor area converted from liters to cubic meter [m^3 s^-1 m^-2]
                    glazing[j],                         # glazing ratio by area
                    Uwindow[j][k],                      # uValue by area, by climate type
                    SHGC[j][k],                         # SHGC, by area, by climate type
                    'AIR',                              # cooling condensation system type: AIR, WATER
                    COP[j][k],                          # cop by area, climate type
                    297,                                # coolSetpointDay [K]
                    297,                                # coolSetpointNight [K]
                    293,                                # heatSetpointDay [K]
                    293,                                # heatSetpointNight [K]
                    60,                                 # coolRHSetpointDay [%]
                    60,                                 # coolRHSetpointNight [%]
                    40,                                 # heatRHSetpointDay [%]
                    40,                                 # heatRHSetpointNight [%]
                    (HVAC[j][k]*1000.0)/AreaFloor[j],   # coolCap converted from kW per entire floor area to Watt per unit floor area [W m^-2]
                    EffHeat[j][k],                      # heatEff by area, climate type
                    293,                                # initialTemp [K]
                    0.006)                              # initialTemp specific humidity  [kgv kga^-1]

                #Not defined in the constructor
                B.heatCap = (HEAT[j][k]*1000.0)/AreaFloor[j]         # heating Capacity converted to [W m^-2] by area, climate type
                B.Type = BLDTYPE[i]
                B.Era = BUILTERA[j]
                B.Zone = ZONETYPE[k]
                refDOE[i][j][k] = B

                # Define wall, mass(floor), roof
                # Reference from E+ for conductivity, thickness (reference below)

                # Material: (thermalCond, volHeat = specific heat * density)
                # Concrete = Material (1.311, 836.8 * 2240,"Concrete")
                # Insulation = Material (0.049, 836.8 * 265.0, "Insulation")
                # Gypsum = Material (0.16, 830.0 * 784.9, "Gypsum")
                # Wood = Material (0.11, 1210.0 * 544.62, "Wood")
                # Stucco = Material(0.6918,  837.0 * 1858.0, "Stucco")

                # Wall (1 in stucco, concrete, insulation, gypsum)
                # Check TypWall by area, by climate
                if TypeWall[j][k] == "MassWall":
                    #Construct wall based on R value of Wall from refDOE and properties defined above
                    # 1" stucco, 8" concrete, tbd insulation, 1/2" gypsum
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material (0.049, 836.8 * 265.0, "Insulation")
                    Gypsum = Material(0.17, 870.0 * 625.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    Brick = Material(0.52, 900 * 899, "Brick")
                    Rbase = 0.271087 # R val based on stucco, concrete, gypsum
                    Rins = RvalWall[j][k] - Rbase #find insulation value
                    D_ins = Rins * Insulation.thermalCond # depth of insulation [m^2 K W^-1 W m^-1 K^-1] = [m]
                    if D_ins > 0.01:
                        thickness = [0.0254,0.0508,0.0508,0.0508,0.0508,D_ins,0.0127]
                        layers = [Brick,Concrete,Concrete,Concrete,Concrete,Insulation,Gypsum]
                    else:
                        #if it's less then 1 cm don't include in layers
                        thickness = [0.0254,0.0508,0.0508,0.0508,0.0508,0.0127]
                        layers = [Brick,Concrete,Concrete,Concrete,Concrete,Gypsum]

                    # wall = Element(0.08,0.92,thickness,layers,0.,293.,0.,"MassWall")
                    # thickness = [0.015,0.06,0.05,0.12,0.015]
                    # lay1 = Material(0.8,1820*863.90,"LimePlaster")
                    # lay2 = Material(0.52, 900 * 899, "brick1")
                    # lay3 = Material (0.049, 836.8 * 265.0, "Insulation")
                    # lay4 = Material(1.1, 900 * 2000, "brick2")
                    # lay5 = Material(0.16, 830.0 * 784.9, "Gypsum")
                    # layers = [lay1,lay2,lay3,lay4,lay5]
                    wall = Element(thickness, layers, 0., 293., 0., "MassWall")

                    # If mass wall, assume mass floor (4" concrete)
                    # Mass (assume 4" concrete);
                    alb = 0.2
                    emis = 0.9
                    thickness = [0.054,0.054]
                    concrete = Material (1.31, 2240.0*836.8)
                    mass = Element(thickness, [concrete, concrete], 0, 293, 1, "MassFloor")

                elif TypeWall[j][k] == "WoodFrame":
                    # 0.01m wood siding, tbd insulation, 1/2" gypsum
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material(0.049, 836.8 * 265.0, "Insulation")
                    Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    Rbase = 0.170284091    # based on wood siding, gypsum
                    Rins = RvalWall[j][k] - Rbase
                    D_ins = Rins * Insulation.thermalCond #depth of insulation

                    if D_ins > 0.01:
                        thickness = [0.01,D_ins,0.0127]
                        layers = [Wood,Insulation,Gypsum]
                    else:
                        thickness = [0.01,0.0127]
                        layers = [Wood,Gypsum]

                    wall = Element(thickness, layers, 0., 293., 0., "WoodFrameWall")

                    # If wood frame wall, assume wooden floor
                    alb = 0.2
                    emis = 0.9
                    thickness = [0.05,0.05]
                    wood = Material(1.31, 2240.0*836.8)
                    mass = Element(thickness, [wood, wood], 0., 293., 1., "WoodFloor")

                elif TypeWall[j][k] == "SteelFrame":
                    # 1" stucco, 8" concrete, tbd insulation, 1/2" gypsum
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material(0.049, 836.8 * 265.0, "Insulation")
                    Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    Rbase = 0.271087 # based on stucco, concrete, gypsum
                    Rins = RvalWall[j][k] - Rbase
                    D_ins = Rins * Insulation.thermalCond
                    if D_ins > 0.01:
                        thickness = [0.0254,0.0508,0.0508,0.0508,0.0508,D_ins,0.0127]
                        layers = [Stucco,Concrete,Concrete,Concrete,Concrete,Insulation,Gypsum]
                    else:    # If insulation is too thin, assume no insulation
                        thickness = [0.0254,0.0508,0.0508,0.0508,0.0508,0.0127]
                        layers = [Stucco,Concrete,Concrete,Concrete,Concrete,Gypsum]
                    wall = Element(thickness, layers, 0., 293., 0., "SteelFrame")

                    # If mass wall, assume mass floor
                    # Mass (assume 4" concrete),
                    alb = 0.2
                    emis = 0.93
                    thickness = [0.05,0.05]
                    mass = Element(thickness, [Concrete, Concrete], 0., 293., 1., "MassFloor")

                elif TypeWall[j][k] == "MetalWall":
                    # metal siding, insulation, 1/2" gypsum
                    alb = 0.2
                    emis = 0.9
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material(0.049, 836.8 * 265.0, "Insulation")
                    Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    D_ins = max((RvalWall[j][k] * Insulation.thermalCond)/2, 0.01) #use derived insulation thickness or 0.01 based on max
                    thickness = [D_ins,D_ins,0.0127]
                    materials = [Insulation,Insulation,Gypsum]
                    wall = Element(thickness, materials, 0, 293, 0, "MetalWall")

                    # Mass (assume 4" concrete);
                    alb = 0.2
                    emis = 0.9
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material(0.049, 836.8 * 265.0, "Insulation")
                    Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    thickness = [0.05, 0.05]
                    concrete = Material(1.31, 2240.0*836.8)
                    mass = Element(thickness, [concrete, concrete], 0., 293., 1., "MassFloor")

                elif TypeWall[j][k] == "EPPWall":
                    # Blue Valley EPP
                    alb = 0.2
                    emis = 0.9
                    # EPP material "effective overall" conductivity and volumetric heat capacity
                    EPPWall = Material(0.067, 289010, "EPPWall")
                    # Calculate layer thickness assuming 3 layers
                    D_ins = max((RvalWall[j][k] * EPPWall.thermalCond) / 3, 0.01)
                    thickness = [D_ins, D_ins, D_ins]
                    material = [EPPWall, EPPWall, EPPWall]
                    wall = Element(thickness, material, 0, 293, 0, "EPPWall")

                    # Mass (assume 4" concrete);
                    alb = 0.2
                    emis = 0.9
                    # EPP material "effective overall" conductivity and volumetric heat capacity
                    EPPFloor = Material(0.094, 1258814, "EPPFloor")
                    #  Calculate layer thickness assuming 3 layers
                    D_ins = max((3.801 * EPPFloor.thermalCond) / 3, 0.01)
                    thickness = [D_ins, D_ins, D_ins]
                    material = [EPPFloor, EPPFloor, EPPFloor]
                    mass = Element(thickness, material, 0., 293., 1., "EPPFloor")

                # Roof
                if TypeRoof[j][k] == "IEAD": #Insulation Entirely Above Deck
                    # IEAD-> membrane, insulation, decking
                     alb = 0.2
                     emis = 0.93
                     Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                     Insulation = Material(0.049, 836.8 * 265.0, "Insulation")
                     Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                     Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                     Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                     D_ins = max(RvalRoof[j][k] * Insulation.thermalCond/2.,0.01);
                     roof = Element([D_ins, D_ins], [Insulation, Insulation], 0., 293., 0., "IEAD")

                elif TypeRoof[j][k] == "Attic":
                    # IEAD-> membrane, insulation, decking
                    alb = 0.2
                    emis = 0.9
                    # D_ins = max(RvalRoof[j][k] * Insulation.thermalCond/2.,0.01)
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material(1.3, 1800000, "Insulation")
                    Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    D_ins = 0.2
                    roof = Element([D_ins, D_ins], [Insulation, Insulation], 0., 293., 0., "Attic")

                elif TypeRoof[j][k] == "MetalRoof":
                    # IEAD-> membrane, insulation, decking
                    alb = 0.2
                    emis = 0.9
                    Concrete = Material(1.311, 836.8 * 2240, "Concrete")
                    Insulation = Material(0.049, 836.8 * 265.0, "Insulation")
                    Gypsum = Material(0.16, 830.0 * 784.9, "Gypsum")
                    Wood = Material(0.11, 1210.0 * 544.62, "Wood")
                    Stucco = Material(0.6918, 837.0 * 1858.0, "Stucco")
                    D_ins = max(RvalRoof[j][k] * Insulation.thermalCond/2.,0.01)
                    roof = Element([D_ins, D_ins], [Insulation, Insulation], 0., 293., 0., "MetalRoof")

                elif TypeRoof[j][k] == "EPPRoof":
                    alb = 0.2
                    emis = 0.9
                    # EPP material "effective overall" conductivity and volumetric heat capacity
                    EPPRoof = Material(0.062, 195080, "EPPRoof")
                    # Calculate layer thickness assuming 3 layers
                    D_ins = max((RvalRoof[j][k] * EPPRoof.thermalCond) / 3, 0.01)
                    thickness = [D_ins, D_ins, D_ins]
                    material = [EPPRoof, EPPRoof, EPPRoof]
                    roof = Element(thickness, material, 0, 293, 0, "EPPRoof")

                # Define building energy model, set fraction of the urban floor space of this typology to zero
                refBEM[i][j][k] = BEMDef(B, mass, wall, roof, 0.0)

                Schedule[i][j][k] = SchDef()

                Schedule[i][j][k].Elec = SchEquip     # 3x24 matrix of schedule for fraction electricity (WD,Sat,Sun)
                Schedule[i][j][k].Light = SchLight    # 3x24 matrix of schedule for fraction light (WD,Sat,Sun)
                Schedule[i][j][k].Gas = SchGas        # 3x24 matrix of schedule for fraction gas (WD,Sat,Sun)
                Schedule[i][j][k].Occ = SchOcc        # 3x24 matrix of schedule for fraction occupancy (WD,Sat,Sun)
                Schedule[i][j][k].Cool = SetCool      # 3x24 matrix of schedule for fraction cooling temp (WD,Sat,Sun) [K]
                Schedule[i][j][k].Heat = SetHeat      # 3x24 matrix of schedule for fraction heating temp (WD,Sat,Sun) [K]
                Schedule[i][j][k].SWH = SchSWH        # 3x24 matrix of schedule for fraction SWH (WD,Sat,Sun)
                Schedule[i][j][k].RHCool = RHSetCool  # 3x24 matrix of schedule for fraction cooling RH (WD,Sat,Sun) [%]
                Schedule[i][j][k].RHHeat = RHSetHeat  # 3x24 matrix of schedule for fraction heating RH (WD,Sat,Sun) [%]

                Schedule[i][j][k].Qelec = Elec[j]                   # [W m^-2] (max) for electrical plug process
                Schedule[i][j][k].Qlight = Light[j]                 # [W m^-2] (max) for light
                Schedule[i][j][k].Nocc = Occupant[j]/AreaFloor[j]   # [Person m^-2]
                Schedule[i][j][k].Qgas = Gas[j]                     # [W m^-2] (max) for gas
                Schedule[i][j][k].Vent = Vent[j]/1000.0             # [m^3 m^-2] per person
                Schedule[i][j][k].Vswh = SHW[j]/AreaFloor[j]        # litres per hour per m^2 of floor


    # if not test serialize refDOE,refBEM,Schedule and store in resources
    if not serialize_output:

        # create a binary file for serialized obj
        pkl_file_path = os.path.join(DIR_CURR,'readDOE.pkl')
        pickle_readDOE = open(pkl_file_path, 'wb')

        # dump in ../resources
        # Pickle objects, protocol 1 b/c binary file
        cPickle.dump(refDOE, pickle_readDOE,1)
        cPickle.dump(refBEM, pickle_readDOE,1)
        cPickle.dump(Schedule, pickle_readDOE,1)

        pickle_readDOE.close()

    return refDOE, refBEM, Schedule

if __name__ == "UWG.ReadDOE": # "__main__":#

    # Set to True only if you want create new .pkls of DOE refs
    # Use --serialize switch to serialize the readDOE data
    print(sys.argv)
    if len(sys.argv)> 1 and sys.argv[1]=="--serialize":
        refDOE, refBEM, Schedule = readDOE(True)
    else:
        refDOE, refBEM, Schedule = readDOE(False)


# Material ref from E+
#     1/2IN Gypsum,            !- Name
#     Smooth,                  !- Roughness
#     0.0127,                  !- Thickness [m]
#     0.1600,                  !- Conductivity [W m^-1 K^-1]
#     784.9000,                !- Density [kg m^-3]
#     830.0000,                !- Specific Heat [J kg^-1 K^-1]
#     0.9000,                  !- Thermal Absorptance
#     0.9200,                  !- Solar Absorptance
#     0.9200;                  !- Visible Absorptance
#
# Material,
#     1IN Stucco,              !- Name
#     Smooth,                  !- Roughness
#     0.0253,                  !- Thickness
#     0.6918,                  !- Conductivity
#     1858.0000,               !- Density
#     837.0000,                !- Specific Heat
#     0.9000,                  !- Thermal Absorptance
#     0.9200,                  !- Solar Absorptance
#     0.9200;                  !- Visible Absorptance
#
# Material,
#     8IN CONCRETE HW,  !- Name
#     Rough,                   !- Roughness
#     0.2032,                  !- Thickness
#     1.3110,                  !- Conductivity
#     2240.0000,               !- Density
#     836.8000,                !- Specific Heat
#     0.9000,                  !- Thermal Absorptance
#     0.7000,                  !- Solar Absorptance
#     0.7000;                  !- Visible Absorptance
#
# Material,
#     Mass NonRes Wall Insulation, !- Name
#     MediumRough,             !- Roughness
#     0.0484268844343858,      !- Thickness
#     0.049,                   !- Conductivity
#     265.0000,                !- Density
#     836.8000,                !- Specific Heat
#     0.9000,                  !- Thermal Absorptance
#     0.7000,                  !- Solar Absorptance
#     0.7000;                  !- Visible Absorptance
#
# Material,
#     Std Wood 6inch,          !- Name
#     MediumSmooth,            !- Roughness
#     0.15,                    !- Thickness
#     0.12,                    !- Conductivity
#     540.0000,                !- Density
#     1210,                    !- Specific Heat
#     0.9000000,               !- Thermal Absorptance
#     0.7000000,               !- Solar Absorptance
#     0.7000000;               !- Visible Absorptance! Common Materials
#
# Material,
#     Wood Siding,             !- Name
#     MediumSmooth,            !- Roughness
#     0.0100,                  !- Thickness
#     0.1100,                  !- Conductivity
#     544.6200,                !- Density
#     1210.0000,               !- Specific Heat
#     0.9000,                  !- Thermal Absorptance
#     0.7800,                  !- Solar Absorptance
#     0.7800;                  !- Visible Absorptance
