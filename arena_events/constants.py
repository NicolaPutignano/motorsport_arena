EVENT_TYPES = [
    ('SingleRace', 'SingleRace'),
    ('Championship', 'Championship'),
    ('League', 'League')
]

STATUS_CHOICES = [
    ('Scheduled', 'Scheduled'),
    ('In progress', 'In progress'),
    ('Finished', 'Finished'),
    ('Deleted', 'Deleted'),
    ('Archived', 'Archived'),
]

RACE_TIME_PROGRESS = [
    ('Continuous', 'Continuous'),
    ('Fixed', 'Fixed')
]

RACE_LENGTH_TYPE = [
    ('Laps', 'Laps'),
    ('Minutes', 'Minutes')
]

RACE_INITIAL_TIME = [
    ('Personalized', 'Personalized'),
    ('Sunrise', 'Sunrise'),
    ('Morning', 'Morning'),
    ('Late morning', 'Late morning'),
    ('Noon', 'Noon'),
    ('Afternoon', 'Afternoon'),
    ('Late afternoon', 'Late afternoon'),
    ('Evening', 'Evening'),
    ('Sunset', 'Sunset'),
    ('Night', 'Night'),
    ('Midnight', 'Midnight')
]

RACE_WEATHER = [
    ('Random', 'Random'),
    ('Variable', 'Variable'),
    ('Clear', 'Clear'),
    ('Mostly clear', 'Mostly clear'),
    ('Partly cloudy', 'Partly cloudy'),
    ('Cloudy', 'Cloudy'),
    ('Threatening clouds', 'Threatening clouds'),
    ('Thundering clouds', 'Thundering clouds'),
    ('Light mist', 'Light mist'),
    ('Irregular fog', 'Irregular fog'),
    ('Thick fog', 'Thick fog'),
    ('Cloudy (dry)', 'Cloudy (dry)'),
    ('Cloudy (wet)', 'Cloudy (wet)'),
    ('Fine rain', 'Fine rain'),
    ('Light rain', 'Light rain'),
    ('Moderate rain', 'Moderate rain'),
    ('Heavy rain', 'Heavy rain'),
    ('Tempest', 'Tempest'),
    ('Storm', 'Storm'),
]

RACE_PENALTY = [
    ('No', 'No'),
    ('Limited', 'Limited'),
    ('Moderate', 'Moderate'),
    ('Complete', 'Complete')
]

CAR_TRACTION = [
    ('FWD', 'Front-Wheel Drive'),
    ('RWD', 'Rear-Wheel Drive'),
    ('AWD', 'All-Wheel Drive')
]

CAR_ENGINE_POS = [
    ('F', 'Front'),
    ('MF', 'Front-Mid'),
    ('MR', 'Rear-Mid'),
    ('R', 'Rear')
]

CAR_WHEEL_TYPE = [
    ('Factory', 'Factory'),
    ('Race', 'Race'),
    ('Upgraded', 'Upgraded'),
]

CAR_STEER_POS = [
    ('C', 'Central'),
    ('L', 'Left'),
    ('R', 'Right')
]

CFG = [
    ('E', 'E'),
    ('F', 'F'),
    ('I', 'I'),
    ('R', 'R'),
    ('V', 'V'),
    ('VR', 'VR'),
    ('W', 'W'),

]

IND = [
    ('DSC', 'DSC'),
    ('EV', 'EV'),
    ('NA', 'Naturally Aspirated'),
    ('T', 'T'),
    ('T4', 'T4'),
    ('TT', 'TT'),
]

EVENT_DOC_DIR = ['event_documents/']

EVENT_ROLE_CHOICES = [
    ('Manager', 'Manager'),
    ('Staff', 'Staff'),
    ('Pilot', 'Pilot'),
]
