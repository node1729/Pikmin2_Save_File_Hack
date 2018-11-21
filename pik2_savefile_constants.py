class OFFSET:
    SAVE_FILE = 0x8
    SF_DAY_COUNTER = 0X14
    SF_POKO_COUNT = 0X2C
    SF_TREASURE_COUNT = 0X30
    SF_IGT = 0X3C
    DAY_COUNTER = 0X3E9
    EXPLORATION_KIT = 0X3ED
    PIKMIN_FALL = {"BLUE": 0X3F1,
                   "RED": 0X3FD,
                   "YELLOW": 0X409,
                   "PURPLE": 0X415,
                   "WHITE": 0X421,
                   "BULBMIN": 0X42D,
                   "PIKPIK": 0X439,}
    PIKMIN_SUB_OFFSET = {"LEAF": 0X0,
                         "BUD": 0X4,
                         "FLOWER": 0X8}
    PIKMIN_ONION = {"BLUE": 0X479,
                    "RED": 0X485,
                    "YELLOW": 0X491,
                    "PURPLE": 0X49D,
                    "WHITE": 0X4A9}

    TREASURE_START = 0X4CF
    EK_TREASURE_START = 0X58D
    POKO_COUNT = 0X834
    UNDERGROUND_POKO_COUNT = 0X838
    CHECKSUM = 0XBFFC

class EXPLORATION_KIT:
    EK_TREASURE_NAME = {"Brute Knuckles":           0B1,
                        "Dream Material":           0B10,
                        "Amplified Amplifier":      0B100,
                        "Professional Noisemaker":  0B1000,
                        "Stellar Orb":              0B10000,
                        "Justice Alloy":            0B100000,
                        "Forged Courage":           0B1000000,
                        "Repugnant Appendage":      0B10000000,
                        "Prototype Detector":       0B100000000,
                        "Five-man Napsack":         0B1000000000,
                        "Spherical Atlas":          0B10000000000,
                        "Geographic Projection":    0B100000000000}
