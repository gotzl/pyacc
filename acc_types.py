from ctypes import LittleEndianStructure, c_int, c_float, Array, wintypes
from enum import IntEnum


class SPageFilePhysics(LittleEndianStructure):
    _fields_ = [
        ('packetId', c_int),
        ('gas', c_float),
        ('brake', c_float),
        ('fuel', c_float),
        ('gear', c_int),
        ('rpms', c_int),
        ('steerAngle', c_float),
        ('speedKmh', c_float),
        ('velocity', c_float * 3),
        ('accG', c_float * 3),
        ('wheelSlip', c_float * 4),
        ('wheelLoad', c_float * 4),
        ('wheelsPressure', c_float * 4),
        ('wheelAngularSpeed', c_float * 4),
        ('tyreWear', c_float * 4),
        ('tyreDirtyLevel', c_float * 4),
        ('tyreCoreTemperature', c_float * 4),
        ('camberRAD', c_float * 4),
        ('suspensionTravel', c_float * 4),
        ('drs', c_float),
        ('tc', c_float),
        ('heading', c_float),
        ('pitch', c_float),
        ('roll', c_float),
        ('cgHeight', c_float),
        ('carDamage', c_float * 5),
        ('numberOfTyresOut', c_int),
        ('pitLimiterOn', c_int),
        ('abs', c_float),
        ('kersCharge', c_float),
        ('kersInput', c_float),
        ('autoShifterOn', c_int),
        ('rideHeight', c_float * 2),
        ('turboBoost', c_float),
        ('ballast', c_float),
        ('airDensity', c_float),
        ('airTemp', c_float),
        ('roadTemp', c_float),
        ('localAngularVel', c_float * 3),
        ('finalFF', c_float),
        ('performanceMeter', c_float),
        ('engineBrake', c_int),
        ('ersRecoveryLevel', c_int),
        ('ersPowerLevel', c_int),
        ('ersHeatCharging', c_int),
        ('ersIsCharging', c_int),
        ('kersCurrentKJ', c_int),
        ('drsAvailable', c_int),
        ('drsEnabled', c_int),
        ('brakeTemp', c_float * 4),
        ('clutch', c_float),
        ('tyreTempI', c_float * 4),
        ('tyreTempM', c_float * 4),
        ('tyreTempO', c_float * 4),
        ('isAIControlled', c_int),
        ('tyreContactPoint', c_float * 3 * 4),
        ('tyreContactNormal', c_float * 3 * 4),
        ('tyreContactHeading', c_float * 3 * 4),
        ('brakeBias', c_float),
        ('localVelocity', c_float * 3),
        ('P2PActivations', c_int),
        ('P2PStatus', c_int),
        ('currentMaxRpm', c_int),
        ('mz', c_float * 4),
        ('fx', c_float * 4),
        ('fy', c_float * 4),
        ('slipRatio', c_float * 4),
        ('slipAngle', c_float * 4),
        ('tcInAction', c_int),
        ('absInAction', c_int),
        ('suspensionDamage', c_float * 4),
        ('tyreTemp', c_float * 4),
        ('waterTemp', c_float),
        ('brakePressure', c_float * 4),
        ('frontBrakeCompound', c_int),
        ('rearBrakeCompound', c_int),
        ('padLife', c_float * 4),
        ('discLife', c_float * 4),
        ('ignitionOn', c_int),
        ('starterEngineOn', c_int),
        ('kerbVibration', c_float),
        ('slipVibrations', c_float),
        ('gVibrations', c_float),
        ('absVibrations', c_float),
    ]


class ShortWord(Array):
    _type_ = wintypes.WORD
    _length_ = 15

    def __str__(self):
        try:
            return bytes(self).decode('utf-16-le').rstrip('\x00')
        except UnicodeDecodeError as e:
            return ""


class Word(Array):
    _type_ = wintypes.WORD
    _length_ = 33

    def __str__(self):
        try:
            return bytes(self).decode('utf-16-le').rstrip('\x00')
        except UnicodeDecodeError as e:
            return ""


# https://gist.github.com/christoph2/9c390e5c094796903097
class StructureWithEnums(LittleEndianStructure):
    """Add missing enum feature to ctypes Structures.
    """
    _map = {}

    def __getattribute__(self, name):
        _map = LittleEndianStructure.__getattribute__(self, '_map')
        value = LittleEndianStructure.__getattribute__(self, name)
        if name in _map:
            EnumClass = _map[name]
            if isinstance(value, Array):
                return [EnumClass(x) for x in value]
            else:
                return EnumClass(value)
        else:
            return value

    def __str__(self):
        result = []
        result.append("struct {0} {{".format(self.__class__.__name__))
        for field in self._fields_:
            attr, attrType = field
            if attr in self._map:
                attrType = self._map[attr]
            value = getattr(self, attr)
            result.append("    {0} [{1}] = {2!r};".format(attr, attrType.__name__, value))
        result.append("};")
        return '\n'.join(result)

    __repr__ = __str__


