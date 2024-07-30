from django.db import models


class EventTypes(models.TextChoices):
    SINGLERACE = "SingleRace"
    CHAMPIONSHIP = "Championship"
    LEAGUE = "League"


class Status(models.TextChoices):
    SCHEDULED = "Scheduled"
    PROGRESS = "In progres"
    Finished = "Finished"
    DELETED = "Deleted"
    ARCHIVED = "Archived"


class RaceGameType(models.TextChoices):
    CIRCUIT_RACE = "Circuit Race"
    TIMED_RACE = "Timed Race"


class RaceLength(models.TextChoices):
    SHORT = "Short"
    MEDIUM = "Medium"
    LONG = "Long"
    CUSTOM = "Custom"


class RaceStartingTime(models.TextChoices):
    CUSTOM = "Custom"
    SUNRISE = "Sunrise"
    MORNING = "Morning"
    LATE_MORNING = "Late Morning"
    NOON = "Noon"
    AFTERNOON = "Afternoon"
    LATE_AFTERNOON = "Late Afternoon"
    EVENING = "Evening"
    SUNSET = "Sunset"
    NIGHT = "Night"
    MIDNIGHT = "Midnight"


class RaceTimeProgress(models.TextChoices):
    ROLLING = "Rolling"
    FIXED = "Fixed"


class RaceWeather(models.TextChoices):
    RANDOM = "Random"
    VARIABLE = "Variable"
    CLEAR = "Clear"
    MOSTLY_CLEAR = "Mostly Clear"
    PARTLY_CLOUDY = "Partly Cloudy"
    CLOUDY = "Cloudy"
    LOOMING_CLOUDS = "Looming Clouds"
    THUNDERCLOUDS = "Thunderclouds"
    THIN_HAZE = "Thin Haze"
    PATCHY_FOG = "Patchy Fog"
    DENSE_FOG = "Dense Fog"
    OVERCAST_DRY = "Overcast Dry"
    OVERCAST_WET = "Overcast Wet"
    DRIZZLE = "Drizzle"
    LIGHT_RAIN = "Light Rain"
    MODERATE_RAIN = "Moderate Rain"
    HEAVY_RAIN = "Heavy rain"
    THUNDERSTORM = "Thunderstorm"
    RAINSTORM = "Rainstorm"


class RacePenalty(models.TextChoices):
    OFF = "Off"
    LIMITED = "Limited"
    MODERATE = "Moderate"
    FULL = "Full"


class RaceShifting(models.TextChoices):
    AUTOMATIC = "Automatic"
    MANUAL = "Manual"
    MANUAL_CLUTCH = "Manual with Clutch only"


class RaceSteering(models.TextChoices):
    FULLY = "Full assisted"
    PARTIALLY = "Partially assisted"
    NORMAL = "Normal"
    SIMULATION = "Simulation only"


class RaceBreakingAssist(models.TextChoices):
    ASSISTED = "Assisted"
    ABS_ON = "ABS on"
    ABS_OFF = "ABS off"


class RaceCameraView(models.TextChoices):
    NONE = "None"
    BUMPER = "Bumper"
    HOOD = "Hood"
    COCKPIT = "Cockpit"
    DRIVER = "Driver"
    CHASE_NEAR = "Chase Near"
    CHASE_FAR = "Chase Far"


class EventRole(models.TextChoices):
    MANAGER = "Manager"
    STAFF = "Staff"
    PILOT = "Pilot"