class ACC_FLAG_TYPE(IntEnum):
    ACC_NO_FLAG = 0
    ACC_BLUE_FLAG = 1
    ACC_YELLOW_FLAG = 2
    ACC_BLACK_FLAG = 3
    ACC_WHITE_FLAG = 4
    ACC_CHECKERED_FLAG = 5
    ACC_PENALTY_FLAG = 6
    ACC_GREEN_FLAG = 7
    ACC_ORANGE_FLAG = 8

class ACC_PENALTY_TYPE(IntEnum):
    ACC_None = 0
    ACC_DriveThrough_Cutting = 1
    ACC_StopAndGo_10_Cutting = 2
    ACC_StopAndGo_20_Cutting = 3
    ACC_StopAndGo_30_Cutting = 4
    ACC_Disqualified_Cutting = 5
    ACC_RemoveBestLaptime_Cutting = 6
    ACC_DriveThrough_PitSpeeding = 7
    ACC_StopAndGo_10_PitSpeeding = 8
    ACC_StopAndGo_20_PitSpeeding = 9
    ACC_StopAndGo_30_PitSpeeding = 10
    ACC_Disqualified_PitSpeeding = 11
    ACC_RemoveBestLaptime_PitSpeeding = 12
    ACC_Disqualified_IgnoredMandatoryPit = 13
    ACC_PostRaceTime = 14
    ACC_Disqualified_Trolling = 15
    ACC_Disqualified_PitEntry = 16
    ACC_Disqualified_PitExit = 17
    ACC_Disqualified_Wrongway = 18
    ACC_DriveThrough_IgnoredDriverStint = 19
    ACC_Disqualified_IgnoredDriverStint = 20
    ACC_Disqualified_ExceededDriverStintLimit = 21

class ACC_SESSION_TYPE(IntEnum):
    ACC_UNKNOWN = -1
    ACC_PRACTICE = 0
    ACC_QUALIFY = 1
    ACC_RACE = 2
    ACC_HOTLAP = 3
    ACC_TIMEATTACK = 4
    ACC_DRIFT = 5
    ACC_DRAG = 6
    ACC_HOTSTINT = 7
    ACC_HOTSTINTSUPERPOLE = 8

class ACC_STATUS(IntEnum):
    ACC_OFF = 0
    ACC_REPLAY = 1
    ACC_LIVE = 2
    ACC_PAUSE = 3

class ACC_WHEELS_TYPE(IntEnum):
    ACC_FrontLeft = 0
    ACC_FrontRight = 1
    ACC_RearLeft = 2
    ACC_RearRight = 3

class ACC_TRACK_GRIP_STATUS(IntEnum):
    ACC_GREEN = 0
    ACC_FAST = 1
    ACC_OPTIMUM = 2
    ACC_GREASY = 3
    ACC_DAMP = 4
    ACC_WET = 5
    ACC_FLOODED = 6

class ACC_RAIN_INTENSITY(IntEnum):
    ACC_NO_RAIN = 0
    ACC_DRIZZLE = 1
    ACC_LIGHT_RAIN = 2
    ACC_MEDIUM_RAIN = 3
    ACC_HEAVY_RAIN = 4
    ACC_THUNDERSTORM = 5


class SPageFileGraphic(StructureWithEnums):
    _fields_ = [
        ("packetId", c_int),
        ("status", c_int),
        ("session", c_int),
        ("currentTime", ShortWord),
        ("lastTime", ShortWord),
        ("bestTime", ShortWord),
        ("split", ShortWord),
        ("completedLaps", c_int),
        ("position", c_int),
        ("iCurrentTime", c_int),
        ("iLastTime", c_int),
        ("iBestTime", c_int),
        ("sessionTimeLeft", c_float),
        ("distanceTraveled", c_float),
        ("isInPit", c_int),
        ("currentSectorIndex", c_int),
        ("lastSectorTime", c_int),
        ("numberOfLaps", c_int),
        ("tyreCompound", Word),
        ("replayTimeMultiplier", c_float),
        ("normalizedCarPosition", c_float),
        ("activeCars", c_int),
        ("carCoordinates", c_float * 3 * 60),
        ("carID", c_int * 60),
        ("playerCarID", c_int),
        ("penaltyTime", c_float),
        ("flag", c_int),
        ("penalty", c_int),
        ("idealLineOn", c_int),
        ("isInPitLane", c_int),
        ("surfaceGrip", c_float),
        ("mandatoryPitDone", c_int),
        ("windSpeed", c_float),
        ("windDirection", c_float),
        ("isSetupMenuVisible", c_int),
        ("mainDisplayIndex", c_int),
        ("secondaryDisplayIndex", c_int),
        ("TC", c_int),
        ("TCCut", c_int),
        ("EngineMap", c_int),
        ("ABS", c_int),
        ("fuelXLap", c_int),
        ("rainLights", c_int),
        ("flashingLights", c_int),
        ("lightsStage", c_int),
        ("exhaustTemperature", c_float),
        ("wiperLV", c_int),
        ("DriverStintTotalTimeLeft", c_int),
        ("DriverStintTimeLeft", c_int),
        ("rainTyres", c_int),
        ("sessionIndex", c_int),
        ("usedFuel", c_float),
        ("deltaLapTime", ShortWord),
        ("iDeltaLapTime", c_int),
        ("estimatedLapTime", ShortWord),
        ("iEstimatedLapTime", c_int),
        ("isDeltaPositive", c_int),
        ("iSplit", c_int),
        ("isValidLap", c_int),
        ("fuelEstimatedLaps", c_float),
        ("trackStatus", Word),
        ("missingMandatoryPits", c_int),
        ("Clock", c_float),
        ("directionLightsLeft", c_int),
        ("directionLightsRight", c_int),
        ("GlobalYellow", c_int),
        ("GlobalYellow1", c_int),
        ("GlobalYellow2", c_int),
        ("GlobalYellow3", c_int),
        ("GlobalWhite", c_int),
        ("GlobalGreen", c_int),
        ("GlobalChequered", c_int),
        ("GlobalRed", c_int),
        ("mfdTyreSet", c_int),
        ("mfdFuelToAdd", c_float),
        ("mfdTyrePressureLF", c_float),
        ("mfdTyrePressureRF", c_float),
        ("mfdTyrePressureLR", c_float),
        ("mfdTyrePressureRR", c_float),
        ("trackGripStatus", c_int),
        ("rainIntensity", c_int),
        ("rainIntensityIn10min", c_int),
        ("rainIntensityIn30min", c_int),
        ("currentTyreSet", c_int),
        ("strategyTyreSet", c_int),
    ]
    _map = {
        "status": ACC_STATUS,
        "session": ACC_SESSION_TYPE,
        "flag": ACC_FLAG_TYPE,
        "penalty": ACC_PENALTY_TYPE,
        "trackGripStatus": ACC_TRACK_GRIP_STATUS,
        "rainIntensity": ACC_RAIN_INTENSITY,
        "rainIntensityIn10min": ACC_RAIN_INTENSITY,
        "rainIntensityIn30min": ACC_RAIN_INTENSITY,
    }


class CAR_CATEGORY(object):
    classes = ["GT3 - 2018", "GT3 - 2019", "GT4", "GT3 - 2020"]
    modelIds = [
        [12,3,11,8,7,14,2,17,13,4,18,15,5,1,10,6,0,9],
        [20,19,21,16,22,23],
        [50,51,52,53,55,56,57,58,59,60,61],
        [24,25]
    ]

    def get_category(self, carModel):
        for i, ids in enumerate(CAR_CATEGORY.modelIds):
            if ids.index(carModel) >= 0:
                return CAR_CATEGORY.classes[i]
        return None


class CAR_MODEL(IntEnum):
    amr_v12_vantage_gt3 = 12
    audi_r8_lms = 3
    bentley_continental_gt3_2016 = 11
    bentley_continental_gt3_2018 = 8
    bmw_m6_gt3 = 7
    jaguar_g3 = 14
    ferrari_488_gt3 = 2
    honda_nsx_gt3 = 17
    lamborghini_gallardo_rex = 13
    lamborghini_huracan_gt3 = 4
    lamborghini_huracan_st = 18
    lexus_rc_f_gt3 = 15
    mclaren_650s_gt3 = 5
    mercedes_amg_gt3 = 1
    nissan_gt_r_gt3_2017 = 10
    nissan_gt_r_gt3_2018 = 6
    porsche_991_gt3_r = 0
    porsche_991ii_gt3_cup = 9
    amr_v8_vantage_gt3 = 20
    audi_r8_lms_evo = 19
    honda_nsx_gt3_evo = 21
    lamborghini_huracan_gt3_evo = 16
    mclaren_720s_gt3 = 22
    porsche_991ii_gt3_r = 23
    alpine_a110_gt4 = 50
    amr_v8_vantage_gt4 = 51
    audi_r8_gt4 = 52
    bmw_m4_gt4 = 54
    chevrolet_camaro_gt4r = 55
    ginetta_g55_gt4 = 56
    ktm_xbow_gt4 = 57
    maserati_mc_gt4 = 58
    mclaren_570s_gt4 = 59
    mercedes_amg_gt4 = 60
    porsche_718_cayman_gt4_mr = 61
    ferrari_488_gt3_evo = 24
    mercedes_amg_gt3_evo = 25


carModelName = {
    12: "Aston Martin Vantage V12 GT3 2013",
    3: "Audi R8 LMS 2015",
    11: "Bentley Continental GT3 2015",
    8: "Bentley Continental GT3 2018",
    7: "BMW M6 GT3 2017",
    14:"Emil Frey Jaguar G3 2012",
    2: "Ferrari 488 GT3 2018",
    17: "Honda NSX GT3 2017",
    13: "Lamborghini Gallardo G3 Reiter 2017",
    4: "Lamborghini Huracan GT3 2015",
    18: "Lamborghini Huracan ST 2015",
    15: "Lexus RCF GT3 2016",
    5: "McLaren 650S GT3 2015",
    1: "Mercedes AMG GT3 2015",
    10: "Nissan GTR Nismo GT3 2015",
    6: "Nissan GTR Nismo GT3 2018",
    0: "Porsche 991 GT3 R 2018",
    9: "Porsche 991 II GT3 Cup 2017",
    20: "Aston Martin V8 Vantage GT3 2019",
    19: "Audi R8 LMS Evo 2019",
    21: "Honda NSX GT3 Evo 2019",
    16: "Lamborghini Huracan GT3 EVO 2019",
    22: "McLaren 720S GT3 2019",
    23: "Porsche 911 II GT3 R 2019",
    50: "Alpine A110 GT4 2018",
    51: "Aston Martin Vantage AMR GT4 2018",
    52: "Audi R8 LMS GT4 2016",
    53: "BMW M4 GT42 018",
    55: "Chevrolet Camaro GT4 R 2017",
    56: "Ginetta G55 GT4 2012",
    57: "Ktm Xbow GT4 2016",
    58: "Maserati Gran Turismo MC GT4 2016",
    59: "McLaren 570s GT4 2016",
    60: "Mercedes AMG GT4 2016",
    61: "Porsche 718 Cayman GT4 MR 2019",
    24: "Ferrari 488 GT3 Evo 2020",
    25: "Mercedes AMG GT3 Evo 2020",
}

maxRPM = {
    12: 7750,
    3: 8650,
    11: 7500,
    8: 7400,
    7: 7100,
    14: 8750,
    2: 7300,
    17: 7500,
    13: 8650,
    4: 8650,
    18: 8650,
    15: 7750,
    5: 7500,
    1: 7900,
    10: 7500,
    6: 7500,
    0: 9250,
    9: 8500,
    20: 7250,
    19: 8650,
    21: 7650,
    16: 8650,
    22: 7700,
    23: 9250,
    50: 6450,
    51: 7000,
    52: 8650,
    53: 7600,
    55: 7500,
    56: 7200,
    57: 6500,
    58: 7000,
    59: 7600,
    60: 7000,
    61: 7800,
    24: 7600,
    25: 7600,
}

class SPageFileStatic(LittleEndianStructure):
    _fields_ = [
        ("smVersion", ShortWord),
        ("acVersion", ShortWord),
        ("numberOfSessions", c_int),
        ("numCars", c_int),
        ("carModel", Word),
        ("track", Word),
        ("playerName", Word),
        ("playerSurname", Word),
        ("playerNick", Word),
        ("sectorCount", c_int),
        ("maxTorque", c_float),
        ("maxPower", c_float),
        ("maxRpm", c_int),
        ("maxFuel", c_float),
        ("suspensionMaxTravel", c_float * 4),
        ("tyreRadius", c_float * 4),
        ("maxTurboBoost", c_float),
        ("deprecated_1", c_float),
        ("deprecated_2", c_float),
        ("penaltiesEnabled", c_int),
        ("aidFuelRate", c_float),
        ("aidTireRate", c_float),
        ("aidMechanicalDamage", c_float),
        ("aidAllowTyreBlankets", c_int),
        ("aidStability", c_float),
        ("aidAutoClutch", c_int),
        ("aidAutoBlip", c_int),
        ("hasDRS", c_int),
        ("hasERS", c_int),
        ("hasKERS", c_int),
        ("kersMaxJ", c_float),
        ("engineBrakeSettingsCount", c_int),
        ("ersPowerControllerCount", c_int),
        ("trackSPlineLength", c_float),
        ("trackConfiguration", Word),
        ("ersMaxJ", c_float),
        ("isTimedRace", c_int),
        ("hasExtraLap", c_int),
        ("carSkin", Word),
        ("reversedGridPositions", c_int),
        ("PitWindowStart", c_int),
        ("PitWindowEnd", c_int),
        ("isOnline", c_int),
        ("dryTyresName", Word),
        ("wetTyresName", Word),
    ]



